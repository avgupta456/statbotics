"use client";

import React, { useEffect, useState } from "react";
import Select, { createFilter } from "react-select";
import WindowedSelect from "react-windowed-select";

import LineChart from "../../../components/Figures/Line";
import { multiSelectStyles } from "../../../components/multiSelect";
import { BACKEND_URL, CURR_YEAR } from "../../../constants";
import { classnames, log, round } from "../../../utils";
import { getWithExpiry, setWithExpiry } from "../../localStorage";

// copied from navbar.tsx
// TODO: consolidate with navbar.tsx
async function getTeamData() {
  const cacheData = getWithExpiry("full_team_list");
  if (cacheData && cacheData?.length > 1000) {
    log("Used Local Storage: Full Team List");
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/teams/all`, { next: { revalidate: 60 } });
  log(`/teams/all took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  setWithExpiry("full_team_list", data, 60 * 60 * 24 * 7); // 1 week expiry
  return data;
}

const Page = () => {
  const [teams, setTeams] = useState([]);
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [allData, setAllData] = useState<{ [key: number]: any }>({});

  useEffect(() => {
    getTeamData().then((data) => setTeams(data));
  }, []);

  const teamOptions = teams?.map((team: any) => ({
    value: team.num,
    label: `${team.num} | ${team.team}`,
  }));

  console.log("teams", teams);
  console.log("selectedTeams", selectedTeams);
  console.log("allData", allData);

  const fetchData = async (teamNum: number) => {
    const start = performance.now();
    const res = await fetch(`${BACKEND_URL}/team/${teamNum}/years`, {
      next: { revalidate: 60 },
    });
    log(`/team/${teamNum}/years took ${round(performance.now() - start, 0)} ms`);

    if (!res.ok) {
      return undefined;
    }

    const data = await res.json();
    if (!data) {
      log("No data found for team " + teamNum);
      return undefined;
    }

    const sortedData: any[] = data.data
      .filter((x) => x.year < CURR_YEAR)
      .sort((a: any, b: any) => a.year - b.year);

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

  const selectedTeamNums = selectedTeams.map((x) => x.value);

  let xSamples = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => allData[teamNum]?.map((x) => x.year) || [])
    .flat();

  if (xSamples.length === 0) {
    xSamples = [2002, CURR_YEAR];
  }

  let ySamples = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => allData[teamNum]?.map((x) => x.norm_epa) || [])
    .flat();

  if (ySamples.length === 0) {
    ySamples = [1200, 2200];
  }

  const xMin = Math.min(...xSamples);
  const xMax = Math.max(...xSamples);
  let roundedYMin = Math.floor(Math.min(...ySamples) / 50) * 50;
  roundedYMin = Math.min(1400, Math.max(roundedYMin - 50, 1200));
  let roundedYMax = Math.ceil(Math.max(...ySamples) / 50) * 50;
  roundedYMax = Math.min(roundedYMax + 50, 2200);

  let lineData: any[] = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => ({
      id: teamNum,
      data:
        allData[teamNum]?.map((x) => ({
          x: x.year,
          y: round(x.norm_epa, 0),
          label: x.year.toString(),
        })) || [],
    }));

  lineData.unshift({
    id: "Baseline",
    data: [
      { x: xMin, y: 1500, label: xMin.toString() },
      { x: xMax, y: 1500, label: xMax.toString() },
    ],
  });

  return (
    <div className="w-full h-full flex-grow flex flex-col pt-4 md:pt-8 md:pb-4 md:px-4">
      <div className="h-full h-full flex-grow flex flex-col">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <p className="text-xl lg:text-2xl">Compare Teams by Normalized EPA</p>
        </div>
        <div className="md:w-4/5 mx-auto flex flex-row justify-center mb-4">
          <WindowedSelect
            isMulti
            instanceId={"team-select"}
            className={"flex-grow text-sm mr-2"}
            styles={multiSelectStyles((value) => {
              let index = 0;
              if (selectedTeams.length > 0) {
                index = selectedTeams.findIndex((x) => x?.value === value);
              }
              return index + 1;
            })}
            options={teamOptions || []}
            onChange={addTeam}
            value={selectedTeams}
            filterOption={createFilter({ ignoreAccents: false })}
            windowThreshold={100}
          />
        </div>
        <div className="flex">
          <LineChart
            data={lineData}
            xAxis="Year"
            yAxis="Norm EPA"
            xMin={xMin}
            xMax={xMax}
            yMin={roundedYMin}
            yMax={roundedYMax}
          />
        </div>
      </div>
    </div>
  );
};

export default Page;
