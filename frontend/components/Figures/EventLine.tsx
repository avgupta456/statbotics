"use client";

import React, { useState } from "react";
import { GiPodium } from "react-icons/gi";
import Select from "react-select";

import { BACKEND_URL, RPMapping } from "../../constants";
import { classnames, round } from "../../utils";
import { multiSelectStyles } from "../multiSelect";
import { APITeamEvent, APITeamMatch } from "../types/api";
import LineChart from "./Line";

const EventLineChart = ({
  eventId,
  year,
  teamEvents,
  teams,
}: {
  eventId: string;
  year: number;
  teamEvents: APITeamEvent[];
  teams: any;
}) => {
  const [yAxis, setYAxis] = useState({ value: "total_epa", label: "Total EPA" });
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [allData, setAllData] = useState<{ [key: number]: APITeamMatch[] }>({});

  // FUNCTIONS

  const fetchData = async (teamNum: number) => {
    const start = performance.now();
    const res = await fetch(`${BACKEND_URL}/event/${eventId}/team_matches/${teamNum}`);
    console.log(
      `/event/${eventId}/team_matches/${teamNum} took ${round(performance.now() - start, 0)} ms`
    );

    if (!res.ok) {
      return undefined;
    }

    const data = await res.json();
    if (!data) {
      console.log("No data found for team " + teamNum);
      return undefined;
    }

    const sortedData = data.data
      .filter((teamMatch: any) => !teamMatch.playoff)
      .sort((a: any, b: any) => a.match_num - b.match_num);

    return sortedData;
  };

  const addTeam = async (selected) => {
    if (selected.length > selectedTeams.length) {
      const team = selected[selected.length - 1].value;
      if (!allData[team]) {
        const newData = await fetchData(team);
        setAllData({ ...allData, [team]: newData });
      }
    }
    setSelectedTeams(selected);
  };

  const addManyTeams = async (_newTeams) => {
    const newTeams = _newTeams;
    setSelectedTeams([...newTeams]);
    let allDataCopy = {};
    for (const team of newTeams) {
      const newData = await fetchData(team.value);
      allDataCopy = { ...allDataCopy, [team.value]: newData };
    }
    setAllData(allDataCopy);
  };

  // VARIABLES

  const topTeams = teamEvents
    .sort((a, b) => b[yAxis.value] - a[yAxis.value])
    .slice(0, 3)
    .map((team) => ({ value: team.num, label: `${team.num} | ${team.team}` }));

  const selectedTeamNums: number[] = selectedTeams.map((team: any) => team.value);

  const lineData: any[] = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => {
      let teamData = {
        id: teamNum,
        data: allData[teamNum].map((teamMatch: any, i: number) => ({
          x: allData[teamNum][i - 1]?.match_number || 0,
          label: allData[teamNum][i - 1]?.match || "Start",
          y: teamMatch[yAxis.value],
        })),
      };

      if (teamData.data.length > 0) {
        const lastMatch = allData[teamNum][allData[teamNum].length - 1].match_number;
        const lastEPA =
          teamEvents[teamEvents.findIndex((team) => team.num === teamNum)][yAxis.value];
        teamData.data.push({ x: lastMatch, label: "End", y: lastEPA });
      }

      return teamData;
    });

  // RENDER

  const yAxisOptions =
    year >= 2016
      ? [
          { value: "total_epa", label: "Total EPA" },
          { value: "auto_epa", label: "Auto EPA" },
          { value: "teleop_epa", label: "Teleop EPA" },
          { value: "endgame_epa", label: "Endgame EPA" },
          { value: "rp_1_epa", label: `${RPMapping[year][0]} EPA` },
          { value: "rp_2_epa", label: `${RPMapping[year][1]} EPA` },
        ]
      : [{ value: "total_epa", label: "EPA" }];

  const TeamSelect = ({ className }) => (
    <Select
      isMulti
      instanceId={"team-select"}
      className={classnames("flex-grow text-sm mr-2", className)}
      styles={multiSelectStyles((value) => {
        let index = 0;
        if (selectedTeams.length > 0) {
          index = selectedTeams.findIndex((team) => team?.value === value);
        }
        return index;
      })}
      options={teams}
      onChange={addTeam}
      value={selectedTeams}
    />
  );

  return (
    <div className="w-full flex flex-col">
      <div className="md:w-4/5 mx-auto flex flex-row justify-center mb-4">
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
        <TeamSelect className="hidden md:inline-block" />
        <div className="tooltip" data-tip="Show Top 3 Teams">
          <GiPodium className="hover_icon ml-2" onClick={() => addManyTeams(topTeams)} />
        </div>
      </div>

      <div className="md:hidden w-4/5 mx-auto flex flex-row justify-center">
        <TeamSelect className="" />
      </div>
      <div className="flex">
        <LineChart
          data={lineData}
          xAxis="Match"
          yAxis={yAxis.label}
          isRP={yAxis.value.includes("rp_")}
        />
      </div>
    </div>
  );
};

export default EventLineChart;
