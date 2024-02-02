import { useEffect, useState } from "react";

import { Button } from "@mantine/core";

import { getNoteworthyMatches } from "../../api/matches";
import MatchTable from "../../components/matchTable";
import { useData } from "../../contexts/dataContext";
import { useLocation } from "../../contexts/locationContext";
import { APIMatch } from "../../types/api";
import { classnames } from "../../utils/utils";
import MatchesFilterBar from "./filterBar";

const lightGray = "#F0F0F0";

type NoteworthyMatchObjs = {
  high_score: APIMatch[];
  combined_score: APIMatch[];
  losing_score: APIMatch[];
  high_auto_score?: APIMatch[];
  high_teleop_score?: APIMatch[];
  high_endgame_score?: APIMatch[];
};

function NoteworthySection({
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
  // eslint-disable-next-line no-unused-vars
  accessor: (match: APIMatch) => number;
  // eslint-disable-next-line no-unused-vars
  redAccessor?: (match: APIMatch) => number;
  // eslint-disable-next-line no-unused-vars
  blueAccessor?: (match: APIMatch) => number;
}) {
  const [more, setMore] = useState(false);

  return (
    <div className="w-full">
      <div className="my-4 flex w-full items-center text-2xl font-bold">
        {mainHeader}
        {matches.length > 10 && (
          <Button className="ml-4" onClick={() => setMore(!more)}>
            {more ? "Show Less" : "Show More"}
          </Button>
        )}
      </div>
      <div className="scrollbar-hide flex overflow-x-scroll">
        <div className="flex min-w-[100px] flex-col border-2 border-gray-300 md:min-w-[135px]">
          <div
            className="flex h-8 items-center justify-center text-xs md:text-sm lg:text-base"
            style={{ backgroundColor: lightGray }}
          >
            {header}
          </div>
          {matches
            .slice(0, more ? matches.length : Math.min(matches.length, 10))
            .map((match, i) => (
              <div
                className={classnames(
                  "flex h-8 w-full items-center justify-center border-b border-gray-300 bg-green-100",
                  redAccessor && redAccessor(match) === accessor(match) && "text-red-500",
                  blueAccessor && blueAccessor(match) === accessor(match) && "text-blue-600",
                )}
                // eslint-disable-next-line react/no-array-index-key
                key={`${match.key}-${i}`}
              >
                {i + 1}. {accessor(match).toFixed(0)}
              </div>
            ))}
        </div>
        <div className="min-w-[720px] flex-grow">
          <MatchTable
            year={year}
            teamNum=""
            matches={matches.slice(0, more ? matches.length : Math.min(matches.length, 10))}
            showHeaders
            showSubHeaders={false}
            sorted={false}
            showVideo
            rawTitle
            stacked={false}
          />
        </div>
      </div>
    </div>
  );
}

export default function NoteworthyMatches() {
  const { year } = useData();
  const { location } = useLocation();
  const [elim, setElim] = useState<string | null>(null);
  const [week, setWeek] = useState<number | null>(null);

  const [loading, setLoading] = useState<boolean>(true);
  const [data, setData] = useState<NoteworthyMatchObjs | null>(null);

  useEffect(() => {
    const getData = async () => {
      setLoading(true);
      const noteworthyMatches = await getNoteworthyMatches(year, location, elim, week);
      setData(noteworthyMatches);
      setLoading(false);
    };

    getData();
  }, [year, location, elim, week]);

  // eslint-disable-next-line no-console
  console.log(data);

  return (
    <div>
      <MatchesFilterBar week={week} setWeek={setWeek} elim={elim} setElim={setElim} />
      <div className="flex flex-col">
        {data !== null && !loading ? (
          <>
            <NoteworthySection
              year={year}
              matches={data?.high_score || []}
              mainHeader={year < 2016 ? "Highest Scores" : "Highest Clean Scores"}
              header="Max Score"
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
            <div className="mb-4 ml-4 mt-4 w-full text-sm">
              <strong>1.</strong> Technically highest winning score, as we include each match only
              once.
            </div>
            <NoteworthySection
              year={year}
              matches={data?.combined_score || []}
              mainHeader={year < 2016 ? "Highest Combined Scores" : "Highest Combined Clean Scores"}
              header="Sum Score"
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
              header="Losing Score"
              accessor={(match) => Math.min(match.result.red_score, match.result.blue_score)}
              redAccessor={(match) => match.result.red_score}
              blueAccessor={(match) => match.result.blue_score}
            />
            {year >= 2016 && (
              <div className="mb-4 ml-4 mt-4 w-full text-sm">
                <strong>1.</strong> Includes fouls, unlike above two tables.
              </div>
            )}
            {year >= 2016 && (
              <>
                <NoteworthySection
                  year={year}
                  matches={data?.high_auto_score || []}
                  mainHeader="Highest Auto Scores"
                  header="Auto Score"
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
                  header="Teleop Score"
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
                  header="Endgame Score"
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
          <div className="flex w-full flex-grow flex-col items-center justify-center">
            <div className="mt-4 text-gray-700">
              {loading ? "Loading data, please wait..." : "No upcoming matches"}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
