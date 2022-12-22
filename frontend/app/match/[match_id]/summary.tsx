import React from "react";

import PieChart from "../../../components/Pie";
import { RED, BLUE } from "../../../constants";
import { classnames } from "../../../utils";
import { Data } from "./types";

const Summary = ({ data }: { data: Data }) => {
  const winProb = data.match.epa_win_prob;
  const redWinProb = winProb * 100;
  const blueWinProb = (1 - winProb) * 100;

  return (
    <div className="w-full lg:w-1/2 flex flex-row flex-wrap">
      <div className="w-full lg:w-1/2 h-full flex flex-col justify-around">
        <div className="w-full flex flex-col items-center">
          <div className="flex text-3xl">
            <p
              className={classnames(
                "data text-red-500",
                data.match.red_epa_sum > data.match.blue_epa_sum
                  ? "font-bold"
                  : ""
              )}
            >
              {Math.round(data.match.red_epa_sum)}
            </p>
            <p className="mx-2">-</p>
            <p
              className={classnames(
                "data text-blue-500",
                data.match.blue_epa_sum > data.match.red_epa_sum
                  ? "font-bold"
                  : ""
              )}
            >
              {Math.round(data.match.blue_epa_sum)}
            </p>
          </div>
          <div className="mt-4 text-lg flex">
            Projected Winner:{" "}
            <p
              className={classnames(
                "ml-2",
                data.match.epa_winner === "red"
                  ? "text-red-500"
                  : "text-blue-500"
              )}
            >
              {data.match.epa_winner.toUpperCase()}
            </p>
          </div>
        </div>
        <div className="w-full flex flex-col items-center">
          <div className="flex text-3xl">
            <p
              className={classnames(
                "data text-red-500",
                data.match.red_score > data.match.blue_score ? "font-bold" : ""
              )}
            >
              {Math.round(data.match.red_score)}
            </p>
            <p className="mx-2">-</p>
            <p
              className={classnames(
                "data text-blue-500",
                data.match.blue_score > data.match.red_score ? "font-bold" : ""
              )}
            >
              {Math.round(data.match.blue_score)}
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
      <div className="w-full lg:w-1/2 h-full flex flex-col justify-center items-center">
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
        <div className="text-lg">Win Probability</div>
      </div>
    </div>
  );
};

export default Summary;
