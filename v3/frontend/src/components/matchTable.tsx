/* eslint-disable no-nested-ternary */
import React from "react";
import { BsPlayCircle } from "react-icons/bs";

import Link from "next/link";

import { APIMatch } from "../types/api";
import { CORRECT_COLOR, INCORRECT_COLOR } from "../utils/constants";
import { COMP_LEVEL_FULL_NAMES, formatMatch } from "../utils/formatting";
import { classnames, round } from "../utils/utils";

const timestampToString = (timestamp: number) => {
  const date = new Date(timestamp * 1000);
  const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const dayOfWeek = daysOfWeek[date.getDay()];
  const options: any = { hour: "numeric", minute: "numeric", hour12: true };
  const tempDate = `${dayOfWeek}, ${date.toLocaleString(undefined, options)}`;
  const formattedDate = tempDate === "Wed, 6:59 PM" ? "-" : tempDate;
  return formattedDate;
};

function Video({ match }: { match: APIMatch }) {
  return (
    <div className="flex h-full w-16 items-center justify-center border-b border-r border-gray-300 dark:border-gray-700">
      {match.video && (
        <Link
          href={`/match/${match.key}`}
          // href={`https://www.youtube.com/watch?v=${match.video}`}
          // rel="noreferrer noopener"
          // target="_blank"
        >
          <BsPlayCircle className="cursor-pointer text-blue-600 hover:text-blue-700" />
        </Link>
      )}
    </div>
  );
}

function Title({
  match,
  stacked,
  rawTitle,
  compLevel,
}: {
  match: APIMatch;
  stacked: boolean;
  rawTitle: boolean;
  compLevel: string;
}) {
  return (
    <Link
      href={`/match/${match.key}`}
      className={classnames(
        "flex h-full cursor-pointer items-center justify-center border-b border-r border-gray-300 text-blue-600 hover:text-blue-700 dark:border-gray-700",
        stacked ? "w-2/9" : "w-1/7",
        rawTitle ? "text-xs lg:text-sm" : "",
      )}
    >
      {rawTitle
        ? `${match.event} - ${match.comp_level}${
            match.comp_level === "qm" ? "" : `${match.set_number}-`
          }${match.match_number}`
        : formatMatch(compLevel, match.match_number, match.set_number)}
    </Link>
  );
}

function Alliances({
  match,
  stacked,
  teamNum,
  year,
}: {
  match: APIMatch;
  stacked: boolean;
  teamNum: string;
  year: number;
}) {
  return (
    <div className={stacked ? "flex w-1/3 flex-col" : "w-3/7 flex"}>
      <div
        className={classnames(
          "bg-matchRed dark:bg-matchRed-dark flex items-center justify-center",
          stacked ? "h-1/2 w-full" : "h-full w-1/2",
        )}
      >
        {match.alliances.red.team_keys.map((team) => (
          <Link
            href={`/team/${team}/${year}`}
            className={classnames(
              "w-1/3",
              match.result.winner === "red" ? "font-bold" : "font-thin",
              team === teamNum ? "underline" : "",
              "cursor-pointer text-blue-600 hover:text-blue-700",
            )}
            key={`${match.key}-${team}`}
          >
            {team}
          </Link>
        ))}
      </div>
      <div
        className={classnames(
          "bg-matchBlue dark:bg-matchBlue-dark flex items-center justify-center",
          stacked ? "h-1/2 w-full" : "h-full w-1/2",
        )}
      >
        {match.alliances.blue.team_keys.map((team) => (
          <Link
            href={`/team/${team}/${year}`}
            className={classnames(
              "w-1/3",
              match.result.winner === "blue" ? "font-bold" : "font-thin",
              team === teamNum ? "underline" : "",
              "cursor-pointer text-blue-600 hover:text-blue-700",
            )}
            key={`${match.key}-${team}`}
          >
            {team}
          </Link>
        ))}
      </div>
    </div>
  );
}

function Scores({
  match,
  stacked,
  alliance,
  year,
}: {
  match: APIMatch;
  stacked: boolean;
  alliance: string;
  year: number;
}) {
  return match.status === "Completed" ? (
    <>
      <div
        className={classnames(
          "bg-matchRed dark:bg-matchRed-dark flex h-full items-center justify-center",
          stacked ? "w-1/9" : "w-1/14",
        )}
      >
        <span
          className={classnames(
            "text-black",
            match.result.winner === "red" ? "font-bold" : "font-thin",
            alliance === "red" ? "underline" : "",
          )}
        >
          {match.result.red_score}
        </span>
        {year >= 2016 && match.result.red_rp_1 > 0.5 && <sup>●</sup>}
        {year >= 2016 && match.result.red_rp_2 > 0.5 && <sup>●</sup>}
      </div>
      <div
        className={classnames(
          "bg-matchBlue bg-matchBlue-dark flex h-full items-center justify-center",
          stacked ? "w-1/9" : "w-1/14",
        )}
      >
        <span
          className={classnames(
            "text-black",
            match.result.winner === "blue" ? "font-bold" : "font-thin",
            alliance === "blue" ? "underline" : "",
          )}
        >
          {match.result.blue_score}
        </span>
        {year >= 2016 && match.result.blue_rp_1 > 0.5 && <sup>●</sup>}
        {year >= 2016 && match.result.blue_rp_2 > 0.5 && <sup>●</sup>}
      </div>
    </>
  ) : (
    <div
      className={classnames(
        "flex items-center justify-center text-xs lg:text-base",
        stacked ? "w-2/9" : "w-1/7",
      )}
    >
      {match.predicted_time ? (
        <span className="italic">{timestampToString(match.predicted_time)}</span>
      ) : (
        <span className="font-thin">-</span>
      )}
    </div>
  );
}

function ScorePreds({
  match,
  alliance,
  myAlliance,
  stacked,
  year,
}: {
  match: APIMatch;
  alliance: string;
  myAlliance: boolean;
  stacked: boolean;
  year: number;
}) {
  const rawWinProb = round(match.pred.red_win_prob * 100, 0);
  const winProb = rawWinProb > 50 ? rawWinProb : 100 - rawWinProb;
  const correctWinner = match.result.winner === match.pred.winner;

  const myAllianceWinProb = alliance === match.pred.winner ? winProb : 100 - winProb;
  const myAllianceWinner = alliance === match.result.winner;

  return (
    <>
      <div className={stacked ? "w-1/9 flex flex-col" : "w-1/7 flex"}>
        <div
          className={classnames(
            "bg-matchRed dark:bg-matchRed-dark flex items-center justify-center border-l-4 border-double border-gray-300 dark:border-gray-700",
            stacked ? "h-1/2 w-full" : "h-full w-1/2",
          )}
        >
          <span
            className={classnames(
              "text-black",
              match.pred.winner === "red" ? "font-bold" : "font-thin",
              alliance === "red" ? "underline" : "",
            )}
          >
            {round(match.pred.red_score, 0)}
          </span>
          {year >= 2016 && !match.elim && match.pred.red_rp_1 > 0.5 && <sup>●</sup>}
          {year >= 2016 && !match.elim && match.pred.red_rp_2 > 0.5 && <sup>●</sup>}
        </div>
        <div
          className={classnames(
            "bg-matchBlue dark:bg-matchBlue-dark flex items-center justify-center border-l-4 border-double border-gray-300 dark:border-gray-700",
            stacked ? "h-1/2 w-full" : "h-full w-1/2",
          )}
        >
          <span
            className={classnames(
              "text-black",
              match.pred.winner === "blue" ? "font-bold" : "font-thin",
              alliance === "blue" ? "underline" : "",
            )}
          >
            {round(match.pred.blue_score, 0)}
          </span>
          {year >= 2016 && !match.elim && match.pred.blue_rp_1 > 0.5 && <sup>●</sup>}
          {year >= 2016 && !match.elim && match.pred.blue_rp_2 > 0.5 && <sup>●</sup>}
        </div>
      </div>
      <div className={stacked ? "w-1/9 flex flex-col" : "w-1/7 flex"}>
        <div
          className={classnames(
            "flex items-center justify-center",
            stacked
              ? "h-1/2 w-full"
              : "h-full w-1/2 border-l-4 border-double border-gray-300 dark:border-gray-700",
          )}
        >
          {myAlliance
            ? match.pred.winner === alliance
              ? "Win"
              : "Lose"
            : match.pred.winner === "red"
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
            "flex items-center justify-center text-black",
            stacked ? "h-1/2 w-full" : "h-full w-1/2",
          )}
        >
          {myAlliance ? myAllianceWinProb : winProb}%
        </div>
      </div>
    </>
  );
}

function MatchRow({
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
  teamNum: string;
  compLevel: string;
  match: APIMatch;
  showVideo: boolean;
  rawTitle: boolean;
  stacked: boolean;
  myAlliance: boolean;
}) {
  let alliance = match.alliances.red.team_keys.includes(teamNum) ? "red" : "";
  alliance = match.alliances.blue.team_keys.includes(teamNum) ? "blue" : alliance;

  return (
    <div
      className={classnames("flex w-full text-center", stacked ? "h-16" : "h-8")}
      key={`${match.comp_level}-${match.set_number}-${match.match_number}`}
    >
      {showVideo && <Video match={match} />}
      <div className="flex flex-grow">
        <Title match={match} stacked={stacked} rawTitle={rawTitle} compLevel={compLevel} />
        <Alliances match={match} stacked={stacked} teamNum={teamNum} year={year} />
        <Scores match={match} stacked={stacked} alliance={alliance} year={year} />
        <ScorePreds
          match={match}
          alliance={alliance}
          myAlliance={myAlliance}
          stacked={stacked}
          year={year}
        />
      </div>
    </div>
  );
}

function MatchTable({
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
  teamNum: string;
  matches: APIMatch[];
  showHeaders?: boolean;
  showSubHeaders?: boolean;
  sorted?: boolean;
  showVideo?: boolean;
  rawTitle?: boolean;
  stacked?: boolean;
  myAlliance?: boolean;
}) {
  if (matches.length === 0) {
    return <div className="w-full text-center">Schedule not released yet.</div>;
  }

  const myAllianceActual = teamNum.length > 0 && myAlliance;

  const compLevels = matches.map((match) => match.comp_level);
  const uniqueCompLevels = compLevels
    .filter((v, i, a) => a.indexOf(v) === i)
    .sort((a, b) => compLevels.indexOf(a) - compLevels.indexOf(b));

  return (
    <div
      className={classnames(
        "flex flex-col border-2 border-gray-300 lg:text-base dark:border-gray-700",
        stacked ? "min-w-[300px] text-xs md:text-sm" : "min-w-[800px] text-sm",
      )}
      key={`match-table-${matches?.[0]?.key ?? ""}`}
    >
      {showHeaders && (
        <div className="flex h-8 w-full items-center bg-zinc-100 text-center dark:bg-zinc-700">
          {showVideo && <div className="w-16">Video</div>}
          <div className="flex flex-grow">
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
                  className={classnames(
                    "w-full border-b-2 border-t-2 border-gray-300 bg-zinc-100 text-center dark:border-gray-700 dark:bg-zinc-700",
                    stacked ? "h-16" : "h-8",
                  )}
                  key={`header-${compLevel}`}
                >
                  {COMP_LEVEL_FULL_NAMES[compLevel]}
                </div>
              )}
              {matches
                .filter((match) => match.comp_level === compLevel)
                .map((match) => (
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
                ))}
            </div>
          ))
        : matches.map((match) => (
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
          ))}
    </div>
  );
}

export default MatchTable;
