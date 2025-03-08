"use client";

import React, { useEffect, useState } from "react";
import { AiOutlineNumber, AiOutlinePercentage } from "react-icons/ai";
import { GiPodium } from "react-icons/gi";
import Select, { createFilter } from "react-select";
import WindowedSelect from "react-windowed-select";

import { getTeamYearTeamMatches } from "../../server/teams";
import { APITeamMatch, APITeamYear } from "../../types/api";
import { classnames } from "../../utils";
import { multiSelectStyles } from "../multiSelect";
import LineChart from "./Line";
import { getYAxisOptions } from "./shared";

const YearLineChart = ({
  year,
  teamYears,
  teams,
}: {
  year: number;
  teamYears: APITeamYear[];
  teams: any;
}) => {
  const yAxisOptions = getYAxisOptions(year);
  const [yAxis, setYAxis] = useState(yAxisOptions[0]);
  const [xAxis, setXAxis] = useState("match");
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [allData, setAllData] = useState<{ [key: string]: APITeamMatch[] | undefined }>({});

  useEffect(() => {
    setSelectedTeams([]);
    setAllData({});
  }, [year]);

  // FUNCTIONS

  const fetchData = async (teamNum: number) => {
    const data = await getTeamYearTeamMatches(year, teamNum);

    const sortedData: APITeamMatch[] = data
      .filter((teamMatch: any) => teamMatch.status === "Completed")
      .sort((a: any, b: any) => a.time - b.time);

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
    setAllData({ ...allData, ...allDataCopy });
  };

  // VARIABLES

  const topTeams = teamYears
    ?.sort((a, b) => yAxis.yearAccessor(b) - yAxis.yearAccessor(a))
    ?.slice(0, 3)
    ?.map((team) => ({ value: team.team, label: `${team.team} | ${team.name}` }));

  const selectedTeamNums: number[] = selectedTeams.map((team) => team.value);

  const lineData: any[] = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => {
      const currData = allData[teamNum];
      const N = currData?.length || 0;
      let teamData = {
        id: teamNum,
        data:
          currData?.map((teamMatch: APITeamMatch, i) => ({
            x: xAxis === "match" ? i : i / Math.max(1, N),
            label: currData?.[i - 1]?.match || "Start",
            y: yAxis.matchAccessor(teamMatch),
          })) || [],
      };

      const currTeamYear = teamYears.find((teamYear) => teamYear.team === teamNum);
      const lastEPA = yAxis.yearAccessor(currTeamYear);
      teamData.data.push({ x: xAxis === "match" ? N : 1, label: "End", y: lastEPA });

      return teamData;
    });

  // RENDER

  const TeamSelect = ({ className }) => (
    <WindowedSelect
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
      filterOption={createFilter({ ignoreAccents: false })}
      windowThreshold={100}
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
        {topTeams && (
          <div className="tooltip" data-tip="Show Top 3 Teams">
            <GiPodium className="hover_icon ml-2" onClick={() => addManyTeams(topTeams)} />
          </div>
        )}
        {xAxis === "match" && (
          <div className="tooltip" data-tip="Show % of Season">
            <AiOutlinePercentage className="hover_icon ml-2" onClick={() => setXAxis("season")} />
          </div>
        )}
        {xAxis === "season" && (
          <div className="tooltip" data-tip="Show Match Number">
            <AiOutlineNumber className="hover_icon ml-2" onClick={() => setXAxis("match")} />
          </div>
        )}
      </div>
      <div className="md:hidden w-4/5 mx-auto flex flex-row justify-center">
        <TeamSelect className="" />
      </div>
      <div className="flex">
        <LineChart
          data={lineData}
          xAxis={xAxis === "match" ? "Match Num" : "Season %"}
          yAxis={yAxis.label}
        />
      </div>
    </div>
  );
};

export default YearLineChart;
