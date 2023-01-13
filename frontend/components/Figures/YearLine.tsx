"use client";

import React, { useEffect, useState } from "react";
import { AiOutlineNumber, AiOutlinePercentage } from "react-icons/ai";
import { GiPodium } from "react-icons/gi";
import Select, { createFilter } from "react-select";
import WindowedSelect from "react-windowed-select";

import { BACKEND_URL, RPMapping } from "../../constants";
import { classnames, log, round } from "../../utils";
import { multiSelectStyles } from "../multiSelect";
import { APITeamMatch, APITeamYear } from "../types/api";
import LineChart from "./Line";

const YearLineChart = ({
  year,
  teamYears,
  teams,
}: {
  year: number;
  teamYears: APITeamYear[];
  teams: any;
}) => {
  const [yAxis, setYAxis] = useState({ value: "total_epa", label: "Total EPA" });
  const [xAxis, setXAxis] = useState("match");
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [allData, setAllData] = useState<{ [key: number]: APITeamMatch[] | undefined }>({});

  useEffect(() => {
    setSelectedTeams([]);
    setAllData({});
  }, [year]);

  // FUNCTIONS

  const fetchData = async (teamNum: number) => {
    const start = performance.now();
    const res = await fetch(`${BACKEND_URL}/team_year/${year}/${teamNum}/matches`, {
      next: { revalidate: 60 },
    });
    log(`/team_year/${year}/${teamNum}/matches took ${round(performance.now() - start, 0)} ms`);

    if (!res.ok) {
      return undefined;
    }

    const data = await res.json();
    if (!data) {
      log("No data found for team " + teamNum);
      return undefined;
    }

    const sortedData: APITeamMatch[] = data.data
      // .filter((teamYear: any) => !teamYear.playoff)
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
    .sort((a, b) => b[yAxis.value] - a[yAxis.value])
    .slice(0, 3)
    .map((team) => ({ value: team.num, label: `${team.num} | ${team.team}` }));

  const selectedTeamNums: number[] = selectedTeams.map((team) => team.value);

  const lineData: any[] = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => {
      const currData = allData[teamNum]?.filter((teamMatch: APITeamMatch) => !teamMatch.offseason);
      const N = currData?.length || 0;
      let teamData = {
        id: teamNum,
        data:
          currData?.map((teamMatch: APITeamMatch, i) => ({
            x: xAxis === "match" ? i : i / Math.max(1, N - 1),
            label: currData?.[i - 1]?.match || "Start",
            y: teamMatch[yAxis.value],
          })) || [],
      };

      // TODO: fix this to the actual post-match EPA
      const lastEPA = currData?.[N - 1]?.[yAxis.value];
      teamData.data.push({ x: xAxis === "match" ? N : 1, label: "End", y: lastEPA });

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
          { value: "rp_1_epa", label: `${RPMapping?.[year]?.[0]} EPA` },
          { value: "rp_2_epa", label: `${RPMapping?.[year]?.[1]} EPA` },
        ]
      : [{ value: "total_epa", label: "EPA" }];

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
        <div className="tooltip" data-tip="Show Top 3 Teams">
          <GiPodium className="hover_icon ml-2" onClick={() => addManyTeams(topTeams)} />
        </div>
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
          isRP={yAxis.value.includes("rp_")}
        />
      </div>
    </div>
  );
};

export default YearLineChart;
