"use client";

import React, { useMemo } from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { RPMapping } from "../../../constants";
import TabsSection from "../shared/tabs";
import { TeamYearData, emptyTeamYearData } from "../types";
import FigureSection from "./figures";
import InsightsTable from "./insightsTable";

const Tabs = ({ year, data }: { year: number; data: TeamYearData | undefined }) => {
  const MemoizedInsightsTable = useMemo(
    () => <InsightsTable year={year} data={data || emptyTeamYearData} />,
    [year, data]
  );

  const MemoizedBubbleChart = useMemo(
    () => (
      <BubbleChart
        year={year}
        data={data?.team_years ?? []}
        filterOptions={["country", "state", "district"]}
        columnOptions={[
          "Total EPA",
          "Auto",
          "Teleop",
          "Endgame",
          "Auto + Endgame",
          `${RPMapping[year][0]}`,
          `${RPMapping[year][1]}`,
          "Wins",
          "Win Rate",
        ]}
      />
    ),
    [data, year]
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

  return <TabsSection loading={data === undefined} tabs={tabs} />;
};

export default Tabs;
