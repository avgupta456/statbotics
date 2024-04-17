"use client";

import React, { useState } from "react";
import { GiPodium } from "react-icons/gi";
import Select from "react-select";

import { BACKEND_URL } from "../../constants";
import { APITeamEvent, APITeamMatch } from "../../types/api";
import { classnames, log, round } from "../../utils";
import { multiSelectStyles } from "../multiSelect";
import LineChart from "./Line";
import { getYAxisOptions } from "./shared";

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
  const yAxisOptions = getYAxisOptions(year);
  const [yAxis, setYAxis] = useState(yAxisOptions[0]);
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [allData, setAllData] = useState<{ [key: number]: APITeamMatch[] }>({});

  // FUNCTIONS

  const fetchData = async (teamNum: number) => {
    const start = performance.now();
    const res = await fetch(`${BACKEND_URL}/event/${eventId}/team_matches/${teamNum}`, {
      next: { revalidate: 60 },
    });
    log(`/event/${eventId}/team_matches/${teamNum} took ${round(performance.now() - start, 0)} ms`);

    if (!res.ok) {
      return undefined;
    }

    const data: { data: APITeamMatch[] } | undefined = await res.json();
    if (!data) {
      log("No data found for team " + teamNum);
      return undefined;
    }

    const sortedData = data.data
      .filter((teamMatch: any) => !teamMatch.playoff && teamMatch.status === "Completed")
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
    .sort((a, b) => yAxis.yearAccessor(b) - yAxis.yearAccessor(a))
    .slice(0, 3)
    .map((team) => ({ value: team.team, label: `${team.team} | ${team.team_name}` }));

  const selectedTeamNums: string[] = selectedTeams.map((team: any) => team.value);

  const lineData: any[] = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => {
      let teamData = {
        id: teamNum,
        data: allData[teamNum].map((teamMatch: any, i: number) => ({
          x: i, // TODO: fix here
          label: allData[teamNum][i - 1]?.match || "Start",
          y: yAxis.matchAccessor(teamMatch),
        })),
      };

      if (teamData.data.length > 0) {
        const lastMatch = allData[teamNum].length;
        const lastEPA = yAxis.yearAccessor(
          teamEvents[teamEvents.findIndex((team) => team.team === teamNum)]
        );
        teamData.data.push({ x: lastMatch, label: "End", y: lastEPA });
      }

      return teamData;
    });

  // RENDER
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
        <LineChart data={lineData} xAxis="Match" yAxis={yAxis.label} />
      </div>
    </div>
  );
};

export default EventLineChart;
