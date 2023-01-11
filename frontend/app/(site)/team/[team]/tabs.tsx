"use client";

import React, { useMemo } from "react";

import TabsSection from "../../shared/tabs";
import FigureSection from "./figures";
import OverviewSection from "./overview";
import { TeamData, TeamYearData } from "./types";

const Tabs = ({
  teamNum,
  year,
  teamData,
  teamYearData,
  fallbackTeamYearData,
}: {
  teamNum: number;
  year: number;
  teamData: TeamData | undefined;
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
    const matches = teamYearData?.team_matches || fallbackTeamYearData?.team_matches || [];
    return (
      <FigureSection
        teamNum={teamNum}
        year={year}
        // creates smooth transition
        matches={matches}
      />
    );
  }, [teamNum, year, teamYearData, fallbackTeamYearData]);

  const tabs = [
    { title: "Overview", content: MemoizedOverviewSection },
    numCompletedMatches > 0 && { title: "Figures", content: MemoizedFigureSection },
  ].filter(Boolean);

  return <TabsSection tabs={tabs} loading={teamData === undefined || teamYearData === undefined} />;
};

export default Tabs;
