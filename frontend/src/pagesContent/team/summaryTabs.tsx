"use client";

import React, { useEffect, useMemo, useState } from "react";

import { getTeam } from "../../api/team";
import { APITeam } from "../../types/api";
import TabsSection from "../shared/tabs";
import SummaryOverviewSection from "./summaryOverview";
import { SummaryRow } from "./types";

const SummaryTabs = ({ team }: { team: number }) => {
  const [teamData, setTeamData] = useState<APITeam | undefined>();
  const [teamYearsData, setTeamYearsData] = useState<SummaryRow[] | undefined>();

  useEffect(() => {
    const _getTeamDataForYear = async (team: number) => {
      if (teamData) {
        if (teamData.team == team) {
          return;
        } else {
          setTeamData(undefined);
          setTeamYearsData(undefined);
          return; // Will trigger useEffect again
        }
      }

      const data = await getTeam(team);
      setTeamData(data.team);
      setTeamYearsData(data.team_years);
    };

    _getTeamDataForYear(team);
  }, [team, teamData]);

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
