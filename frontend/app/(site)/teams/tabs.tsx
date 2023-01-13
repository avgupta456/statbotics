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
}: {
  year: number;
  data: TeamYearData | undefined;
  error: boolean;
}) => {
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
        columnOptions={
          [
            "Total EPA",
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

  return <TabsSection loading={data === undefined} error={error} tabs={tabs} />;
};

export default Tabs;
