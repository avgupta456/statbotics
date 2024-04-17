import React from "react";

import MatchTable from "../../../../components/MatchTable";
import { MAX_TEAM, RP_NAMES } from "../../../../constants";
import { EventData } from "../../../../types/data";
import { round } from "../../../../utils";

const MatchSection = ({ year, quals, data }: { year: number; quals: boolean; data: EventData }) => {
  const matches = data.matches.filter((match) => match.elim === !quals);

  const N = matches.filter((match) => match.status === "Completed").length;
  const correctPreds = matches
    .filter((match) => match.status === "Completed")
    .reduce((acc, match) => {
      if (match.pred.winner === match.result.winner) {
        return acc + 1;
      }
      return acc;
    }, 0);
  const accuracy = round((correctPreds / Math.max(N, 1)) * 100, 1);

  const rp1CorrectPreds = matches
    .filter((match) => !match.elim && match.status === "Completed")
    .reduce((acc, match) => {
      if (match.pred.red_rp_1 > 0.5 === match.result.red_rp_1 > 0.5) {
        acc = acc + 1;
      }
      if (match.pred.blue_rp_1 > 0.5 === match.result.blue_rp_1 > 0.5) {
        acc = acc + 1;
      }
      return acc;
    }, 0);
  const rp1Accuracy = round((rp1CorrectPreds / (2 * Math.max(N, 1))) * 100, 1);

  const rp2CorrectPreds = matches
    .filter((match) => !match.elim && match.status === "Completed")
    .reduce((acc, match) => {
      if (match.pred.red_rp_2 > 0.5 === match.result.red_rp_2 > 0.5) {
        acc = acc + 1;
      }
      if (match.pred.blue_rp_2 > 0.5 === match.result.blue_rp_2 > 0.5) {
        acc = acc + 1;
      }
      return acc;
    }, 0);
  const rp2Accuracy = round((rp2CorrectPreds / (2 * Math.max(N, 1))) * 100, 1);

  return (
    <div className="flex flex-col">
      <div className="w-full text-2xl font-bold mb-4">Match Predictions</div>
      <div>Remember, match predictions are just for fun, you control your own destiny!</div>
      {N > 0 && (
        <div>
          <strong>Accuracy: {accuracy}%</strong>
          {quals &&
            year >= 2016 &&
            ` | ${RP_NAMES?.[year]?.[0]} Accuracy: ${rp1Accuracy}% | ${RP_NAMES?.[year]?.[1]} Accuracy: ${rp2Accuracy}%`}
        </div>
      )}
      {data.event.offseason && (
        <div className="mb-4">
          This event is an <strong>offseason</strong> event. Offseason teams are assigned a default
          EPA and EPAs do not update. Prediction accuracy may be lower than expected.
        </div>
      )}
      <div className="w-full my-4 overflow-x-scroll scrollbar-hide">
        <MatchTable year={data.event.year} teamNum={""} matches={matches} />
      </div>
    </div>
  );
};

export default MatchSection;
