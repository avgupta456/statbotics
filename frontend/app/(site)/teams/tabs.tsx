"use client";

import React, { useMemo } from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { CURR_YEAR, RPMapping } from "../../../constants";
import TabsSection from "../shared/tabs";
import { TeamYearData, emptyTeamYearData } from "../types";
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
  data: TeamYearData | undefined;
  error: boolean;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
}) => {
  const MemoizedInsightsTable = useMemo(
    () => (
      <InsightsTable
        year={year}
        data={data || emptyTeamYearData}
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
            year >= 2016 && `${RPMapping?.[year]?.[0]}`,
            year >= 2016 && `${RPMapping?.[year]?.[1]}`,
            "Wins",
            "Win Rate",
          ].filter(Boolean) as string[]
        }
      />
    ),
    [year, data, filters, setFilters]
  );

  const MemoizedFigureSection = useMemo(
    () => <FigureSection year={year} data={data || emptyTeamYearData} />,
    [year, data]
  );

  const tabs = [
    { title: "Insights", content: MemoizedInsightsTable },
    { title: "Bubble Chart", content: MemoizedBubbleChart },
    { title: "Figures", content: MemoizedFigureSection },
  ];

  return <TabsSection loading={data === undefined} error={error} tabs={tabs} />;
};

export default Tabs;
