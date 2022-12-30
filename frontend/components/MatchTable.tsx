import React from "react";

import Link from "next/link";

import { classnames } from "../utils";
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

const MatchTable = ({ teamNum, matches }: { teamNum: number; matches: Match[] }) => {
  const compLevels = matches.map((match) => match.comp_level);
  // get list of unique comp levels, sorted by first appearance in matches
  const uniqueCompLevels = [...new Set(compLevels)].sort(
    (a, b) => compLevels.indexOf(a) - compLevels.indexOf(b)
  );

  return (
    <div className="w-3/4 mx-auto flex flex-col border-2 border-gray-300">
      <div
        style={{ backgroundColor: lightGray }}
        className="w-full h-8 flex text-center items-center"
      >
        <div className="w-1/5">Match</div>
        <div className="w-3/10">Red Alliance</div>
        <div className="w-3/10">Blue Alliance</div>
        <div className="w-1/5">Scores</div>
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
              const displayMatch = `${compLevelShortNames[compLevel]} ${match.match_number}`;
              return (
                <div
                  className="w-full h-8 flex text-center"
                  key={`${match.comp_level}-${match.comp_level}-${match.match_number}`}
                >
                  <Link href={`/match/${match.key}`} className="w-1/5">
                    <a className="text-blue-600 hover:text-blue-700 cursor-pointer">
                      {displayMatch}
                    </a>
                  </Link>
                  <div
                    style={{
                      backgroundColor: lightRed,
                    }}
                    className="w-3/10 flex"
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
                    className="w-3/10 flex"
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
                      "w-1/10",
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
                      "w-1/10",
                      match.winner === "blue" ? "font-bold" : "font-thin",
                      match.alliance === "blue" ? "underline" : ""
                    )}
                  >
                    {match.blue_score}
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
