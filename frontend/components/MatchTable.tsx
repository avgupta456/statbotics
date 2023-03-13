import React from "react";
import { BsPlayCircle } from "react-icons/bs";

import Link from "next/link";

import { CORRECT_COLOR, INCORRECT_COLOR } from "../constants";
import { classnames, round } from "../utils";
import { APIMatch } from "./types/api";
import { compLevelFullNames, formatMatch, formatNumber } from "./utils";

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

const MatchRow = ({
  year,
  foulRate,
  teamNum,
  compLevel,
  match,
  showVideo,
  stacked,
}: {
  year: number;
  foulRate: number;
  teamNum: number;
  compLevel: string;
  match: APIMatch;
  showVideo: boolean;
  stacked: boolean;
}) => {
  let alliance = match.red.includes(teamNum) ? "red" : "";
  alliance = match.blue.includes(teamNum) ? "blue" : alliance;

  const _winProb = round(match.epa_win_prob * 100, 0);
  const winProb = _winProb > 50 ? _winProb : 100 - _winProb;
  const correctWinner = match.winner === match.pred_winner;

  const Video = () => (
    <div className="w-16 h-full flex justify-center items-center border-r border-b border-gray-300">
      {match.video && (
        <Link
          href={`/match/${match.key}`}
          // href={`https://www.youtube.com/watch?v=${match.video}`}
          // rel="noreferrer noopener"
          // target="_blank"
        >
          <BsPlayCircle className="text-blue-600 hover:text-blue-700 cursor-pointer" />
        </Link>
      )}
    </div>
  );

  const Title = () => (
    <Link
      href={`/match/${match.key}`}
      className={classnames(
        "h-full flex justify-center items-center text-blue-600 hover:text-blue-700 cursor-pointer border-r border-b border-gray-300",
        stacked ? "w-2/9" : "w-1/7"
      )}
    >
      {formatMatch(compLevel, match.match_number, match.set_number)}
    </Link>
  );

  const Alliances = () => (
    <div className={stacked ? "w-1/3 flex flex-col" : "w-3/7 flex"}>
      <div
        style={{ backgroundColor: lightRed }}
        className={classnames(
          "flex justify-center items-center",
          stacked ? "w-full h-1/2" : "w-1/2 h-full"
        )}
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
        className={classnames(
          "flex justify-center items-center",
          stacked ? "w-full h-1/2" : "w-1/2 h-full"
        )}
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
    </div>
  );

  const Scores = () =>
    match.status === "Completed" ? (
      <>
        <div
          style={{ backgroundColor: lightRed }}
          className={classnames(
            "h-full flex justify-center items-center",
            stacked ? "w-1/9" : "w-1/14"
          )}
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
          className={classnames(
            "h-full flex justify-center items-center",
            stacked ? "w-1/9" : "w-1/14"
          )}
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
      <div
        className={classnames(
          "flex justify-center items-center text-xs lg:text-base",
          stacked ? "w-2/9" : "w-1/7"
        )}
      >
        {match.predicted_time ? (
          <span className="italic">{timestampToString(match.predicted_time)}</span>
        ) : (
          <span className="font-thin">-</span>
        )}
      </div>
    );

  const ScorePreds = () => (
    <>
      <div className={stacked ? "w-1/9 flex flex-col" : "w-1/7 flex"}>
        <div
          className={classnames(
            "border-double border-l-4 border-gray-300 flex justify-center items-center",
            stacked ? "w-full h-1/2" : "w-1/2 h-full"
          )}
          style={{ backgroundColor: lightRed }}
        >
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
        <div
          className={classnames(
            "border-double border-l-4 border-gray-300 flex justify-center items-center",
            stacked ? "w-full h-1/2" : "w-1/2 h-full"
          )}
          style={{ backgroundColor: lightBlue }}
        >
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
      </div>
      <div className={stacked ? "w-1/9 flex flex-col" : "w-1/7 flex"}>
        <div
          className={classnames(
            "flex justify-center items-center",
            stacked ? "w-full h-1/2" : "w-1/2 h-full border-double border-l-4 border-gray-300 "
          )}
        >
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
          className={classnames(
            "flex justify-center items-center",
            stacked ? "w-full h-1/2" : "w-1/2 h-full"
          )}
        >
          {winProb}%
        </div>
      </div>
    </>
  );

  return (
    <div
      className={classnames("w-full flex text-center", stacked ? "h-16" : "h-8")}
      key={`${match.comp_level}-${match.set_number}-${match.match_number}`}
    >
      {showVideo && <Video />}
      <div className="flex-grow flex">
        <Title />
        <Alliances />
        <Scores />
        <ScorePreds />
      </div>
    </div>
  );
};

const MatchTable = ({
  year,
  teamNum,
  matches,
  foulRate,
  showHeaders = true,
  showSubHeaders = true,
  showVideo = true,
  stacked = false,
}: {
  year: number;
  teamNum: number;
  matches: APIMatch[];
  foulRate: number;
  showHeaders?: boolean;
  showSubHeaders?: boolean;
  showVideo?: boolean;
  stacked?: boolean;
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
      className={classnames(
        "flex flex-col border-2 border-gray-300 text-xs md:text-sm lg:text-base",
        stacked ? "min-w-[300px]" : "min-w-[720px]"
      )}
      key={`match-table-${matches?.[0]?.key ?? ""}`}
    >
      {showHeaders && (
        <div
          style={{ backgroundColor: lightGray }}
          className="w-full h-8 flex text-center items-center"
        >
          {showVideo && <div className="w-16">Video</div>}
          <div className="flex-grow flex">
            {stacked ? (
              <>
                <div className="w-2/9">Match</div>
                <div className="w-1/3">Alliances</div>
                <div className="w-2/9">Time</div>
                <div className="w-2/9">Preds</div>
              </>
            ) : (
              <>
                <div className="w-1/7">Match</div>
                <div className="w-3/14">Red Alliance</div>
                <div className="w-3/14">Blue Alliance</div>
                <div className="w-1/7">Scores</div>
                <div className="w-1/7">Score Preds</div>
                <div className="w-1/7">Win Pred</div>
              </>
            )}
          </div>
        </div>
      )}
      {uniqueCompLevels.map((compLevel) => (
        <div key={`section-${compLevel}`}>
          {showSubHeaders && (
            <div
              style={{ backgroundColor: lightGray }}
              className={classnames(
                "w-full text-center border-t-2 border-b-2 border-gray-300",
                stacked ? "h-16" : "h-8"
              )}
              key={`header-${compLevel}`}
            >
              {compLevelFullNames[compLevel]}
            </div>
          )}
          {matches
            .filter((match) => match.comp_level === compLevel)
            .map((match) => {
              return (
                <MatchRow
                  key={match.key}
                  year={year}
                  foulRate={foulRate}
                  teamNum={teamNum}
                  compLevel={compLevel}
                  match={match}
                  showVideo={showVideo}
                  stacked={stacked}
                />
              );
            })}
        </div>
      ))}
    </div>
  );
};

export default MatchTable;
