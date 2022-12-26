"use client";

import React, { useState } from "react";
import Select from "react-select";

import { BACKEND_URL } from "../../constants";
import { TeamEvent } from "../types/api";
import LineChart from "./Line";

const EventLineChart = ({
  eventId,
  teamEvents,
  teams,
}: {
  eventId: string;
  teamEvents: TeamEvent[];
  teams: any;
}) => {
  const [yAxis, setYAxis] = useState({ value: "total_epa", label: "Total EPA" });
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [allData, setAllData] = useState<any>({});

  // FUNCTIONS

  const fetchData = async (teamNum: number) => {
    const res = await fetch(`${BACKEND_URL}/event/${eventId}/team_matches/${teamNum}`);
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
      .sort((a: any, b: any) => a.match - b.match);

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
    const newTeams = _newTeams; // _newTeams.filter((team) => !selectedTeamNums.includes(team.value));
    setSelectedTeams([, ...newTeams]);
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
    .map((team) => ({ value: team.num, label: `${team.team} | ${team.num}` }));

  // const moverTeams = teamEvents
  //   .sort((a, b) => b[`${yAxis}_diff`] - a[`${yAxis}_diff`])
  //   .slice(0, 3)
  //   .map((team) => ({ value: team.num, label: `${team.team} | ${team.num}` }));

  const selectedTeamNums: number[] = selectedTeams.map((team: any) => team.value);

  const lineData: any[] = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => ({
      id: teamNum,
      data: allData[teamNum].map((teamMatch: any) => ({
        x: teamMatch.match,
        y: teamMatch[yAxis.value],
      })),
    }));

  // RENDER

  return (
    <div className="w-full flex flex-col">
      <div className="w-3/4 mx-auto flex flex-row justify-center">
        <Select
          instanceId={"y-axis-select"}
          className="w-36 h-10 text-sm mr-2"
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={[
            { value: "auto_epa", label: "Auto EPA" },
            { value: "teleop_epa", label: "Teleop EPA" },
            { value: "endgame_epa", label: "Endgame EPA" },
            { value: "total_epa", label: "Total EPA" },
            { value: "rp_1_epa", label: "RP 1 EPA" },
            { value: "rp_2_epa", label: "RP 2 EPA" },
          ]}
          onChange={(e: any) => setYAxis(e)}
          value={yAxis}
        />
        <Select
          isMulti
          instanceId={"team-select"}
          className="flex-grow text-sm mr-2"
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={teams}
          onChange={addTeam}
          value={selectedTeams}
        />
        <button
          className="border-2 border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer h-10 w-32 px-2 mr-2 rounded text-sm flex items-center justify-center"
          onClick={() => addManyTeams(topTeams)}
        >
          Add Top 3 Teams
        </button>
      </div>
      <div className="w-3/4 mx-auto flex">
        <LineChart
          data={lineData}
          xAxis="Match"
          yAxis="Total EPA"
          isRP={yAxis.value.includes("rp_")}
        />
      </div>
    </div>
  );
};

export default EventLineChart;
