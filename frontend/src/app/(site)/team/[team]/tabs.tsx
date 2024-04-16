"use client";

import React, { useMemo } from "react";

import { APITeam } from "../../../../types/api";
import { TeamYearData } from "../../../../types/data";
import TabsSection from "../../shared/tabs";
import FigureSection from "./figures";
import OverviewSection from "./overview";

const Tabs = ({
  teamNum,
  year,
  teamData,
  teamYearData,
  fallbackTeamYearData,
}: {
  teamNum: string;
  year: number;
  teamData: APITeam | undefined;
  teamYearData: TeamYearData | undefined;
  fallbackTeamYearData: TeamYearData | undefined;
}) => {
  const matches = teamYearData?.matches || fallbackTeamYearData?.matches || [];
  const numCompletedMatches = matches.filter((match) => match.status === "Completed").length;

  const MemoizedOverviewSection = useMemo(
    () => <OverviewSection teamData={teamData} teamYearData={teamYearData} />,
    [teamData, teamYearData]
  );

  const MemoizedFigureSection = useMemo(() => {
    // creates smooth transition
    const teamYear = teamYearData?.team_year ?? fallbackTeamYearData?.team_year;
    const matches = teamYearData?.team_matches ?? fallbackTeamYearData?.team_matches ?? [];
    return <FigureSection teamNum={teamNum} year={year} teamYear={teamYear} matches={matches} />;
  }, [teamNum, year, teamYearData, fallbackTeamYearData]);

  const tabs = [
    { title: "Overview", content: MemoizedOverviewSection },
    numCompletedMatches > 0 && { title: "Figures", content: MemoizedFigureSection },
  ].filter(Boolean);

  return (
    <TabsSection
      loading={teamData === undefined || teamYearData === undefined}
      error={false}
      tabs={tabs}
    />
  );
};

export default Tabs;
