"use client";

import React, { useMemo } from "react";

import BubbleChart from "../../../../components/Figures/Bubble";
import { RPMapping } from "../../../../constants";
import TabsSection from "../../shared/tabs";
import FiguresSection from "./figures";
import InsightsTable from "./insightsTable";
import MatchSection from "./matches";
import SimulationSection from "./simulation";
import { Data } from "./types";

const Tabs = ({ eventId, year, data }: { eventId: string; year: number; data: Data }) => {
  const MemoizedInsightsTable = useMemo(
    () => <InsightsTable eventId={eventId} data={data} />,
    [eventId, data]
  );

  const bubbleData = data.team_events.map((teamEvent) => ({
    ...teamEvent,
    numTeams: data.team_events.length,
  }));

  const MemoizedBubbleChart = useMemo(
    () => (
      <BubbleChart
        year={year}
        data={bubbleData}
        filterOptions={[]}
        columnOptions={[
          "Total EPA",
          "Auto",
          "Teleop",
          "Endgame",
          "Auto + Endgame",
          `${RPMapping[year][0]}`,
          `${RPMapping[year][1]}`,
          "Rank",
          "N - Rank",
          "RPs / Match",
          "Wins",
        ]}
      />
    ),
    [bubbleData, year]
  );

  const MemoizedQualMatchSection = useMemo(
    () => <MatchSection year={year} quals={true} data={data} />,
    [data, year]
  );

  const MemoizedElimMatchSection = useMemo(
    () => <MatchSection year={year} quals={false} data={data} />,
    [data, year]
  );

  const MemoizedFigureSection = useMemo(
    () => <FiguresSection eventId={eventId} data={data} />,
    [eventId, data]
  );

  const MemoizedSimulationSection = useMemo(
    () => <SimulationSection eventId={eventId} data={data} />,
    [eventId, data]
  );

  const qualsN = data?.matches?.filter((match) => !match.playoff)?.length || 0;
  const elimsN = data?.matches?.filter((match) => match.playoff)?.length || 0;

  let tabs = [
    { title: "Insights", content: MemoizedInsightsTable },
    { title: "Bubble Chart", content: MemoizedBubbleChart },
    qualsN > 0
      ? { title: "Qual Matches", content: MemoizedQualMatchSection }
      : { title: "", content: "" },
    elimsN > 0
      ? { title: "Elim Matches", content: MemoizedElimMatchSection }
      : { title: "", content: "" },
    { title: "Figures", content: MemoizedFigureSection },
    { title: "Simulation", content: MemoizedSimulationSection },
  ].filter((tab) => tab.title !== "");

  return <TabsSection tabs={tabs} loading={data === undefined} />;
};

export default Tabs;
