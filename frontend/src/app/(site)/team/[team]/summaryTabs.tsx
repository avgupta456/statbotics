"use client";

import React, { useMemo } from "react";

import { APITeam } from "../../../../types/api";
import TabsSection from "../../shared/tabs";
import SummaryOverviewSection from "./summaryOverview";
import { SummaryRow } from "./types";

const SummaryTabs = ({
  teamData,
  teamYearsData,
}: {
  teamData: APITeam | undefined;
  teamYearsData: SummaryRow[] | undefined;
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
