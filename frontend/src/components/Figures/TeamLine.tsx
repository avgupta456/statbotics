"use client";

import React, { useState } from "react";
import { TbArrowsJoin, TbArrowsSplit } from "react-icons/tb";
import Select from "react-select";

import { RP_KEYS, RP_NAMES } from "../../constants";
import { APITeamMatch, APITeamYear } from "../../types/api";
import LineChart from "./Line";

const TeamLineChart = ({
  teamNum,
  year,
  teamYear,
  data,
}: {
  teamNum: string;
  year: number;
  teamYear: APITeamYear;
  data: APITeamMatch[];
}) => {
  const yAxisOptions = [
    {
      matchAccessor: (teamMatch: APITeamMatch) => teamMatch?.epa?.breakdown?.total_points,
      yearAccessor: (teamYear: APITeamYear) => teamYear?.epa?.breakdown?.total_points?.mean,
      value: "total_epa",
      label: "Total EPA",
    },
    ...(year >= 2016
      ? [
          {
            matchAccessor: (teamMatch: APITeamMatch) => teamMatch?.epa?.breakdown?.auto_points,
            yearAccessor: (teamYear: APITeamYear) => teamYear?.epa?.breakdown?.auto_points?.mean,
            value: "auto_epa",
            label: "Auto EPA",
          },
          {
            matchAccessor: (teamMatch: APITeamMatch) => teamMatch?.epa?.breakdown?.teleop_points,
            yearAccessor: (teamYear: APITeamYear) => teamYear?.epa?.breakdown?.teleop_points?.mean,
            value: "teleop_epa",
            label: "Teleop EPA",
          },
          {
            matchAccessor: (teamMatch: APITeamMatch) => teamMatch?.epa?.breakdown?.endgame_points,
            yearAccessor: (teamYear: APITeamYear) => teamYear?.epa?.breakdown?.endgame_points?.mean,
            value: "endgame_epa",
            label: "Endgame EPA",
          },
          {
            matchAccessor: (teamMatch: APITeamMatch) =>
              teamMatch?.epa?.breakdown?.[RP_KEYS[year][0]],
            value: "rp_1_epa",
            label: `${RP_NAMES[year][0]} EPA`,
          },
          {
            matchAccessor: (teamMatch: APITeamMatch) =>
              teamMatch?.epa?.breakdown?.[RP_KEYS[year][1]],
            value: "rp_2_epa",
            label: `${RP_NAMES[year][1]} EPA`,
          },
        ]
      : []),
  ];

  const [yAxis, setYAxis] = useState(yAxisOptions[0]);
  const [splitEvents, setSplitEvents] = useState(false);

  // VARIABLES
  let filteredData = data.filter((teamMatch: APITeamMatch) => teamMatch.status === "Completed");

  let arr = filteredData.map((teamMatch: APITeamMatch, i: number) => ({
    x: i,
    event: teamMatch.match.split("_")[0],
    label: data[i - 1]?.match || "Start",
    y: yAxis.matchAccessor(teamMatch),
  }));

  const lastEPA = yAxis.yearAccessor(teamYear);
  const lastEvent = filteredData[filteredData.length - 1]?.match.split("_")[0];
  arr.push({ x: filteredData.length, event: lastEvent, label: "End", y: lastEPA });

  console.log(arr);

  let teamData = [
    {
      id: teamNum.toString(),
      data: arr,
    },
  ];

  if (splitEvents) {
    teamData = teamData[0].data.reduce((acc, curr) => {
      if (!acc[curr.event]) {
        acc[curr.event] = [];
      }
      acc[curr.event].push(curr);
      return acc;
    }, {} as any);

    teamData = Object.keys(teamData).map((event) => ({
      id: event,
      data: teamData[event],
    }));

    teamData = teamData.sort((a, b) => a.data[0].x - b.data[0].x);
  }

  // RENDER
  return (
    <div className="w-full flex flex-col">
      <div className="w-4/5 mx-auto flex flex-row justify-center">
        <Select
          instanceId={"y-axis-select"}
          className="flex-shrink-0 w-36 h-10 text-sm mr-2"
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={yAxisOptions}
          onChange={(e: any) => setYAxis(e)}
          value={yAxis}
        />
        {splitEvents && (
          <div className="tooltip" data-tip="Combine Events">
            <TbArrowsJoin className="hover_icon" onClick={() => setSplitEvents(false)} />
          </div>
        )}
        {!splitEvents && (
          <div className="tooltip" data-tip="Split Events">
            <TbArrowsSplit className="hover_icon" onClick={() => setSplitEvents(true)} />
          </div>
        )}
      </div>
      <div className="flex">
        <LineChart data={teamData} xAxis="Match" yAxis={yAxis.label} />
      </div>
    </div>
  );
};

export default TeamLineChart;
