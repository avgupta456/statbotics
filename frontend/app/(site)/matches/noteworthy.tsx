import React, { useEffect, useState } from "react";

import MatchTable from "../../../components/MatchTable";
import { FilterBar } from "../../../components/filter";
import { APIMatch } from "../../../components/types/api";
import { BACKEND_URL } from "../../../constants";
import { log, round } from "../../../utils";

const lightGray = "#F0F0F0";

type MatchData = {
  matches: {
    high_score: APIMatch[];
    combined_score: APIMatch[];
    losing_score: APIMatch[];
  };
  foul_rate: number;
};

const NoteworthySection = ({
  year,
  foulRate,
  matches,
  mainHeader,
  header,
  accessor,
}: {
  year: number;
  foulRate: number;
  matches: APIMatch[];
  mainHeader: string;
  header: string;
  accessor: (match: APIMatch) => number;
}) => {
  return (
    <div className="w-full">
      <div className="w-full text-2xl font-bold my-4">{mainHeader}</div>
      <div className="flex overflow-x-scroll scrollbar-hide">
        <div className="w-32 flex flex-col border-2 border-gray-300">
          <div
            className="flex h-8 justify-center items-center"
            style={{ backgroundColor: lightGray }}
          >
            {header}
          </div>
          {matches.map((match, i) => (
            <div
              className="flex w-full h-8 justify-center items-center border-b border-gray-300 bg-green-100"
              key={`${match.key}-${i}`}
            >
              {i + 1}. {accessor(match).toFixed(0)}
            </div>
          ))}
        </div>
        <div className="flex-grow min-w-[720px]">
          <MatchTable
            year={year}
            teamNum={0}
            matches={matches}
            foulRate={foulRate}
            showHeaders={true}
            showSubHeaders={false}
            sorted={false}
            showVideo={true}
            rawTitle={true}
            stacked={false}
          />
        </div>
      </div>
    </div>
  );
};

const defaultFilters = {
  country: "",
  state: "",
  district: "",
  playoff: "",
  week: "",
};

async function getMatchData(year, country, state, district, playoff, week) {
  const start = performance.now();
  let suffix = "";
  if (country) suffix += `?country=${country}`;
  if (state) suffix += (suffix ? "&" : "?") + `state=${state}`;
  if (district) suffix += (suffix ? "&" : "?") + `district=${district}`;
  if (playoff) suffix += (suffix ? "&" : "?") + `playoff=${playoff}`;
  if (week) suffix += (suffix ? "&" : "?") + `week=${week}`;

  const res = await fetch(`${BACKEND_URL}/noteworthy_matches/${year}${suffix}`, {
    next: { revalidate: 60 },
  });
  log(`/noteworthy_matches/${year}/ took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }

  return (await res.json())?.data;
}

const NoteworthyMatches = ({ year }: { year: number }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState<MatchData>(null);
  const [filters, setFilters] = useState(defaultFilters);

  useEffect(() => {
    setLoading(true);
    getMatchData(
      year,
      filters.country,
      filters.state,
      filters.district,
      filters.playoff,
      filters.week
    ).then((data) => {
      if (data) {
        setData(data);
      } else {
        setError(true);
      }
      setLoading(false);
    });
  }, [year, filters]);

  if (error) {
    return (
      <div className="w-full flex-grow flex flex-col items-center justify-center">
        <div className="text-gray-700 mt-4">Error loading data</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col mb-4">
      <FilterBar defaultFilters={defaultFilters} filters={filters} setFilters={setFilters} />
      <div className="flex flex-col">
        {data !== null && !loading ? (
          <>
            <NoteworthySection
              year={year}
              foulRate={data.foul_rate}
              matches={data.matches.high_score}
              mainHeader="Highest Clean Scores"
              header={"Highest Score"}
              accessor={(match) =>
                Math.max(
                  match.red_auto + match.red_teleop + match.red_endgame,
                  match.blue_auto + match.blue_teleop + match.blue_endgame
                )
              }
            />
            <div className="w-full text-sm ml-4 mt-4 mb-4">
              <strong>1.</strong> Technically clean winning score, as we include each match only
              once.
            </div>
            <NoteworthySection
              year={year}
              foulRate={data.foul_rate}
              matches={data.matches.combined_score}
              mainHeader="Highest Combined Clean Scores"
              header={"Combined Score"}
              accessor={(match) =>
                match.red_auto +
                match.red_teleop +
                match.red_endgame +
                match.blue_auto +
                match.blue_teleop +
                match.blue_endgame
              }
            />
            <div className="mb-8" />
            <NoteworthySection
              year={year}
              foulRate={data.foul_rate}
              matches={data.matches.losing_score}
              mainHeader="Highest Losing Scores"
              header={"Losing Score"}
              accessor={(match) => Math.min(match.red_score, match.blue_score)}
            />
            <div className="w-full text-sm ml-4 mt-4 mb-4">
              <strong>1.</strong> Includes fouls, unlike above two tables.
            </div>
          </>
        ) : (
          <div className="w-full flex-grow flex flex-col items-center justify-center">
            <div className="text-gray-700 mt-4">
              {loading ? "Loading data, please wait..." : "No upcoming matches"}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NoteworthyMatches;
