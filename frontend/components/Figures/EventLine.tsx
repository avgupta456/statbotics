"use client";

import React, { useState } from "react";
import Select from "react-select";

import { BACKEND_URL } from "../../constants";
import { multiSelectStyles } from "../multiSelect";
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

  // const moverTeams = teamEvents
  //   .sort((a, b) => b[`${yAxis}_diff`] - a[`${yAxis}_diff`])
  //   .slice(0, 3)
  //   .map((team) => ({ value: team.num, label: `${team.num} | ${team.team}` }));

  const selectedTeamNums: number[] = selectedTeams.map((team: any) => team.value);

  const lineData: any[] = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => {
      let teamData = {
        id: teamNum,
        data: allData[teamNum].map((teamMatch: any, i: number) => ({
          x: allData[teamNum][i - 1] ? allData[teamNum][i - 1].match : 0,
          y: teamMatch[yAxis.value],
        })),
      };

      const lastMatch = allData[teamNum][allData[teamNum].length - 1].match;
      const lastEPA = teamEvents[teamEvents.findIndex((team) => team.num === teamNum)][yAxis.value];
      teamData.data.push({ x: lastMatch, y: lastEPA });

      return teamData;
    });

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
        <button className="flex-shrink-0 filter_button w-36" onClick={() => addManyTeams(topTeams)}>
          Show Top 3 Teams
        </button>
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
