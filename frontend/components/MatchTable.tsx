import React from "react";

import Link from "next/link";

import { classnames, round } from "../utils";
import { Match } from "./types/api";

const compLevelFullNames = {
  qm: "Qualifications",
  qf: "Quarterfinals",
  sf: "Semifinals",
  f: "Finals",
};

const compLevelShortNames = {
  qm: "Quals",
  qf: "Quarters",
  sf: "Semis",
  f: "Finals",
};

const lightRed = "#FFEEEE";
const lightBlue = "#EEEEFF";
const lightGray = "#F0F0F0";
const lighterGray = "#F8F8F8";

const MatchTable = ({ teamNum, matches }: { teamNum: number; matches: Match[] }) => {
  const compLevels = matches.map((match) => match.comp_level);
  const uniqueCompLevels = compLevels
    .filter((v, i, a) => a.indexOf(v) === i)
    .sort((a, b) => compLevels.indexOf(a) - compLevels.indexOf(b));

  return (
    <div className="w-4/5 mx-auto flex flex-col border-2 border-gray-300">
      <div
        style={{ backgroundColor: lightGray }}
        className="w-full h-8 flex text-center items-center"
      >
        <div className="w-1/6">Match</div>
        <div className="w-1/4">Red Alliance</div>
        <div className="w-1/4">Blue Alliance</div>
        <div className="w-1/6">Scores</div>
        <div className="w-1/6">Predictions</div>
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

              return (
                <div
                  className="w-full h-8 flex text-center"
                  key={`${match.comp_level}-${match.comp_level}-${match.match_number}`}
                >
                  <Link href={`/match/${match.key}`} className="w-1/6">
                    <a className="text-blue-600 hover:text-blue-700 cursor-pointer">
                      {displayMatch}
                    </a>
                  </Link>
                  <div
                    style={{
                      backgroundColor: lightRed,
                    }}
                    className="w-1/4 flex"
                  >
                    {match.red.map((team) => (
                      <Link
                        href={`/team/${team}`}
                        className={classnames(
                          "w-1/3",
                          match.winner === "red" ? "font-bold" : "font-thin",
                          team === teamNum ? "underline" : ""
                        )}
                        key={team}
                      >
                        <a className="text-blue-600 hover:text-blue-700 cursor-pointer">{team}</a>
                      </Link>
                    ))}
                  </div>
                  <div
                    style={{
                      backgroundColor: lightBlue,
                    }}
                    className="w-1/4 flex"
                  >
                    {match.blue.map((team) => (
                      <Link
                        href={`/team/${team}`}
                        className={classnames(
                          "w-1/3",
                          match.winner === "blue" ? "font-bold" : "font-thin",
                          team === teamNum ? "underline" : ""
                        )}
                        key={team}
                      >
                        <a className="text-blue-600 hover:text-blue-700 cursor-pointer">{team}</a>
                      </Link>
                    ))}
                  </div>
                  <div
                    style={{
                      backgroundColor: lightRed,
                    }}
                    className={classnames(
                      "w-1/12",
                      match.winner === "red" ? "font-bold" : "font-thin",
                      match.alliance === "red" ? "underline" : ""
                    )}
                  >
                    {match.red_score}
                  </div>
                  <div
                    style={{
                      backgroundColor: lightBlue,
                    }}
                    className={classnames(
                      "w-1/12",
                      match.winner === "blue" ? "font-bold" : "font-thin",
                      match.alliance === "blue" ? "underline" : ""
                    )}
                  >
                    {match.blue_score}
                  </div>
                  <div
                    style={{
                      backgroundColor: lighterGray,
                    }}
                    className={classnames(
                      "w-1/12 border-double border-l-4 border-gray-300",
                      match.pred_winner === "red" ? "font-bold" : "font-thin",
                      match.alliance === "red" ? "underline" : ""
                    )}
                  >
                    {round(match.red_epa_pred, 0)}
                  </div>
                  <div
                    style={{
                      backgroundColor: lighterGray,
                    }}
                    className={classnames(
                      "w-1/12",
                      match.pred_winner === "blue" ? "font-bold" : "font-thin",
                      match.alliance === "blue" ? "underline" : ""
                    )}
                  >
                    {round(match.blue_epa_pred, 0)}
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
