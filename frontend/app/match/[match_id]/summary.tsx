import React from "react";

import PieChart from "../../../components/Pie";
import { BLUE, RED } from "../../../constants";
import { classnames } from "../../../utils";
import { Data } from "./types";

const Summary = ({ data }: { data: Data }) => {
  const winProb = data.match.epa_win_prob;
  const redWinProb = winProb * 100;
  const blueWinProb = (1 - winProb) * 100;

  const redPred = data.match.red_epa_sum * (1 + data.year_stats.foul_rate);
  const bluePred = data.match.blue_epa_sum * (1 + data.year_stats.foul_rate);

  const redScore = data.match.red_score;
  const blueScore = data.match.blue_score;

  return (
    <div className="w-full lg:w-1/2 flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-4">Summary</p>
      <div className="w-full flex-grow flex flex-row flex-wrap">
        <div className="w-full lg:w-1/2 h-full flex flex-col justify-around">
          <div className="w-full flex flex-col items-center">
            <div className="flex text-3xl">
              <p className={classnames("data text-red-500", redPred > bluePred ? "font-bold" : "")}>
                {Math.round(redPred)}
              </p>
              <p className="mx-2">-</p>
              <p
                className={classnames("data text-blue-500", bluePred > redPred ? "font-bold" : "")}
              >
                {Math.round(bluePred)}
              </p>
            </div>
            <div className="mt-4 text-lg flex">
              Projected Winner:{" "}
              <p
                className={classnames(
                  "ml-2",
                  data.match.epa_winner === "red" ? "text-red-500" : "text-blue-500"
                )}
              >
                {data.match.epa_winner.toUpperCase()}
              </p>
            </div>
          </div>
          <div className="w-full flex flex-col items-center">
            <div className="flex text-3xl">
              <p
                className={classnames("data text-red-500", redScore > blueScore ? "font-bold" : "")}
              >
                {Math.round(redScore)}
              </p>
              <p className="mx-2">-</p>
              <p
                className={classnames(
                  "data text-blue-500",
                  blueScore > redScore ? "font-bold" : ""
                )}
              >
                {Math.round(blueScore)}
              </p>
            </div>
            <div className="mt-4 text-lg flex">
              Actual Winner:{" "}
              <p
                className={classnames(
                  "ml-2",
                  data.match.winner === "red" ? "text-red-500" : "text-blue-500"
                )}
              >
                {data.match.winner.toUpperCase()}
              </p>
            </div>
          </div>
        </div>
        <div className="w-full lg:w-1/2 flex flex-col justify-center items-center">
          <PieChart
            data={[
              {
                title: "Red",
                value: redWinProb,
                label: `${Math.round(redWinProb)}%`,
              },
              {
                title: "Blue",
                value: blueWinProb,
                label: `${Math.round(blueWinProb)}%`,
              },
            ]}
            colors={[RED, BLUE]}
          />
        </div>
      </div>
    </div>
  );
};

export default Summary;
