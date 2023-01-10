"use client";

import React, { useEffect, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../../../constants";
import { round } from "../../../../utils";
import PageLayout from "../../shared/layout";
import NotFound from "../../shared/notFound";
import Tabs from "./tabs";
import { TeamData, TeamYearData } from "./types";

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
  const res = await fetch(`${BACKEND_URL}/team/${team}/${year}`);
  console.log(`/team/${team}/${year} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

const Page = ({ params }: { params: { team: number } }) => {
  const { team } = params;
  const [prevYear, _setPrevYear] = useState(CURR_YEAR);
  const [year, _setYear] = useState(CURR_YEAR);

  const setYear = (newYear: number) => {
    _setPrevYear(year);
    _setYear(newYear);
  };

  const [teamData, setTeamData] = useState<TeamData | undefined>();
  const [teamYearDataDict, setTeamYearDataDict] = useState<{
    [key: number]: TeamYearData | undefined;
  }>({});

  useEffect(() => {
    const getTeamDataForYear = async (team: number) => {
      if (teamData) {
        return;
      }

      const data: TeamData | undefined = await getTeamData(team);
      setTeamData(data);
    };

    getTeamDataForYear(team);
  }, [team, teamData]);

  useEffect(() => {
    const getTeamYearDataForYear = async (team: number, year: number) => {
      if (teamYearDataDict[year]) {
        return;
      }

      const data: TeamYearData | undefined = await getTeamYearData(team, year);
      if (!data) {
        return;
      }

      setTeamYearDataDict((prev) => ({ ...prev, [year]: data }));
    };

    getTeamYearDataForYear(team, year);
  }, [team, year, teamYearDataDict]);

  if (!teamData) {
    return <NotFound type="Team" />;
  }

  const teamYearData = teamYearDataDict[year];
  const fallbackTeamYearData = teamYearDataDict[prevYear];

  const rookieYear = teamData?.rookie_year ?? 2002;

  return (
    <PageLayout title={`Team ${team}`} year={year} setYear={setYear} minYear={rookieYear}>
      <div className="w-full text-center text-2xl lg:text-3xl mb-4">{teamData?.team}</div>
      <Tabs
        teamNum={team}
        year={year}
        teamData={teamData}
        teamYearData={teamYearData}
        fallbackTeamYearData={fallbackTeamYearData}
      />
    </PageLayout>
  );
};

export default Page;
