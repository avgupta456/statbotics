import React from "react";

import MatchTable from "../../../../components/MatchTable";
import { MAX_TEAM, RPMapping } from "../../../../constants";
import { round } from "../../../../utils";
import { Data } from "./types";

const MatchSection = ({ year, quals, data }: { year: number; quals: boolean; data: Data }) => {
  const matches = data.matches.filter((match) => match.playoff === !quals);

  const N = matches.filter((match) => match.status === "Completed").length;
  const correctPreds = matches
    .filter((match) => match.status === "Completed")
    .reduce((acc, match) => {
      if (match.pred_winner === match.winner) {
        return acc + 1;
      }
      return acc;
    }, 0);
  const accuracy = round((correctPreds / Math.max(N, 1)) * 100, 1);

  const rp1CorrectPreds = matches
    .filter((match) => !match.playoff && match.status === "Completed")
    .reduce((acc, match) => {
      if (match.red_rp_1_pred > 0.5 === match.red_rp_1 > 0.5) {
        acc = acc + 1;
      }
      if (match.blue_rp_1_pred > 0.5 === match.blue_rp_1 > 0.5) {
        acc = acc + 1;
      }
      return acc;
    }, 0);
  const rp1Accuracy = round((rp1CorrectPreds / (2 * Math.max(N, 1))) * 100, 1);

  const rp2CorrectPreds = matches
    .filter((match) => !match.playoff && match.status === "Completed")
    .reduce((acc, match) => {
      if (match.red_rp_2_pred > 0.5 === match.red_rp_2 > 0.5) {
        acc = acc + 1;
      }
      if (match.blue_rp_2_pred > 0.5 === match.blue_rp_2 > 0.5) {
        acc = acc + 1;
      }
      return acc;
    }, 0);
  const rp2Accuracy = round((rp2CorrectPreds / (2 * Math.max(N, 1))) * 100, 1);

  const hasOffseasonTeams = matches.some(
    (match) => Math.max(...match.red, ...match.blue) > MAX_TEAM
  );

  return (
    <div className="flex flex-col">
      <div className="w-full text-2xl font-bold mb-4">Match Predictions</div>
      <div>Remember, match predictions are just for fun, you control your own destiny!</div>
      {N > 0 && (
        <div>
          <strong>Accuracy: {accuracy}%</strong>
          {quals &&
            year >= 2016 &&
            ` | ${RPMapping?.[year]?.[0]} Accuracy: ${rp1Accuracy}% | ${RPMapping?.[year]?.[1]} Accuracy: ${rp2Accuracy}%`}
        </div>
      )}
      {hasOffseasonTeams && (
        <div className="mb-4">
          This event has <strong>offseason teams</strong> which are assigned a default EPA value. As
          a result, prediction accuracy may be lower than expected.
        </div>
      )}
      <div className="w-full my-4 overflow-x-scroll scrollbar-hide">
        <MatchTable year={data.event.year} teamNum={0} matches={matches} />
      </div>
    </div>
  );
};

export default MatchSection;
