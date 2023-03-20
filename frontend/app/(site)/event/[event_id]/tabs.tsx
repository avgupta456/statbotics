"use client";

import React, { useMemo } from "react";

import BubbleChart from "../../../../components/Figures/Bubble";
import { CURR_YEAR, RPMapping } from "../../../../constants";
import TabsSection from "../../shared/tabs";
import AlliancesSection from "./alliances";
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
        defaultFilters={{}}
        filters={{}}
        setFilters={() => {}}
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
            "Rank",
            "N - Rank",
            "RPs / Match",
            "Wins",
          ].filter(Boolean) as string[]
        }
      />
    ),
    [bubbleData, year]
  );

  const MemoizedQualMatchSection = useMemo(
    () => <MatchSection year={year} quals={true} data={data} />,
    [data, year]
  );

  const MemoizedAlliancesSection = useMemo(
    () => <AlliancesSection year={year} eventId={eventId} data={data} />,
    [year, eventId, data]
  );

  const MemoizedElimMatchSection = useMemo(
    () => <MatchSection year={year} quals={false} data={data} />,
    [data, year]
  );

  const MemoizedFigureSection = useMemo(
    () => <FiguresSection year={year} eventId={eventId} data={data} />,
    [year, eventId, data]
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
      ? { title: "Alliances", content: MemoizedAlliancesSection }
      : { title: "", content: "" },
    elimsN > 0
      ? { title: "Elim Matches", content: MemoizedElimMatchSection }
      : { title: "", content: "" },
    { title: "Figures", content: MemoizedFigureSection },
    year !== 2015 && (qualsN > 0 || data?.event?.status === "Upcoming")
      ? { title: "Simulation", content: MemoizedSimulationSection }
      : { title: "", content: "" },
  ].filter((tab) => tab.title !== "");

  return <TabsSection loading={data === undefined} error={false} tabs={tabs} />;
};

export default Tabs;
