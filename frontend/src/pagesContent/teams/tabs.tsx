"use client";

import React, { useMemo } from "react";

import BubbleChart from "../../components/Figures/Bubble";
import { BREAKDOWN_YEARS, CURR_YEAR, RP_NAMES } from "../../constants";
import { TeamYearsData, emptyTeamYearsData } from "../../types/data";
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
  loadAllData,
  setLoadAllData,
}: {
  year: number;
  data: TeamYearsData | undefined;
  error: boolean;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
  loadAllData: boolean;
  setLoadAllData: (loadAllData: boolean) => void;
}) => {
  const MemoizedInsightsTable = useMemo(
    () => (
      <InsightsTable
        year={year}
        data={data || emptyTeamYearsData}
        filters={filters}
        setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
        loadAllData={loadAllData}
        setLoadAllData={setLoadAllData}
      />
    ),
    [year, data, filters, setFilters, loadAllData, setLoadAllData]
  );

  const MemoizedBreakdownTable = useMemo(
    () =>
      BREAKDOWN_YEARS.includes(year) && (
        <BreakdownTable
          year={year}
          data={data || emptyTeamYearsData}
          filters={filters}
          setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
          loadAllData={loadAllData}
          setLoadAllData={setLoadAllData}
        />
      ),
    [year, data, filters, setFilters, loadAllData, setLoadAllData]
  );

  const MemoizedBubbleChart = useMemo(
    () => (
      <BubbleChart
        year={year}
        data={data?.team_years ?? []}
        defaultFilters={{ country: "", state: "", district: "" }}
        filters={filters}
        setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
        loadAllData={loadAllData}
        setLoadAllData={setLoadAllData}
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
    [year, data, filters, setFilters, loadAllData, setLoadAllData]
  );

  const MemoizedFigureSection = useMemo(
    () => <FigureSection year={year} data={data || emptyTeamYearsData} />,
    [year, data]
  );

  const tabs = [
    { title: "Insights", content: MemoizedInsightsTable },
    BREAKDOWN_YEARS.includes(year) && { title: "Breakdown", content: MemoizedBreakdownTable },
    { title: "Bubble Chart", content: MemoizedBubbleChart },
    { title: "Figures", content: MemoizedFigureSection },
  ].filter(Boolean);

  return <TabsSection loading={data === undefined} error={error} tabs={tabs} />;
};

export default Tabs;
