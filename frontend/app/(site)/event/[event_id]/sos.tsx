"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";

import Link from "next/link";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../../components/Table/InsightsTable";
import {
  TeamLink,
  formatCell,
  formatEPACell,
  formatPercentileCell,
} from "../../../../components/Table/shared";
import { formatNumber } from "../../../../components/utils";
import { round } from "../../../../utils";
import { Data } from "./types";

type SosDatum = {
  preSimAvgRank: number;
  simAvgRank: number;
  deltaRank: number;
  rankPercentile: number;
  preSimAvgRP: number;
  simAvgRP: number;
  deltaRP: number;
  rpPercentile: number;
  avgPartnerEPA: number;
  avgOpponentEPA: number;
  deltaEPA: number;
  epaPercentile: number;
  overallPercentile: number;
};

type SosResults = {
  preEventMetrics: Record<number, SosDatum>;
  postEventMetrics: Record<number, SosDatum>;
};

type SosRow = {
  rank: number;
  num: number;
  team: string;
  epa: number;
  rankPercentile: number;
  rpPercentile: number;
  epaPercentile: number;
  overallPercentile: number;
};

const columnHelper = createColumnHelper<SosRow>();
const detailedColumnHelper = createColumnHelper<any>();

const SosSection = ({ eventId, data }: { eventId: string; data: Data }) => {
  const workerRef = useRef<Worker | null>();
  const [workerMessages, setWorkerMessages] = useState<SosResults[]>([]);
  const [preEvent, setPreEvent] = useState(true);
  const [disableHighlight, setDisableHighlight] = useState(false);

  useEffect(() => {
    // From https://webpack.js.org/guides/web-workers/#syntax
    if (workerRef.current) {
      return;
    }

    workerRef.current = new Worker(new URL("./worker.ts", import.meta.url));
    workerRef.current.addEventListener("message", (evt) => {
      setWorkerMessages([...workerMessages, evt.data]);
    });
  }, [workerMessages]);

  useEffect(() => {
    if (!workerRef.current) {
      return;
    }

    setWorkerMessages([]);

    workerRef.current.postMessage({ type: "strengthOfSchedule", data, simCount: 5000 });
  }, [data]);

  const preSimAvgRank = {};
  const simAvgRank = {};
  const deltaRank = {};
  const rankPercentile = {};
  const preSimAvgRP = {};
  const simAvgRP = {};
  const deltaRP = {};
  const rpPercentile = {};
  const avgPartnerEPA = {};
  const avgOpponentEPA = {};
  const deltaEPA = {};
  const epaPercentile = {};
  const overallPercentile = {};
  const epaAdjust = {};

  const simResult = preEvent
    ? workerMessages[0]?.preEventMetrics
    : workerMessages[0]?.postEventMetrics;

  if (simResult) {
    for (const teamNum of Object.keys(simResult)) {
      preSimAvgRank[teamNum] = round(simResult[teamNum].preSimAvgRank, 2);
      simAvgRank[teamNum] = round(simResult[teamNum].simAvgRank, 2);
      deltaRank[teamNum] = round(simResult[teamNum].deltaRank, 2);
      rankPercentile[teamNum] = round(simResult[teamNum].rankPercentile, 2);
      preSimAvgRP[teamNum] = round(simResult[teamNum].preSimAvgRP, 2);
      simAvgRP[teamNum] = round(simResult[teamNum].simAvgRP, 2);
      deltaRP[teamNum] = round(simResult[teamNum].deltaRP, 2);
      rpPercentile[teamNum] = round(simResult[teamNum].rpPercentile, 2);
      avgPartnerEPA[teamNum] = round(simResult[teamNum].avgPartnerEPA, 1);
      avgOpponentEPA[teamNum] = round(simResult[teamNum].avgOpponentEPA, 1);
      deltaEPA[teamNum] = round(simResult[teamNum].deltaEPA, 1);
      epaPercentile[teamNum] = round(simResult[teamNum].epaPercentile, 2);
      overallPercentile[teamNum] = round(simResult[teamNum].overallPercentile, 2);
      epaAdjust[teamNum] = simResult[teamNum].epaAdjust;
    }
  }

  const year = data.event.year;

  const sosData = data.team_events
    .sort((a, b) => a.rank - b.rank)
    .map((teamEvent, i) => ({
      rank: i + 1,
      num: teamEvent.num,
      team: teamEvent.team,
      epa: round(preEvent ? teamEvent.start_total_epa : teamEvent.total_epa, 1),
      preSimAvgRank: preSimAvgRank[teamEvent.num],
      simAvgRank: simAvgRank[teamEvent.num],
      deltaRank: deltaRank[teamEvent.num],
      rankPercentile: rankPercentile[teamEvent.num],
      preSimAvgRP: preSimAvgRP[teamEvent.num],
      simAvgRP: simAvgRP[teamEvent.num],
      deltaRP: deltaRP[teamEvent.num],
      rpPercentile: rpPercentile[teamEvent.num],
      avgPartnerEPA: avgPartnerEPA[teamEvent.num],
      avgOpponentEPA: avgOpponentEPA[teamEvent.num],
      deltaEPA: deltaEPA[teamEvent.num],
      epaPercentile: epaPercentile[teamEvent.num],
      overallPercentile: overallPercentile[teamEvent.num],
    }));

  const columns = useMemo<any>(
    () => [
      columnHelper.accessor("rank", {
        cell: (info) => formatCell(info),
        header: "Rank",
      }),
      columnHelper.accessor("num", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Number",
      }),
      columnHelper.accessor("team", {
        cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
        header: "Team",
      }),
      columnHelper.accessor("epa", {
        cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight),
        header: "EPA",
      }),
      columnHelper.accessor("rpPercentile", {
        cell: (info) => formatPercentileCell(info, disableHighlight),
        header: "RP Score",
      }),
      columnHelper.accessor("rankPercentile", {
        cell: (info) => formatPercentileCell(info, disableHighlight),
        header: "Rank Score",
      }),
      columnHelper.accessor("epaPercentile", {
        cell: (info) => formatPercentileCell(info, disableHighlight),
        header: "EPA Score",
      }),
      columnHelper.accessor("overallPercentile", {
        cell: (info) => formatPercentileCell(info, disableHighlight),
        header: "Composite Score",
      }),
    ],
    [year, data, disableHighlight]
  );

  const detailedColumns = useMemo<any>(
    () => [
      detailedColumnHelper.accessor("rank", {
        cell: (info) => formatCell(info),
        header: "Rank",
      }),
      detailedColumnHelper.accessor("num", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Number",
      }),
      detailedColumnHelper.accessor("team", {
        cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
        header: "Team",
      }),
      detailedColumnHelper.accessor("epa", {
        cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight),
        header: "EPA",
      }),
      detailedColumnHelper.accessor("preSimAvgRP", {
        cell: (info) => formatCell(info),
        header: "Before RP",
      }),
      detailedColumnHelper.accessor("simAvgRP", {
        cell: (info) => formatCell(info),
        header: "After RP",
      }),
      detailedColumnHelper.accessor("deltaRP", {
        cell: (info) => formatCell(info),
        header: "Δ RP",
      }),
      detailedColumnHelper.accessor("rpPercentile", {
        cell: (info) => formatPercentileCell(info, disableHighlight),
        header: "RP Score",
      }),
      detailedColumnHelper.accessor("preSimAvgRank", {
        cell: (info) => formatCell(info),
        header: "Before Rank",
      }),
      detailedColumnHelper.accessor("simAvgRank", {
        cell: (info) => formatCell(info),
        header: "After Rank",
      }),
      detailedColumnHelper.accessor("deltaRank", {
        cell: (info) => formatCell(info),
        header: "Δ Rank",
      }),
      detailedColumnHelper.accessor("rankPercentile", {
        cell: (info) => formatPercentileCell(info, disableHighlight),
        header: "Rank Score",
      }),
      detailedColumnHelper.accessor("avgPartnerEPA", {
        cell: (info) => formatCell(info),
        header: "Partner EPA",
      }),
      detailedColumnHelper.accessor("avgOpponentEPA", {
        cell: (info) => formatCell(info),
        header: "Opponent EPA",
      }),
      detailedColumnHelper.accessor("deltaEPA", {
        cell: (info) => formatCell(info),
        header: "Δ EPA",
      }),
      detailedColumnHelper.accessor("epaPercentile", {
        cell: (info) => formatPercentileCell(info, disableHighlight),
        header: "EPA Score",
      }),
      detailedColumnHelper.accessor("overallPercentile", {
        cell: (info) => formatPercentileCell(info, disableHighlight),
        header: "Composite Score",
      }),
    ],
    [year, data, disableHighlight]
  );

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <div className="w-full text-2xl font-bold mb-4">Strength of Schedule</div>
      <div className="w-full mb-4">
        Using EPA ratings and RP strengths from before and after the event, we estimate the impact
        of each team&apos;s schedule.{" "}
        <strong>The simulation happens live and takes a few seconds to load.</strong> Generally,
        lower scores mean easier schedules, and higher scores mean harder schedules. Read more about
        the methodology{" "}
        <Link href="/blog/sos" className="text_link">
          here
        </Link>
        .
      </div>
      <div className="w-full h-8 mb-4 flex items-center text-sm md:text-base text-center">
        <strong className="mr-2">Using EPAs from:</strong>
        <div
          className="mr-4 flex items-center hover:bg-blue-50 p-1 rounded cursor-pointer"
          onClick={() => setPreEvent(true)}
        >
          <input type="radio" className="radio-sm mr-1 cursor-pointer" checked={preEvent} />
          <span>Before Event</span>
        </div>
        <div
          className="flex items-center hover:bg-blue-50 p-1 rounded cursor-pointer"
          onClick={() => setPreEvent(false)}
        >
          <input type="radio" className="radio-sm mr-1 cursor-pointer" checked={!preEvent} />
          <span>After Event</span>
        </div>
      </div>
      <InsightsTable
        title={"Strength of Schedule"}
        data={sosData}
        columns={columns}
        detailedData={sosData}
        detailedColumns={detailedColumns}
        searchCols={["num", "team"]}
        csvFilename={`${eventId}_sos.csv`}
        includeKey={false}
        toggleDisableHighlight={() => setDisableHighlight(!disableHighlight)}
      />
    </div>
  );
};

export default SosSection;
