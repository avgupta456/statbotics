"use client";

import React, { useState } from "react";
import { TbArrowsJoin, TbArrowsSplit } from "react-icons/tb";
import Select from "react-select";

import { APITeamMatch, APITeamYear } from "../../types/api";
import LineChart from "./Line";
import { getYAxisOptions } from "./shared";

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
  const yAxisOptions = getYAxisOptions(year);
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
