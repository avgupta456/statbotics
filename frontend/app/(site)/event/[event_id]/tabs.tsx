"use client";

import React, { useMemo } from "react";
import Select from "react-select";

import { useRouter } from "next/navigation";

import BubbleChart from "../../../../components/Figures/Bubble";
import {
  CURR_YEAR,
  RPMapping,
  divisionToMainEvent,
  mainEventToDivisions,
} from "../../../../constants";
import TabsSection from "../../shared/tabs";
import AlliancesSection from "./alliances";
import EPABreakdownSection from "./epaBreakdown";
import FiguresSection from "./figures";
import InsightsTable from "./insightsTable";
import MatchSection from "./matches";
import SimulationSection from "./simulation";
import SosSection from "./sos";
import { Data } from "./types";

const Tabs = ({ eventId, year, data }: { eventId: string; year: number; data: Data }) => {
  const router = useRouter();

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

  const MemoizedSosSection = useMemo(
    () => <SosSection eventId={eventId} data={data} />,
    [eventId, data]
  );

  const MemoizedEPABreakdownSection = useMemo(
    () => <EPABreakdownSection year={year} eventId={eventId} data={data} />,
    [year, eventId, data]
  );

  const qualsN = data?.matches?.filter((match) => !match.playoff)?.length || 0;
  const elimsN = data?.matches?.filter((match) => match.playoff)?.length || 0;

  let tabs = [
    { title: "Insights", content: MemoizedInsightsTable },
    { title: "Bubble Chart", content: MemoizedBubbleChart },
    qualsN > 0 && { title: "Qual Matches", content: MemoizedQualMatchSection },
    elimsN > 0 && { title: "Alliances", content: MemoizedAlliancesSection },
    elimsN > 0 && { title: "Elim Matches", content: MemoizedElimMatchSection },
    { title: "Figures", content: MemoizedFigureSection },
    year !== 2015 &&
      (qualsN > 0 || data?.event?.status === "Upcoming") && {
        title: "Simulation",
        content: MemoizedSimulationSection,
      },
    year !== 2015 && qualsN > 0 && { title: "SOS", content: MemoizedSosSection },
    year === 2023 && { title: "EPA Breakdown", content: MemoizedEPABreakdownSection },
  ].filter(Boolean);

  const mainEvent = divisionToMainEvent[eventId];
  const isDivision = mainEvent !== undefined;
  const allDivisions = mainEventToDivisions[mainEvent] || [];
  const currDivision = allDivisions?.filter((division) => division.key === eventId)?.[0] || {};
  const otherDivisions = allDivisions?.filter((division) => division.key !== eventId);

  return (
    <>
      {isDivision && (
        <div className="w-full flex items-center justify-center mb-4 text-sm">
          <p className="mr-2">Other Divisions:</p>
          <Select
            options={otherDivisions?.map((division) => ({
              value: division.key,
              label: division.name,
            }))}
            value={{
              value: currDivision.key,
              label: currDivision.name,
            }}
            onChange={(e) => router.push(`/event/${e.value}`)}
            className="w-40"
          />
        </div>
      )}
      <TabsSection loading={data === undefined} error={false} tabs={tabs} />
    </>
  );
};

export default Tabs;
