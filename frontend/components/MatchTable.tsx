import React from "react";

import Link from "next/link";

import { CORRECT_COLOR, INCORRECT_COLOR } from "../constants";
import { classnames, round } from "../utils";
import { APIMatch } from "./types/api";
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

const timestampToString = (timestamp: number) => {
  const date = new Date(timestamp * 1000);
  const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const dayOfWeek = daysOfWeek[date.getDay()];
  const options: any = { hour: "numeric", minute: "numeric", hour12: true };
  const _formattedDate = `${dayOfWeek}, ${date.toLocaleString(undefined, options)}`;
  const formattedDate = _formattedDate === "Wed, 6:59 PM" ? "-" : _formattedDate;
  return formattedDate;
};

const MatchTable = ({
  year,
  teamNum,
  matches,
  foulRate,
}: {
  year: number;
  teamNum: number;
  matches: APIMatch[];
  foulRate: number;
}) => {
  if (matches.length === 0) {
    return <div className="w-full text-center">Schedule not released yet.</div>;
  }

  const compLevels = matches.map((match) => match.comp_level);
  const uniqueCompLevels = compLevels
    .filter((v, i, a) => a.indexOf(v) === i)
    .sort((a, b) => compLevels.indexOf(a) - compLevels.indexOf(b));

  return (
    <div
      className="min-w-[667px] flex flex-col border-2 border-gray-300"
      key={`match-table-${matches?.[0]?.key ?? ""}`}
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

              let alliance = match.red.includes(teamNum) ? "red" : "";
              alliance = match.blue.includes(teamNum) ? "blue" : alliance;

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
                          href={`/team/${team}/${year}`}
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
                          href={`/team/${team}/${year}`}
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
                  {match.status === "Completed" ? (
                    <>
                      <div
                        style={{ backgroundColor: lightRed }}
                        className="w-1/14 flex justify-center items-center"
                      >
                        <span
                          className={classnames(
                            match.winner === "red" ? "font-bold" : "font-thin",
                            alliance === "red" ? "underline" : ""
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
                            alliance === "blue" ? "underline" : ""
                          )}
                        >
                          {match.blue_score}
                        </span>
                        {year >= 2016 && match.blue_rp_1 > 0.5 && <sup>●</sup>}
                        {year >= 2016 && match.blue_rp_2 > 0.5 && <sup>●</sup>}
                      </div>
                    </>
                  ) : (
                    <div className="w-1/7 flex justify-center items-center text-xs lg:text-base">
                      {match.predicted_time ? (
                        <span className="italic">{timestampToString(match.predicted_time)}</span>
                      ) : (
                        <span className="font-thin">-</span>
                      )}
                    </div>
                  )}
                  <div className="w-1/14 border-double border-l-4 border-gray-300 flex justify-center items-center">
                    <span
                      className={classnames(
                        match.pred_winner === "red" ? "font-bold" : "font-thin",
                        alliance === "red" ? "underline" : ""
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
                        alliance === "blue" ? "underline" : ""
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
                    style={{
                      backgroundColor:
                        match.status === "Completed"
                          ? correctWinner
                            ? CORRECT_COLOR
                            : INCORRECT_COLOR
                          : "#FFF",
                    }}
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
