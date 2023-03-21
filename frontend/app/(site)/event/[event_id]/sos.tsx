"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../../components/Table/InsightsTable";
import { TeamLink, formatCell } from "../../../../components/Table/shared";
import { formatNumber } from "../../../../components/utils";
import { round } from "../../../../utils";
import { Data } from "./types";

type SosResults = Record<
  number,
  {
    deltaRank: number;
    deltaRP: number;
  }
>;

type SosRow = {
  rank: number;
  num: number;
  team: string;
  deltaRank: number;
  deltaRP: number;
};

const columnHelper = createColumnHelper<SosRow>();
const detailedColumnHelper = createColumnHelper<any>();

const SosSection = ({ eventId, data }: { eventId: string; data: Data }) => {
  const workerRef = useRef<Worker | null>();
  const [workerMessages, setWorkerMessages] = useState<SosResults[]>([]);

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

    workerRef.current.postMessage({ type: "strengthOfSchedule", data, simCount: 1000 });
  }, [data]);

  const deltaRank = {};
  const deltaRP = {};

  for (const simResult of workerMessages) {
    for (const teamNum of Object.keys(simResult)) {
      deltaRank[teamNum] = round(simResult[teamNum].deltaRank, 2);
      deltaRP[teamNum] = round(simResult[teamNum].deltaRP, 2);
    }
  }

  const year = data.event.year;

  const sosData = data.team_events
    .sort((a, b) => a.rank - b.rank)
    .map((teamEvent, i) => ({
      rank: i + 1,
      num: teamEvent.num,
      team: teamEvent.team,
      deltaRank: deltaRank[teamEvent.num],
      deltaRP: deltaRP[teamEvent.num],
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
      columnHelper.accessor("deltaRank", {
        cell: (info) => formatCell(info),
        header: "Δ Rank",
      }),
      columnHelper.accessor("deltaRP", {
        cell: (info) => formatCell(info),
        header: "Δ RP",
      }),
    ],
    [year]
  );

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <div className="w-full text-2xl font-bold mb-4">Strength of Schedule</div>
      <div className="w-full mb-4">
        Using EPA ratings and RP strengths from before the event, we estimate the impact of each
        team&apos;s schedule on their final rank and RP.{" "}
        <strong>The simulation happens live and takes a few seconds to load.</strong>
      </div>
      <InsightsTable
        title={"Strength of Schedule"}
        data={sosData}
        columns={columns}
        searchCols={["num", "team"]}
        csvFilename={`${eventId}_sos.csv`}
        includeKey={false}
      />
    </div>
  );
};

export default SosSection;
