import React, { useEffect, useState } from "react";

import MatchTable from "../../../components/MatchTable";
import { FilterBar } from "../../../components/filterBar";
import { APIMatch } from "../../../components/types/api";
import { BACKEND_URL } from "../../../constants";
import { classnames, log, round } from "../../../utils";

const lightGray = "#F0F0F0";

type MatchData = {
  matches: {
    high_score: APIMatch[];
    combined_score: APIMatch[];
    losing_score: APIMatch[];
    high_auto_score?: APIMatch[];
    high_teleop_score?: APIMatch[];
    high_endgame_score?: APIMatch[];
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
  redAccessor,
  blueAccessor,
}: {
  year: number;
  foulRate: number;
  matches: APIMatch[];
  mainHeader: string;
  header: string;
  accessor: (match: APIMatch) => number;
  redAccessor?: (match: APIMatch) => number;
  blueAccessor?: (match: APIMatch) => number;
}) => {
  const [more, setMore] = useState(false);

  return (
    <div className="w-full">
      <div className="w-full flex items-center text-2xl font-bold my-4">
        {mainHeader}
        {matches.length > 10 && (
          <button
            className="w-24 p-2 ml-4 rounded bg-blue-500 hover:bg-blue-600 text-white text-sm"
            onClick={() => setMore(!more)}
          >
            {more ? "Show Less" : "Show More"}
          </button>
        )}
      </div>
      <div className="flex overflow-x-scroll scrollbar-hide">
        <div className="min-w-[100px] md:min-w-[135px] flex flex-col border-2 border-gray-300">
          <div
            className="flex h-8 justify-center items-center text-xs md:text-sm lg:text-base"
            style={{ backgroundColor: lightGray }}
          >
            {header}
          </div>
          {matches
            .slice(0, more ? matches.length : Math.min(matches.length, 10))
            .map((match, i) => (
              <div
                className={classnames(
                  "flex w-full h-8 justify-center items-center border-b border-gray-300 bg-green-100",
                  redAccessor && redAccessor(match) === accessor(match) && "text-red-500",
                  blueAccessor && blueAccessor(match) === accessor(match) && "text-blue-600"
                )}
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
            matches={matches.slice(0, more ? matches.length : Math.min(matches.length, 10))}
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

const defaultFilters = {
  country: "",
  state: "",
  district: "",
  playoff: "",
  week: "",
};

const NoteworthyMatches = ({
  year,
  filters,
  setFilters,
}: {
  year: number;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
}) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState<MatchData>(null);

  const [currYear, setCurrYear] = useState(-1);
  const [currFilters, setCurrFilters] = useState({});

  const actualFilters: { [key: string]: any } = Object.keys(defaultFilters).reduce(
    (acc, key) => ({ ...acc, [key]: filters[key] || defaultFilters[key] }),
    {}
  );

  useEffect(() => {
    if (year === currYear && JSON.stringify(currFilters) === JSON.stringify(actualFilters)) {
      return;
    }

    setLoading(true);
    getMatchData(
      year,
      actualFilters.country,
      actualFilters.state,
      actualFilters.district,
      actualFilters.playoff,
      actualFilters.week
    ).then((data) => {
      if (data) {
        setData(data);
        setCurrYear(year);
        setCurrFilters(actualFilters);
      } else {
        setError(true);
      }
      setLoading(false);
    });
  }, [year, actualFilters, currFilters]);

  if (error) {
    return (
      <div className="w-full flex-grow flex flex-col items-center justify-center">
        <div className="text-gray-700 mt-4">Error loading data</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col mb-4">
      <FilterBar defaultFilters={defaultFilters} filters={actualFilters} setFilters={setFilters} />
      <div className="flex flex-col">
        {data !== null && !loading ? (
          <>
            <NoteworthySection
              year={year}
              foulRate={data.foul_rate}
              matches={data?.matches?.high_score || []}
              mainHeader={year < 2016 ? "Highest Scores" : "Highest Clean Scores"}
              header={"Max Score"}
              accessor={(match) =>
                year < 2016
                  ? Math.max(match.red_score, match.blue_score)
                  : Math.max(
                      match.red_auto + match.red_teleop + match.red_endgame,
                      match.blue_auto + match.blue_teleop + match.blue_endgame
                    )
              }
              redAccessor={(match) =>
                year < 2016
                  ? match.red_score
                  : match.red_auto + match.red_teleop + match.red_endgame
              }
              blueAccessor={(match) =>
                year < 2016
                  ? match.blue_score
                  : match.blue_auto + match.blue_teleop + match.blue_endgame
              }
            />
            <div className="w-full text-sm ml-4 mt-4 mb-4">
              <strong>1.</strong> Technically highest winning score, as we include each match only
              once.
            </div>
            <NoteworthySection
              year={year}
              foulRate={data.foul_rate}
              matches={data?.matches?.combined_score || []}
              mainHeader={year < 2016 ? "Highest Combined Scores" : "Highest Combined Clean Scores"}
              header={"Sum Score"}
              accessor={(match) =>
                year < 2016
                  ? match.red_score + match.blue_score
                  : match.red_auto +
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
              matches={data?.matches?.losing_score || []}
              mainHeader="Highest Losing Scores"
              header={"Losing Score"}
              accessor={(match) => Math.min(match.red_score, match.blue_score)}
              redAccessor={(match) => match.red_score}
              blueAccessor={(match) => match.blue_score}
            />
            {year >= 2016 && (
              <div className="w-full text-sm ml-4 mt-4 mb-4">
                <strong>1.</strong> Includes fouls, unlike above two tables.
              </div>
            )}
            {year >= 2016 && (
              <>
                <NoteworthySection
                  year={year}
                  foulRate={data.foul_rate}
                  matches={data?.matches?.high_auto_score || []}
                  mainHeader="Highest Auto Scores"
                  header={"Auto Score"}
                  accessor={(match) => Math.max(match.red_auto, match.blue_auto)}
                  redAccessor={(match) => match.red_auto}
                  blueAccessor={(match) => match.blue_auto}
                />
                <div className="mb-8" />
                <NoteworthySection
                  year={year}
                  foulRate={data.foul_rate}
                  matches={data?.matches?.high_teleop_score || []}
                  mainHeader="Highest Teleop Scores"
                  header={"Teleop Score"}
                  accessor={(match) => Math.max(match.red_teleop, match.blue_teleop)}
                  redAccessor={(match) => match.red_teleop}
                  blueAccessor={(match) => match.blue_teleop}
                />
                <div className="mb-8" />
                <NoteworthySection
                  year={year}
                  foulRate={data.foul_rate}
                  matches={data?.matches?.high_endgame_score || []}
                  mainHeader="Highest Endgame Scores"
                  header={"Endgame Score"}
                  accessor={(match) => Math.max(match.red_endgame, match.blue_endgame)}
                  redAccessor={(match) => match.red_endgame}
                  blueAccessor={(match) => match.blue_endgame}
                />
              </>
            )}
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
