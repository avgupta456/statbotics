import React from "react";

import MatchTable from "../../../components/MatchTable";
import { APIMatch } from "../../../components/types/api";
import { formatMatch } from "../../../components/utils";
import { truncate } from "../../../utils";
import { MatchData } from "../types";

const UpcomingMatches = ({ data }: { data: MatchData }) => {
  return (
    <div className="flex flex-col gap-8">
      {data.upcoming_matches
        .sort((a, b) => a.match.predicted_time - b.match.predicted_time)
        .map((match) => {
          return (
            <div key={match.match.key} className="w-full">
              <div className="w-full flex flex-wrap justify-center text-lg mb-2">
                <p className="font-bold mr-1">{truncate(match.event_name, 30)}</p>
                {" - "}
                {formatMatch(
                  match.match.comp_level,
                  match.match.match_number,
                  match.match.set_number
                )}
              </div>
              <div className="w-full md:w-2/3 lg:w-1/2 overflow-x-scroll scrollbar-hide mx-auto">
                <MatchTable
                  year={2023}
                  teamNum={0}
                  matches={[match.match]}
                  foulRate={0}
                  showHeaders={true}
                  showSubHeaders={false}
                  showVideo={false}
                  stacked={true}
                />
              </div>
            </div>
          );
        })}
    </div>
  );
};

export default UpcomingMatches;
