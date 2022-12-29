"use client";

import React, { useEffect, useState } from "react";
import Select from "react-select";

import { yearOptions } from "../../../../components/filterConstants";
import { TeamMatch } from "../../../../components/types/api";
import { BACKEND_URL } from "../../../../constants";
import { round } from "../../../../utils";
import Tabs from "./tabs";
import { Data } from "./types";

async function getTeamData(team: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team/${team}`);
  console.log(`/team/${team} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }

  const data = await res.json();
  return data?.data;
}

async function getTeamYearData(team: number, year: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team_year/${year}/${team}`);
  console.log(`/team_year/${year}/${team} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

const Page = ({ params }: { params: { team: number } }) => {
  const { team } = params;
  const [prevYear, _setPrevYear] = useState(2022);
  const [year, _setYear] = useState(2022);

  const setYear = (newYear: number) => {
    _setPrevYear(year);
    _setYear(newYear);
  };

  const [teamData, setTeamData] = useState<Data>();
  const [teamYearDataDict, setTeamYearDataDict] = useState<{ [key: number]: TeamMatch[] }>({});

  useEffect(() => {
    const getTeamDataForYear = async (team: number) => {
      if (teamData) {
        return;
      }

      const data: Data = await getTeamData(team);
      setTeamData(data);
    };

    getTeamDataForYear(team);
  }, [team, teamData]);

  useEffect(() => {
    const getTeamYearDataForYear = async (team: number, year: number) => {
      if (teamYearDataDict[year]) {
        return;
      }

      const data: TeamMatch[] = await getTeamYearData(team, year);
      setTeamYearDataDict((prev) => ({ ...prev, [year]: data }));
    };

    getTeamYearDataForYear(team, year);
  }, [team, year, teamYearDataDict]);

  const teamYearData = teamYearDataDict[year];
  const fallbackTeamYearData = teamYearDataDict[prevYear];

  console.log(teamData);
  console.log(teamYearData);

  const rookieYear = teamData?.rookie_year ?? 2002;

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <Select
            instanceId={"year-select"}
            className="w-28"
            styles={{
              menu: (provided) => ({ ...provided, zIndex: 9999 }),
            }}
            options={yearOptions.filter((y) => parseInt(y.value) >= rookieYear)}
            onChange={(e) => setYear((e?.value ?? 2023) as number)}
            value={{
              value: year.toString(),
              label: year.toString(),
            }}
          />
          <p className="text-2xl lg:text-3xl ml-3">
            Team {team} - {teamData?.team}
          </p>
        </div>
        <Tabs
          teamNum={team}
          year={year}
          teamData={teamData}
          teamYearData={teamYearData}
          fallbackTeamYearData={fallbackTeamYearData}
        />
      </div>
    </div>
  );
};

export default Page;
