"use client";

import React, { useEffect, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../../../constants";
import { log, round } from "../../../../utils";
import PageLayout from "../../shared/layout";
import NotFound from "../../shared/notFound";
import SummaryTabs from "./summaryTabs";
import Tabs from "./tabs";
import { TeamData, TeamYearData, TeamYearsData } from "./types";

async function getTeamData(team: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team/${team}`, { next: { revalidate: 60 } });
  log(`/team/${team} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }

  const data = await res.json();
  return data?.data;
}

async function getTeamYearData(team: number, year: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team/${team}/${year}`, { next: { revalidate: 60 } });
  log(`/team/${team}/${year} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

async function getTeamYearsData(team: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team/${team}/years`, { next: { revalidate: 60 } });
  log(`/team/${team}/years took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

const Page = ({ params }: { params: { team: number } }) => {
  const team = params.team?.[0];
  let paramYear = params.team?.[1] ?? -1;

  if (paramYear !== -1) {
    paramYear = Math.max(paramYear, 2002);
    paramYear = Math.min(paramYear, CURR_YEAR);
  }

  const [prevYear, _setPrevYear] = useState(paramYear);
  const [year, _setYear] = useState(paramYear);

  const setYear = (newYear: number) => {
    _setPrevYear(year);
    _setYear(newYear);
  };

  const [teamData, setTeamData] = useState<TeamData | undefined>();
  const [teamYearsData, setTeamYearsData] = useState<TeamYearsData | undefined>();
  const [teamYearDataDict, setTeamYearDataDict] = useState<{
    [key: number]: TeamYearData | undefined;
  }>({});

  useEffect(() => {
    const _getTeamDataForYear = async (team: number) => {
      if (teamData) {
        return;
      }

      const data: TeamData | undefined = await getTeamData(team);
      setTeamData(data);
    };

    _getTeamDataForYear(team);
  }, [team, teamData]);

  useEffect(() => {
    const _getTeamYearDataForYear = async (team: number, year: number) => {
      if (teamYearDataDict[year]) {
        return;
      }

      const data: TeamYearData | undefined = await getTeamYearData(team, year);
      if (!data) {
        return;
      }

      setTeamYearDataDict((prev) => ({ ...prev, [year]: data }));
    };

    const _getTeamYearsData = async (team: number) => {
      if (teamYearsData) {
        return;
      }

      const data: TeamYearsData | undefined = await getTeamYearsData(team);
      setTeamYearsData(data);
    };

    if (year >= 2002 && year <= CURR_YEAR) {
      _getTeamYearDataForYear(team, year);
    } else {
      _getTeamYearsData(team);
    }
  }, [team, year, teamYearDataDict, teamYearsData]);

  if (!teamData) {
    return <NotFound type="Team" />;
  }

  const teamYearData = teamYearDataDict?.[year];
  const fallbackTeamYearData = teamYearDataDict?.[prevYear];

  const rookieYear = teamData?.rookie_year ?? 2002;

  return (
    <PageLayout
      title={`Team ${team}`}
      year={year}
      setYear={setYear}
      minYear={rookieYear}
      includeSummary
    >
      <div className="w-full text-center text-2xl lg:text-3xl mb-4">{teamData?.team}</div>
      {year >= 2002 && year <= CURR_YEAR ? (
        <Tabs
          teamNum={team}
          year={year}
          teamData={teamData}
          teamYearData={teamYearData}
          fallbackTeamYearData={fallbackTeamYearData}
        />
      ) : (
        <SummaryTabs teamNum={team} teamData={teamData} teamYearsData={teamYearsData} />
      )}
    </PageLayout>
  );
};

export default Page;
