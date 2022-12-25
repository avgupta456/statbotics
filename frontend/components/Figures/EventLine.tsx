"use client";

import React, { useState } from "react";
import Select from "react-select";

import { BACKEND_URL } from "../../constants";
import LineChart from "./Line";

const EventLineChart = ({ event_id, teams }: { event_id: string; teams: any }) => {
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [allData, setAllData] = useState<any>({});

  const fetchData = async (team_num: number) => {
    if (allData[team_num]) {
      return;
    }

    const res = await fetch(`${BACKEND_URL}/event/${event_id}/team_matches/${team_num}`);
    if (!res.ok) {
      return undefined;
    }
    const data = await res.json();
    if (!data) {
      console.log("No data found for team " + team_num);
      return;
    }

    const sortedData = data.data
      .filter((teamMatch: any) => !teamMatch.playoff)
      .sort((a: any, b: any) => a.match - b.match);

    setAllData({ ...allData, [team_num]: sortedData });
  };

  const selectedTeamNums: number[] = selectedTeams.map((team: any) => team.value);

  const lineData: any[] = selectedTeamNums
    .filter((team_num) => allData[team_num])
    .map((team_num) => ({
      id: team_num,
      data: allData[team_num].map((teamMatch: any) => ({
        x: teamMatch.match,
        y: teamMatch.total_epa,
      })),
    }));

  return (
    <div className="w-full flex flex-col">
      <div className="w-full flex flex-row justify-center">
        <Select
          isMulti
          instanceId={"team-select"}
          className="w-3/4 text-sm mr-2"
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={teams}
          onChange={(selected) => {
            if (selected.length > selectedTeams.length) {
              const team = selected[selected.length - 1].value;
              fetchData(team);
            }
            setSelectedTeams(selected);
          }}
          value={selectedTeams}
        />
      </div>
      <LineChart data={lineData} />
    </div>
  );
};

export default EventLineChart;
