"use client";

import React, { useMemo } from "react";

import TabsSection from "../../shared/tabs";
import SummaryOverviewSection from "./summaryOverview";
import { TeamData, TeamYearsData } from "./types";

const SummaryTabs = ({
  teamNum,
  teamData,
  teamYearsData,
}: {
  teamNum: number;
  teamData: TeamData | undefined;
  teamYearsData: TeamYearsData | undefined;
}) => {
  const MemoizedSummaryOverviewSection = useMemo(
    () => <SummaryOverviewSection teamData={teamData} teamYearsData={teamYearsData} />,
    [teamData, teamYearsData]
  );

  const tabs = [{ title: "Overview", content: MemoizedSummaryOverviewSection }];

  return (
    <TabsSection
      loading={teamData === undefined || teamYearsData === undefined}
      error={false}
      tabs={tabs}
    />
  );
};

export default SummaryTabs;
