import React from "react";

import MatchTable from "../../../components/MatchTable";
import { APIMatch } from "../../../components/types/api";
import { MatchData } from "../types";

const UpcomingMatches = ({ data }: { data: MatchData }) => {
  return (
    <div>
      {data.upcoming_matches.map((match) => {
        return (
          <div key={match.match.key} className="w-full p-4 m-4 rounded">
            <div className="text-center text-2xl font-bold">{match.event_name}</div>
            <MatchTable year={2023} teamNum={0} matches={[match.match]} foulRate={0} />
          </div>
        );
      })}
    </div>
  );
};

export default UpcomingMatches;
