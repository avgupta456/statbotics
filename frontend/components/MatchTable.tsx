import React from "react";

import Link from "next/link";

import { CORRECT_COLOR, INCORRECT_COLOR } from "../constants";
import { classnames, round } from "../utils";
import { Match } from "./types/api";
import { formatNumber } from "./utils";

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
    <div
      className="w-full flex flex-col border-2 border-gray-300"
      key={`match-table-${matches?.[0].key ?? ""}`}
    >
      <div
        style={{ backgroundColor: lightGray }}
        className="w-full h-8 flex text-center items-center"
      >
        <div className="w-1/7">Match</div>
        <div className="w-3/14">Red Alliance</div>
        <div className="w-3/14">Blue Alliance</div>
        <div className="w-1/7">Scores</div>
        <div className="w-1/7">Score Preds</div>
        <div className="w-1/7">Win Pred</div>
      </div>
      {uniqueCompLevels.map((compLevel) => (
        <div key={`section-${compLevel}`}>
          <div
            style={{ backgroundColor: lightGray }}
            className="w-full h-8 text-center border-t-2 border-b-2 border-gray-300"
            key={`header-${compLevel}`}
          >
            {compLevelFullNames[compLevel]}
          </div>
          {matches
            .filter((match) => match.comp_level === compLevel)
            .map((match) => {
              let displayMatch = `${compLevelShortNames[compLevel]} ${match.match_number}`;
              if (compLevel !== "qm") {
                displayMatch = `${compLevelShortNames[compLevel]} ${match.set_number}-${match.match_number}`;
              }

              const _winProb = round(match.epa_win_prob * 100, 0);
              const winProb = _winProb > 50 ? _winProb : 100 - _winProb;

              const correctWinner = match.winner === match.pred_winner;

              return (
                <div
                  className="w-full h-8 flex text-center"
                  key={`${match.comp_level}-${match.set_number}-${match.match_number}`}
                >
                  <Link
                    href={`/match/${match.key}`}
                    className="w-1/7 flex justify-center items-center text-blue-600 hover:text-blue-700 cursor-pointer"
                  >
                    {displayMatch}
                  </Link>
                  <div
                    style={{ backgroundColor: lightRed }}
                    className="w-3/14 flex justify-center items-center"
                  >
                    {match.red.map((team) =>
                      team > 100000 ? (
                        <div className="w-1/3" key={`${match.key}-${team}`}>
                          {formatNumber(team)}
                        </div>
                      ) : (
                        <Link
                          href={`/team/${team}`}
                          className={classnames(
                            "w-1/3",
                            match.winner === "red" ? "font-bold" : "font-thin",
                            team === teamNum ? "underline" : "",
                            "text-blue-600 hover:text-blue-700 cursor-pointer"
                          )}
                          key={`${match.key}-${team}`}
                        >
                          {team}
                        </Link>
                      )
                    )}
                  </div>
                  <div
                    style={{ backgroundColor: lightBlue }}
                    className="w-3/14 flex justify-center items-center"
                  >
                    {match.blue.map((team) =>
                      team > 100000 ? (
                        <div className="w-1/3" key={`${match.key}-${team}`}>
                          {formatNumber(team)}
                        </div>
                      ) : (
                        <Link
                          href={`/team/${team}`}
                          className={classnames(
                            "w-1/3",
                            match.winner === "blue" ? "font-bold" : "font-thin",
                            team === teamNum ? "underline" : "",
                            "text-blue-600 hover:text-blue-700 cursor-pointer"
                          )}
                          key={`${match.key}-${team}`}
                        >
                          {team}
                        </Link>
                      )
                    )}
                  </div>
                  <div
                    style={{ backgroundColor: lightRed }}
                    className="w-1/14 flex justify-center items-center"
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
                    style={{ backgroundColor: lightBlue }}
                    className="w-1/14 flex justify-center items-center"
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
                  <div className="w-1/14 border-double border-l-4 border-gray-300 flex justify-center items-center">
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
                  <div className="w-1/14 flex justify-center items-center">
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
                  <div className="w-1/14 border-double border-l-4 border-gray-300 flex justify-center items-center">
                    {match.pred_winner === "red" ? "Red" : "Blue"}
                  </div>
                  <div
                    style={{ backgroundColor: correctWinner ? CORRECT_COLOR : INCORRECT_COLOR }}
                    className="w-1/14 flex justify-center items-center"
                  >
                    {winProb}%
                  </div>
                </div>
              );
            })}
        </div>
      ))}
    </div>
  );
};

export default MatchTable;
