import React, { useEffect, useState } from "react";

import { getNoteworthyMatches } from "../../../api/matches";
import MatchTable from "../../../components/MatchTable";
import { FilterBar } from "../../../components/filterBar";
import { APIMatch } from "../../../types/api";
import { classnames } from "../../../utils";

const lightGray = "#F0F0F0";

type MatchData = {
  high_score: APIMatch[];
  combined_score: APIMatch[];
  losing_score: APIMatch[];
  high_auto_score?: APIMatch[];
  high_teleop_score?: APIMatch[];
  high_endgame_score?: APIMatch[];
};

const NoteworthySection = ({
  year,
  matches,
  mainHeader,
  header,
  accessor,
  redAccessor,
  blueAccessor,
}: {
  year: number;
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
            teamNum={""}
            matches={matches.slice(0, more ? matches.length : Math.min(matches.length, 10))}
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
    getNoteworthyMatches(
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
  }, [year, actualFilters, currYear, currFilters]);

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
              matches={data?.high_score || []}
              mainHeader={year < 2016 ? "Highest Scores" : "Highest Clean Scores"}
              header={"Max Score"}
              accessor={(match) =>
                year < 2016
                  ? Math.max(match.result.red_score, match.result.blue_score)
                  : Math.max(match.result.red_no_foul, match.result.blue_no_foul)
              }
              redAccessor={(match) =>
                year < 2016 ? match.result.red_score : match.result.red_no_foul
              }
              blueAccessor={(match) =>
                year < 2016 ? match.result.blue_score : match.result.blue_no_foul
              }
            />
            <div className="w-full text-sm ml-4 mt-4 mb-4">
              <strong>1.</strong> Technically highest winning score, as we include each match only
              once.
            </div>
            <NoteworthySection
              year={year}
              matches={data?.combined_score || []}
              mainHeader={year < 2016 ? "Highest Combined Scores" : "Highest Combined Clean Scores"}
              header={"Sum Score"}
              accessor={(match) =>
                year < 2016
                  ? match.result.red_score + match.result.blue_score
                  : match.result.red_no_foul + match.result.blue_no_foul
              }
            />
            <div className="mb-8" />
            <NoteworthySection
              year={year}
              matches={data?.losing_score || []}
              mainHeader="Highest Losing Scores"
              header={"Losing Score"}
              accessor={(match) => Math.min(match.result.red_score, match.result.blue_score)}
              redAccessor={(match) => match.result.red_score}
              blueAccessor={(match) => match.result.blue_score}
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
                  matches={data?.high_auto_score || []}
                  mainHeader="Highest Auto Scores"
                  header={"Auto Score"}
                  accessor={(match) =>
                    Math.max(match.result.red_auto_points, match.result.blue_auto_points)
                  }
                  redAccessor={(match) => match.result.red_auto_points}
                  blueAccessor={(match) => match.result.blue_auto_points}
                />
                <div className="mb-8" />
                <NoteworthySection
                  year={year}
                  matches={data?.high_teleop_score || []}
                  mainHeader="Highest Teleop Scores"
                  header={"Teleop Score"}
                  accessor={(match) =>
                    Math.max(match.result.red_teleop_points, match.result.blue_teleop_points)
                  }
                  redAccessor={(match) => match.result.red_teleop_points}
                  blueAccessor={(match) => match.result.blue_teleop_points}
                />
                <div className="mb-8" />
                <NoteworthySection
                  year={year}
                  matches={data?.high_endgame_score || []}
                  mainHeader="Highest Endgame Scores"
                  header={"Endgame Score"}
                  accessor={(match) =>
                    Math.max(match.result.red_endgame_points, match.result.blue_endgame_points)
                  }
                  redAccessor={(match) => match.result.red_endgame_points}
                  blueAccessor={(match) => match.result.blue_endgame_points}
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
