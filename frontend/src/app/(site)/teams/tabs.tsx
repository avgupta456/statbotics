"use client";

import React, { useMemo } from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { CURR_YEAR, RP_NAMES } from "../../../constants";
import { TeamYearsData, emptyTeamYearsData } from "../../../types/data";
import TabsSection from "../shared/tabs";
import BreakdownTable from "./breakdownTable";
import FigureSection from "./figures";
import InsightsTable from "./insightsTable";

const Tabs = ({
  year,
  data,
  error,
  filters,
  setFilters,
}: {
  year: number;
  data: TeamYearsData | undefined;
  error: boolean;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
}) => {
  const MemoizedInsightsTable = useMemo(
    () => (
      <InsightsTable
        year={year}
        data={data || emptyTeamYearsData}
        filters={filters}
        setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
      />
    ),
    [year, data, filters, setFilters]
  );

  const MemoizedBreakdownTable = useMemo(
    () => (
      <BreakdownTable
        year={year}
        data={data || emptyTeamYearsData}
        filters={filters}
        setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
      />
    ),
    [year, data, filters, setFilters]
  );

  const MemoizedBubbleChart = useMemo(
    () => (
      <BubbleChart
        year={year}
        data={data?.team_years ?? []}
        defaultFilters={{ country: "", state: "", district: "" }}
        filters={filters}
        setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
        columnOptions={
          [
            "Total EPA",
            year >= CURR_YEAR && "Unitless EPA",
            year >= 2016 && "Auto",
            year >= 2016 && "Teleop",
            year >= 2016 && "Endgame",
            year >= 2016 && "Auto + Endgame",
            year >= 2016 && `${RP_NAMES[year][0]}`,
            year >= 2016 && `${RP_NAMES[year][1]}`,
            "Wins",
            "Win Rate",
          ].filter(Boolean) as string[]
        }
      />
    ),
    [year, data, filters, setFilters]
  );

  const MemoizedFigureSection = useMemo(
    () => <FigureSection year={year} data={data || emptyTeamYearsData} />,
    [year, data]
  );

  const tabs = [
    { title: "Insights", content: MemoizedInsightsTable },
    { title: "Breakdown", content: MemoizedBreakdownTable },
    { title: "Bubble Chart", content: MemoizedBubbleChart },
    { title: "Figures", content: MemoizedFigureSection },
  ].filter(Boolean);

  return <TabsSection loading={data === undefined} error={error} tabs={tabs} />;
};

export default Tabs;
