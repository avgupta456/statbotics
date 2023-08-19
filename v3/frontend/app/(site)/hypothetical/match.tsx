import React, { useState } from "react";
import WindowedSelect, { createFilter } from "react-windowed-select";

import { classnames, round } from "../../../utils";
import ImageRow from "../match/[match_id]/imageRow";
import PageMatchTable from "../match/[match_id]/table";
import { TeamYearData } from "../types";

const Select = ({
  label,
  value,
  setValue,
  options,
}: {
  label: string;
  value: number;
  setValue: (value: number) => void;
  options: { value: number; label: string; total_epa: number }[];
}) => {
  const currTeam = options.find((x) => x.value === value);
  return (
    <div className="w-full md:w-1/3">
      <WindowedSelect
        instanceId={`team-select-${label}`}
        className="w-full text-sm"
        options={options || []}
        onChange={(x: any) => setValue(x.value)}
        value={currTeam ?? null}
        placeholder="Select a team"
        filterOption={createFilter({ ignoreAccents: false })}
        windowThreshold={100}
      />
      <div className="w-full text-center text-base text-gray-700 mt-2">
        {currTeam ? `${round(currTeam?.total_epa, 1)} EPA` : ""}
      </div>
    </div>
  );
};

const Match = ({ data }: { data: TeamYearData }) => {
  const [red1, setRed1] = useState(0);
  const [red2, setRed2] = useState(0);
  const [red3, setRed3] = useState(0);

  const [blue1, setBlue1] = useState(0);
  const [blue2, setBlue2] = useState(0);
  const [blue3, setBlue3] = useState(0);

  const red1EPA = data.team_years.find((team) => team.num === red1)?.total_epa ?? 0;
  const red2EPA = data.team_years.find((team) => team.num === red2)?.total_epa ?? 0;
  const red3EPA = data.team_years.find((team) => team.num === red3)?.total_epa ?? 0;
  const redEPA = red1EPA + red2EPA + red3EPA;
  const redPred = redEPA * (1 + data?.year?.foul_rate ?? 0);

  const blue1EPA = data.team_years.find((team) => team.num === blue1)?.total_epa ?? 0;
  const blue2EPA = data.team_years.find((team) => team.num === blue2)?.total_epa ?? 0;
  const blue3EPA = data.team_years.find((team) => team.num === blue3)?.total_epa ?? 0;
  const blueEPA = blue1EPA + blue2EPA + blue3EPA;
  const bluePred = blueEPA * (1 + data?.year?.foul_rate ?? 0);

  const predWinner = redPred > bluePred ? "red" : "blue";

  const yearSd = data?.year?.score_sd ?? 0;
  const K = -5 / 8;

  const redWinProb = 100 / (1 + 10 ** ((K * (redEPA - blueEPA)) / yearSd));
  const blueWinProb = 100 - redWinProb;

  const teamOptions = data.team_years
    .sort((a, b) => a.num - b.num)
    .map((team) => ({
      value: team.num,
      label: `${team.num} | ${team.team}`,
      total_epa: team.total_epa,
    }));

  const teamMatches: any = data?.team_years.filter((team) =>
    [red1, red2, red3, blue1, blue2, blue3].includes(team.num)
  );

  teamMatches.push({
    num: 0,
    total_epa: 0,
    auto_epa: 0,
    teleop_epa: 0,
    endgame_epa: 0,
  });

  const matchData: any = {
    match: {
      red: [red1, red2, red3],
      blue: [blue3, blue2, blue1],
      red_epa_pred: redPred,
      blue_epa_pred: bluePred,
    },
    team_matches: teamMatches,
    team_events: teamMatches,
    year: data?.year,
  };

  return (
    <div className="w-full mb-8">
      <div className="w-full lg:w-2/3 xl:w-1/2 mx-auto">
        <div className="bg-red-100 rounded p-2">
          <div className="text-lg mb-2">Red Alliance</div>
          <div className="w-full flex flex-wrap md:flex-nowrap gap-2">
            <Select label="Red 1" value={red1} setValue={setRed1} options={teamOptions} />
            <Select label="Red 2" value={red2} setValue={setRed2} options={teamOptions} />
            <Select label="Red 3" value={red3} setValue={setRed3} options={teamOptions} />
          </div>
        </div>
        <div className="bg-blue-100 rounded mt-4 p-2">
          <div className="text-lg mb-2">Blue Alliance</div>
          <div className="w-full flex flex-wrap md:flex-nowrap gap-2">
            <Select label="Blue 1" value={blue1} setValue={setBlue1} options={teamOptions} />
            <Select label="Blue 2" value={blue2} setValue={setBlue2} options={teamOptions} />
            <Select label="Blue 3" value={blue3} setValue={setBlue3} options={teamOptions} />
          </div>
        </div>
        <div className="w-full flex flex-col md:flex-row justify-center gap-4 md:gap-16 mt-12 mb-4">
          <div className="flex flex-col items-center">
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
            <div className="mt-4 text-xl flex">
              Projected Winner:{" "}
              <p
                className={classnames(
                  "ml-2",
                  predWinner === "red" ? "text-red-500" : "text-blue-500"
                )}
              >
                {predWinner.toUpperCase()}
              </p>
            </div>
            <div className="text-sm text-gray-600 mt-2">
              Includes {Math.round(data?.year?.foul_rate * 100)}% foul rate
            </div>
          </div>
          <div className="h-full w-1 bg-gray-300" />
          <div className="flex flex-col items-center">
            <div className="flex text-3xl">
              {redWinProb > blueWinProb ? (
                <p className="data text-red-500">{Math.round(redWinProb)}%</p>
              ) : (
                <p className="data text-blue-500">{Math.round(blueWinProb)}%</p>
              )}
            </div>
            <div className="mt-4 text-xl flex">Win Probability</div>
          </div>
        </div>
      </div>
      {data?.year?.year >= 2016 && (
        <>
          <div className="h-[2px] bg-gray-300 my-8" />
          <PageMatchTable data={matchData} />
          <div className="my-16" />
          <ImageRow data={matchData} />
        </>
      )}
    </div>
  );
};

export default Match;
