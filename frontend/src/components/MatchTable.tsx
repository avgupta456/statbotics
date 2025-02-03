import React from "react";
import { BsPlayCircle } from "react-icons/bs";

import Link from "next/link";

import { CORRECT_COLOR, INCORRECT_COLOR } from "../constants";
import { APIMatch } from "../types/api";
import { classnames, round } from "../utils";
import { compLevelFullNames, formatMatch } from "./utils";

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
  teamNum,
  compLevel,
  match,
  showVideo,
  rawTitle,
  stacked,
  myAlliance,
}: {
  year: number;
  teamNum: number;
  compLevel: string;
  match: APIMatch;
  showVideo: boolean;
  rawTitle: boolean;
  stacked: boolean;
  myAlliance: boolean;
}) => {
  let alliance = match?.alliances?.red?.team_keys.includes(teamNum) ? "red" : "";
  alliance = match?.alliances?.blue?.team_keys.includes(teamNum) ? "blue" : alliance;

  const _winProb = round(match?.pred?.red_win_prob * 100, 0);
  const winProb = _winProb > 50 ? _winProb : 100 - _winProb;
  const correctWinner = match?.result?.winner === match?.pred?.winner;

  const myAllianceWinProb = alliance === match?.pred?.winner ? winProb : 100 - winProb;
  const myAllianceWinner = alliance === match?.result?.winner;

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
        stacked ? "w-2/9" : "w-1/7",
        rawTitle && "text-xs lg:text-sm"
      )}
    >
      {rawTitle
        ? `${match.event} - ${match.comp_level}${
            match.comp_level === "qm" ? "" : match.set_number + "-"
          }${match.match_number}`
        : formatMatch(compLevel, match.match_number, match.set_number)}
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
        {match?.alliances?.red?.team_keys?.map((team) => (
          <Link
            href={`/team/${team}/${year}`}
            className={classnames(
              "w-1/3",
              match?.result?.winner === "red" ? "font-bold" : "font-thin",
              team === teamNum ? "underline" : "",
              "text-blue-600 hover:text-blue-700 cursor-pointer"
            )}
            key={`${match.key}-${team}`}
          >
            {team}
          </Link>
        ))}
      </div>
      <div
        style={{ backgroundColor: lightBlue }}
        className={classnames(
          "flex justify-center items-center",
          stacked ? "w-full h-1/2" : "w-1/2 h-full"
        )}
      >
        {match?.alliances?.blue?.team_keys?.map((team) => (
          <Link
            href={`/team/${team}/${year}`}
            className={classnames(
              "w-1/3",
              match?.result?.winner === "blue" ? "font-bold" : "font-thin",
              team === teamNum ? "underline" : "",
              "text-blue-600 hover:text-blue-700 cursor-pointer"
            )}
            key={`${match.key}-${team}`}
          >
            {team}
          </Link>
        ))}
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
              match?.result?.winner === "red" ? "font-bold" : "font-thin",
              alliance === "red" ? "underline" : ""
            )}
          >
            {match?.result?.red_score}
          </span>
          {year >= 2016 && match?.result?.red_rp_1 > 0.5 && <sup>●</sup>}
          {year >= 2016 && match?.result?.red_rp_2 > 0.5 && <sup>●</sup>}
          {year >= 2025 && match?.result?.red_rp_3 > 0.5 && <sup>●</sup>}
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
              match?.result?.winner === "blue" ? "font-bold" : "font-thin",
              alliance === "blue" ? "underline" : ""
            )}
          >
            {match?.result?.blue_score}
          </span>
          {year >= 2016 && match?.result?.blue_rp_1 > 0.5 && <sup>●</sup>}
          {year >= 2016 && match?.result?.blue_rp_2 > 0.5 && <sup>●</sup>}
          {year >= 2025 && match?.result?.blue_rp_3 > 0.5 && <sup>●</sup>}
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
              match?.pred?.winner === "red" ? "font-bold" : "font-thin",
              alliance === "red" ? "underline" : ""
            )}
          >
            {round(match?.pred?.red_score, 0)}
          </span>
          {year >= 2016 && !match.elim && match?.pred?.red_rp_1 > 0.5 && <sup>●</sup>}
          {year >= 2016 && !match.elim && match?.pred?.red_rp_2 > 0.5 && <sup>●</sup>}
          {year >= 2025 && !match.elim && match?.pred?.red_rp_3 > 0.5 && <sup>●</sup>}
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
              match?.pred?.winner === "blue" ? "font-bold" : "font-thin",
              alliance === "blue" ? "underline" : ""
            )}
          >
            {round(match?.pred?.blue_score, 0)}
          </span>
          {year >= 2016 && !match.elim && match?.pred?.blue_rp_1 > 0.5 && <sup>●</sup>}
          {year >= 2016 && !match.elim && match?.pred?.blue_rp_2 > 0.5 && <sup>●</sup>}
          {year >= 2025 && !match.elim && match?.pred?.blue_rp_3 > 0.5 && <sup>●</sup>}
        </div>
      </div>
      <div className={stacked ? "w-1/9 flex flex-col" : "w-1/7 flex"}>
        <div
          className={classnames(
            "flex justify-center items-center",
            stacked ? "w-full h-1/2" : "w-1/2 h-full border-double border-l-4 border-gray-300 "
          )}
        >
          {myAlliance
            ? match?.pred?.winner === alliance
              ? "Win"
              : "Lose"
            : match?.pred?.winner === "red"
            ? "Red"
            : "Blue"}
        </div>
        <div
          style={{
            backgroundColor:
              match.status === "Completed"
                ? (myAlliance ? myAllianceWinner : correctWinner)
                  ? CORRECT_COLOR
                  : INCORRECT_COLOR
                : "#FFF",
          }}
          className={classnames(
            "flex justify-center items-center",
            stacked ? "w-full h-1/2" : "w-1/2 h-full"
          )}
        >
          {myAlliance ? myAllianceWinProb : winProb}%
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
  showHeaders = true,
  showSubHeaders = true,
  sorted = true,
  showVideo = true,
  rawTitle = false,
  stacked = false,
  myAlliance = true,
}: {
  year: number;
  teamNum: number;
  matches: APIMatch[];
  showHeaders?: boolean;
  showSubHeaders?: boolean;
  sorted?: boolean;
  showVideo?: boolean;
  rawTitle?: boolean;
  stacked?: boolean;
  myAlliance?: boolean;
}) => {
  if (matches.length === 0) {
    return <div className="w-full text-center">Schedule not released yet.</div>;
  }

  const myAllianceActual = teamNum > 0 && myAlliance;

  const compLevels = matches.map((match) => match.comp_level);
  const uniqueCompLevels = compLevels
    .filter((v, i, a) => a.indexOf(v) === i)
    .sort((a, b) => compLevels.indexOf(a) - compLevels.indexOf(b));

  return (
    <div
      className={classnames(
        "flex flex-col border-2 border-gray-300 lg:text-base",
        stacked ? "text-xs md:text-sm min-w-[300px]" : "text-sm min-w-[800px]"
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
      {sorted
        ? uniqueCompLevels.map((compLevel) => (
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
                      teamNum={teamNum}
                      compLevel={compLevel}
                      match={match}
                      showVideo={showVideo}
                      rawTitle={rawTitle}
                      stacked={stacked}
                      myAlliance={myAllianceActual}
                    />
                  );
                })}
            </div>
          ))
        : matches.map((match) => {
            return (
              <MatchRow
                key={match.key}
                year={year}
                teamNum={teamNum}
                compLevel={match.comp_level}
                match={match}
                showVideo={showVideo}
                rawTitle={rawTitle}
                stacked={stacked}
                myAlliance={myAllianceActual}
              />
            );
          })}
    </div>
  );
};

export default MatchTable;
