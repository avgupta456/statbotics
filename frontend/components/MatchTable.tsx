import React from "react";

import Link from "next/link";

import { CORRECT_COLOR, INCORRECT_COLOR } from "../constants";
import { classnames, round } from "../utils";
import { Match } from "./types/api";

const compLevelFullNames = {
  qm: "Qualifications",
  ef: "Eighth Finals",
  qf: "Quarterfinals",
  sf: "Semifinals",
  f: "Finals",
};

const compLevelShortNames = {
  qm: "Quals",
  ef: "Eighths",
  qf: "Quarters",
  sf: "Semis",
  f: "Finals",
};

const lightRed = "#FFEEEE";
const lightBlue = "#EEEEFF";
const lightGray = "#F0F0F0";

const MatchTable = ({
  year,
  teamNum,
  matches,
  foulRate,
}: {
  year: number;
  teamNum: number;
  matches: Match[];
  foulRate: number;
}) => {
  const compLevels = matches.map((match) => match.comp_level);
  const uniqueCompLevels = compLevels
    .filter((v, i, a) => a.indexOf(v) === i)
    .sort((a, b) => compLevels.indexOf(a) - compLevels.indexOf(b));

  return (
    <div className="w-full flex flex-col border-2 border-gray-300">
      <div
        style={{ backgroundColor: lightGray }}
        className="w-full h-8 flex text-center items-center"
      >
        <div className="w-2/13">Match</div>
        <div className="w-3/13">Red Alliance</div>
        <div className="w-3/13">Blue Alliance</div>
        <div className="w-2/13">Scores</div>
        <div className="w-3/13">Predictions</div>
      </div>
      {uniqueCompLevels.map((compLevel) => (
        <>
          <div
            style={{ backgroundColor: lightGray }}
            className="w-full h-8 text-center border-t-2 border-b-2 border-gray-300"
            key={compLevel}
          >
            {compLevelFullNames[compLevel]}
          </div>
          {matches
            .filter((match) => match.comp_level === compLevel)
            .map((match) => {
              let displayMatch = `${compLevelShortNames[compLevel]} ${match.match_number}`;
              if (compLevel === "qf" || compLevel === "sf") {
                displayMatch = `${compLevelShortNames[compLevel]} ${match.set_number}-${match.match_number}`;
              }

              const _winProb =
                match.alliance === "red" ? match.epa_win_prob : 1 - match.epa_win_prob;
              const winProb = round(_winProb * 100, 0);

              const correctWinner = match.winner === match.pred_winner;

              return (
                <div
                  className="w-full h-8 flex text-center"
                  key={`${match.comp_level}-${match.comp_level}-${match.match_number}`}
                >
                  <Link
                    href={`/match/${match.key}`}
                    className="w-2/13 flex justify-center items-center text-blue-600 hover:text-blue-700 cursor-pointer"
                  >
                    {displayMatch}
                  </Link>
                  <div
                    style={{
                      backgroundColor: lightRed,
                    }}
                    className="w-3/13 flex justify-center items-center"
                  >
                    {match.red.map((team) => (
                      <Link
                        href={`/team/${team}`}
                        className={classnames(
                          "w-1/3",
                          match.winner === "red" ? "font-bold" : "font-thin",
                          team === teamNum ? "underline" : "",
                          "text-blue-600 hover:text-blue-700 cursor-pointer"
                        )}
                        key={team}
                      >
                        {team}
                      </Link>
                    ))}
                  </div>
                  <div
                    style={{
                      backgroundColor: lightBlue,
                    }}
                    className="w-3/13 flex justify-center items-center"
                  >
                    {match.blue.map((team) => (
                      <Link
                        href={`/team/${team}`}
                        className={classnames(
                          "w-1/3",
                          match.winner === "blue" ? "font-bold" : "font-thin",
                          team === teamNum ? "underline" : "",
                          "text-blue-600 hover:text-blue-700 cursor-pointer"
                        )}
                        key={team}
                      >
                        {team}
                      </Link>
                    ))}
                  </div>
                  <div
                    style={{
                      backgroundColor: lightRed,
                    }}
                    className="w-1/13 flex justify-center items-center"
                  >
                    <span
                      className={classnames(
                        match.winner === "red" ? "font-bold" : "font-thin",
                        match.alliance === "red" ? "underline" : ""
                      )}
                    >
                      {match.red_score}
                    </span>
                    {year >= 2016 && match.red_rp_1 > 0.5 && <sup>●</sup>}
                    {year >= 2016 && match.red_rp_2 > 0.5 && <sup>●</sup>}
                  </div>
                  <div
                    style={{
                      backgroundColor: lightBlue,
                    }}
                    className="w-1/13 flex justify-center items-center"
                  >
                    <span
                      className={classnames(
                        match.winner === "blue" ? "font-bold" : "font-thin",
                        match.alliance === "blue" ? "underline" : ""
                      )}
                    >
                      {match.blue_score}
                    </span>
                    {year >= 2016 && match.blue_rp_1 > 0.5 && <sup>●</sup>}
                    {year >= 2016 && match.blue_rp_2 > 0.5 && <sup>●</sup>}
                  </div>
                  <div className="w-1/13 border-double border-l-4 border-gray-300 flex justify-center items-center">
                    <span
                      className={classnames(
                        match.pred_winner === "red" ? "font-bold" : "font-thin",
                        match.alliance === "red" ? "underline" : ""
                      )}
                    >
                      {round((1 + foulRate) * match.red_epa_pred, 0)}
                    </span>
                    {year >= 2016 && !match.playoff && match.red_rp_1_pred > 0.5 && <sup>●</sup>}
                    {year >= 2016 && !match.playoff && match.red_rp_2_pred > 0.5 && <sup>●</sup>}
                  </div>
                  <div className="w-1/13 flex justify-center items-center">
                    <span
                      className={classnames(
                        match.pred_winner === "blue" ? "font-bold" : "font-thin",
                        match.alliance === "blue" ? "underline" : ""
                      )}
                    >
                      {round((1 + foulRate) * match.blue_epa_pred, 0)}
                    </span>
                    {year >= 2016 && !match.playoff && match.blue_rp_1_pred > 0.5 && <sup>●</sup>}
                    {year >= 2016 && !match.playoff && match.blue_rp_2_pred > 0.5 && <sup>●</sup>}
                  </div>
                  <div
                    style={{ backgroundColor: correctWinner ? CORRECT_COLOR : INCORRECT_COLOR }}
                    className="w-1/13 flex justify-center items-center"
                  >
                    {winProb}%
                  </div>
                </div>
              );
            })}
        </>
      ))}
    </div>
  );
};

export default MatchTable;
