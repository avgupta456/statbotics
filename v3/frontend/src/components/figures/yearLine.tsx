import { useEffect, useState } from "react";
import { AiOutlineNumber, AiOutlinePercentage } from "react-icons/ai";
import { GiPodium } from "react-icons/gi";

import { Tooltip } from "@mantine/core";

import { getTeamYearMatches } from "../../api/teams";
import { APITeamMatch, APITeamYear } from "../../types/api";
import { MultiSelect, Select } from "../select";
import { getAxisOptions, renderOptions } from "./axisOptions";
import LineChart from "./lineChart";

function YearLineChart({ year, teamYears }: { year: number; teamYears?: APITeamYear[] }) {
  const [yAxis, setYAxis] = useState({ value: "total_points", label: "Total EPA" });
  const [xAxis, setXAxis] = useState("match");
  const [selectedTeams, setSelectedTeams] = useState<string[]>([]);
  const [allData, setAllData] = useState<{ [key: string]: APITeamMatch[] | undefined }>({});

  const teamOptions = teamYears?.map((team) => ({
    value: team.team,
    label: `${team.team} | ${team.name}`,
  }));

  useEffect(() => {
    setSelectedTeams([]);
    setAllData({});
  }, [year]);

  // FUNCTIONS

  const addTeams = async (newTeams: string[]) => {
    setSelectedTeams(newTeams);
    const newAllData = { ...allData };
    await Promise.all(
      newTeams.map(async (teamNum) => {
        if (!newAllData[teamNum]) {
          const teamData = await getTeamYearMatches(year, teamNum);
          newAllData[teamNum] = teamData;
        }
      }),
    );
    setAllData(newAllData);
  };
  // VARIABLES

  const topTeams = teamYears
    ?.sort(
      (a, b) =>
        (b?.epa?.breakdown?.[yAxis.value]?.mean ?? 0) -
        (a?.epa?.breakdown?.[yAxis.value]?.mean ?? 0),
    )
    ?.slice(0, 3)
    ?.map((team) => team.team);

  const selectedTeamNums: string[] = selectedTeams.map((team) => team);

  const lineData = selectedTeamNums
    .filter((teamNum) => allData[teamNum])
    .map((teamNum) => {
      const currTeamMatchData = allData[teamNum]?.filter(
        (teamMatch: APITeamMatch) => !teamMatch.offseason,
      );
      const currTeamYearData = teamYears?.find((teamYear) => teamYear.team === teamNum);
      const N = currTeamMatchData?.length || 0;
      const teamData = {
        id: teamNum,
        data:
          currTeamMatchData?.map((teamMatch: APITeamMatch, i) => ({
            x: xAxis === "match" ? i : i / Math.max(1, N - 1),
            label: teamMatch?.match || "Start",
            y: teamMatch?.epa?.breakdown?.[yAxis.value],
          })) || [],
      };

      const lastEPA = currTeamYearData?.epa?.breakdown?.[yAxis.value]?.mean ?? 0;
      teamData.data.push({ x: xAxis === "match" ? N : 1, label: "End", y: lastEPA });

      return teamData;
    });

  // RENDER

  return (
    <div className="flex w-full flex-col">
      <div className="mx-auto mb-4 flex flex-row justify-center md:w-4/5">
        <Select
          className="mr-2 h-10 w-36 flex-shrink-0 text-sm"
          data={renderOptions(getAxisOptions(year))}
          value={yAxis?.value}
          onChange={(_value, option) => setYAxis(option)}
        />
        <MultiSelect
          className="mr-2 h-10 flex-grow text-sm"
          data={teamOptions}
          onChange={addTeams}
          value={selectedTeams}
          limit={20}
          searchable
        />
        {topTeams && (
          <Tooltip label="Show Top 3 Teams" className="ml-2">
            <div className="cursor-pointer">
              <GiPodium className="m-2 h-6 w-6 text-gray-600" onClick={() => addTeams(topTeams)} />
            </div>
          </Tooltip>
        )}
        {xAxis === "match" ? (
          <Tooltip label="Show % of Season" className="ml-2">
            <div className="cursor-pointer">
              <AiOutlinePercentage
                className="m-2 h-6 w-6 text-gray-600"
                onClick={() => setXAxis("season")}
              />
            </div>
          </Tooltip>
        ) : (
          <Tooltip label="Show Match Number" className="ml-2">
            <div className="cursor-pointer">
              <AiOutlineNumber
                className="m-2 h-6 w-6 text-gray-600"
                onClick={() => setXAxis("match")}
              />
            </div>
          </Tooltip>
        )}
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
}

export default YearLineChart;
