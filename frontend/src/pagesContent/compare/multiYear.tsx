"use client";

import React, { useState } from "react";
import { createFilter } from "react-select";
import WindowedSelect from "react-windowed-select";

import { getTeam } from "../../api/team";
import LineChart from "../../components/Figures/Line";
import { multiSelectStyles } from "../../components/multiSelect";
import { CURR_YEAR } from "../../constants";
import { ShortTeam } from "../../types/data";
import { round } from "../../utils";

const MultiYear = ({ teams }: { teams: ShortTeam[] }) => {
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [allData, setAllData] = useState<{ [key: number]: any[] }>({});

  const teamOptions = teams?.map((team) => ({
    value: team.team,
    label: `${team.team} | ${team.name}`,
  }));

  const fetchData = async (teamNum: number) => {
    const data = await getTeam(teamNum);

    const sortedData: any[] = data.team_years
      .filter((x) => x.year <= CURR_YEAR)
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
    .map((teamNum) => allData[teamNum]?.map((x) => x.norm_epa || x.unitless_epa) || [])
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
          y: round(x.norm_epa || x.unitless_epa, 0),
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
    <div className="w-full h-full flex-grow flex flex-col md:pb-4 md:px-4">
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
  );
};

export default MultiYear;
