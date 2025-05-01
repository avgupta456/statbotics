"use client";

import React, { useEffect, useState } from "react";

import Image from "next/image";
import Link from "next/link";

import { getTeamYear } from "../../api/team";
import { CURR_YEAR } from "../../constants";
import { TeamYearData } from "../../types/data";
import PageLayout from "../shared/layout";
import NotFound from "../shared/notFound";
import SummaryTabs from "./summaryTabs";
import Tabs from "./tabs";

const PageContent = ({ team, paramYear }: { team: number; paramYear: number }) => {
  if (isNaN(team)) {
    return <NotFound type="Team" />;
  }

  const [prevYear, _setPrevYear] = useState(paramYear);
  const [year, _setYear] = useState(paramYear);

  const setYear = (newYear: number) => {
    _setPrevYear(year);
    _setYear(newYear);
  };

  const [teamYearDataDict, setTeamYearDataDict] = useState<{
    [key: number]: TeamYearData | undefined;
  }>({});

  useEffect(() => {
    setTeamYearDataDict({});
  }, [team]);

  useEffect(() => {
    const _getTeamYearDataForYear = async (team: number, year: number) => {
      if (teamYearDataDict[year]) {
        return;
      }

      const data: TeamYearData | undefined = await getTeamYear(team, year);
      if (!data) {
        return;
      }

      setTeamYearDataDict((prev) => ({ ...prev, [year]: data }));
    };

    if (year >= 2002 && year <= CURR_YEAR) {
      _getTeamYearDataForYear(team, year);
    }
  }, [team, year]);

  const teamYearData = teamYearDataDict?.[year];
  const fallbackTeamYearData = teamYearDataDict?.[prevYear];

  if (!teamYearData && !fallbackTeamYearData) {
    return <NotFound type="Team" />;
  }

  const rookieYear = teamYearData?.team_year?.rookie_year ?? 2002;

  let yearOptions = Array.from(
    { length: CURR_YEAR - rookieYear + 1 },
    (_, i) => rookieYear + i
  ).reverse();

  // remembers name when selecting a year without data
  const teamName = Object.values(teamYearDataDict).find((data) => data?.team_year?.team === team)
    ?.team_year?.name;

  return (
    <PageLayout
      title={`Team ${team}`}
      year={year}
      setYear={setYear}
      years={yearOptions}
      includeSummary
    >
      <div className="w-full flex items-center justify-center mb-4">
        <div className="text-2xl lg:text-3xl">{teamName}</div>
        <Link
          href={`https://www.thebluealliance.com/team/${team}`}
          rel="noopener noreferrer"
          target="_blank"
          className="ml-4"
        >
          <Image src="/tba.png" alt="TBA" width={28} height={28} />
        </Link>
      </div>
      {year >= 2002 && year <= CURR_YEAR ? (
        <Tabs
          teamNum={team}
          year={year}
          teamYearData={teamYearData}
          fallbackTeamYearData={fallbackTeamYearData}
        />
      ) : (
        <SummaryTabs team={team} />
      )}
    </PageLayout>
  );
};

export default PageContent;
