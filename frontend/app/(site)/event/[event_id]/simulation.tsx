"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import { Range } from "react-range";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../../components/Table/InsightsTable";
import { TeamLink, formatCell, formatProbCell } from "../../../../components/Table/shared";
import { formatNumber } from "../../../../components/utils";
import { Data } from "./types";

type SimResults = {
  index: number;
  simRanks: Record<number, number>;
  simRPs: Record<number, number>;
};

type SimulationRow = {
  rank: number;
  num: number;
  team: string;
  rankMean: number;
  rank5: number;
  rank50: number;
  rank95: number;
  RPMean: number;
};

const columnHelper = createColumnHelper<SimulationRow>();
const detailedColumnHelper = createColumnHelper<any>();

const SimulationSection = ({ eventId, data }: { eventId: string; data: Data }) => {
  const qualsN = data.matches.filter((m) => m.status === "Completed" && !m.playoff).length;
  const eventOngoing = data.event.status === "Ongoing";

  const [index, setIndex] = useState(eventOngoing ? qualsN : -1);
  const [finalIndex, setFinalIndex] = useState(eventOngoing ? qualsN : -1);

  const workerRef = useRef<Worker | null>();
  const [workerMessages, setWorkerMessages] = useState<SimResults[]>([]);

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

    if (finalIndex < 0) {
      workerRef.current.postMessage({
        type: "preSim",
        data,
        simCount: 1000,
      });
    } else {
      workerRef.current.postMessage({
        type: "indexSim",
        data,
        index: finalIndex,
        simCount: 1000,
      });
    }
  }, [data, finalIndex]);

  const simRanks = {};
  const simRPs = {};

  for (const simResult of workerMessages) {
    for (const teamNum of Object.keys(simResult.simRanks)) {
      if (simRanks[teamNum] == undefined) {
        simRanks[teamNum] = [];
      }
      simRanks[teamNum].push(...simResult.simRanks[teamNum]);
    }
    for (const teamNum of Object.keys(simResult.simRPs)) {
      if (simRPs[teamNum] == undefined) {
        simRPs[teamNum] = [];
      }
      simRPs[teamNum].push(...simResult.simRPs[teamNum]);
    }
  }

  const RPMean = {};
  const rankMean = {};
  const rank5 = {};
  const rank50 = {};
  const rank95 = {};
  const rankProbs = {};

  const year = data.event.year;
  const N = data.team_events.length;
  const emptyArr = Array(N).fill(0);

  for (const teamNum of Object.keys(simRanks)) {
    RPMean[teamNum] = simRPs[teamNum].reduce((a, b) => a + b, 0) / simRPs[teamNum].length;

    const sortedRanks = simRanks[teamNum].sort((a, b) => a - b);
    rankMean[teamNum] = sortedRanks.reduce((a, b) => a + b, 0) / sortedRanks.length;
    rank5[teamNum] = sortedRanks[Math.floor(sortedRanks.length * 0.05)];
    rank50[teamNum] = sortedRanks[Math.floor(sortedRanks.length * 0.5)];
    rank95[teamNum] = sortedRanks[Math.floor(sortedRanks.length * 0.95)];

    rankProbs[teamNum] = emptyArr.slice();
    for (let i = 0; i < N; i++) {
      rankProbs[teamNum][i] =
        sortedRanks.filter((rank) => rank === i + 1).length / sortedRanks.length;
    }
  }

  const simulationData = data.team_events
    .sort((a, b) => rankMean[a.num] - rankMean[b.num])
    .map((teamEvent, i) => ({
      rank: i + 1,
      num: teamEvent.num,
      team: teamEvent.team,
      rankMean: rankMean[teamEvent.num],
      rank5: rank5[teamEvent.num],
      rank50: rank50[teamEvent.num],
      rank95: rank95[teamEvent.num],
      RPMean: RPMean[teamEvent.num],
    }));

  const detailedSimData = data.team_events
    .sort((a, b) => rankMean[a.num] - rankMean[b.num])
    .map((teamEvent, i) => {
      const probsObj = {};
      for (let i = 0; i < N; i++) {
        probsObj[`prob${i + 1}`] = rankProbs[teamEvent.num]?.[i];
      }

      return {
        num: teamEvent.num,
        team: teamEvent.team,
        rankMean: rankMean[teamEvent.num],
        RPMean: RPMean[teamEvent.num],
        ...probsObj,
      };
    });

  const columns = useMemo<any>(
    () => [
      columnHelper.accessor("rank", {
        cell: (info) => formatCell(info),
        header: "Predicted Rank",
      }),
      columnHelper.accessor("num", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Number",
      }),
      columnHelper.accessor("team", {
        cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
        header: "Team",
      }),
      columnHelper.accessor("rankMean", {
        cell: (info) => formatCell(info),
        header: "Mean Rank",
      }),
      columnHelper.accessor("rank5", {
        cell: (info) => formatCell(info),
        header: "5% Rank",
      }),
      columnHelper.accessor("rank50", {
        cell: (info) => formatCell(info),
        header: "Median Rank",
      }),
      columnHelper.accessor("rank95", {
        cell: (info) => formatCell(info),
        header: "95% Rank",
      }),
      columnHelper.accessor("RPMean", {
        cell: (info) => formatCell(info),
        header: "Mean RPs",
      }),
    ],
    [year]
  );

  const detailedColumns = useMemo<any>(
    () => [
      detailedColumnHelper.accessor("num", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Number",
      }),
      detailedColumnHelper.accessor("team", {
        cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
        header: "Team",
      }),
      detailedColumnHelper.accessor("rankMean", {
        cell: (info) => formatCell(info),
        header: "Mean Rank",
      }),
      detailedColumnHelper.accessor("RPMean", {
        cell: (info) => formatCell(info),
        header: "Mean RPs",
      }),
      ...emptyArr
        .slice()
        .map((_, i) => i + 1)
        .map((i) =>
          detailedColumnHelper.accessor("prob" + i, {
            cell: (info) => formatProbCell(info),
            header: "P(" + i + ")",
          })
        ),
    ],
    [year, emptyArr]
  );

  // TODO: UI to switch between simple and detailed
  // TODO: detailed cumulative vs singular probs

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <div className="w-full text-2xl font-bold mb-4">Simulation</div>
      <div className="w-full mb-4">
        Using EPA ratings and RP strengths from a snapshot in time, we can simulate the remainder of
        the event. The entire event is simulated 1000 times. Surrogates and DQed teams are correctly
        handled. The first tiebreaker is included from 2016 onwards.{" "}
        <strong>The simulation happens live, and may take a few seconds to load.</strong>
      </div>
      <div className="w-full mb-4 flex flex-col">
        <div>
          Simulate from:{" "}
          <strong>
            {index === -1
              ? "Before Schedule Release"
              : index === 0
              ? "Schedule Release"
              : "Qualification Match " + index}
          </strong>
        </div>
        {qualsN > 0 && (
          <div className="px-4 md:px-16">
            <Range
              step={1}
              min={-1}
              max={qualsN}
              values={[index]}
              onChange={(values) => setIndex(values[0])}
              onFinalChange={(values) => {
                setFinalIndex(values[0]);
              }}
              renderTrack={({ props, children }) => (
                <div
                  {...props}
                  key="slider-track"
                  className="w-full h-[10px] pr-2 my-4 bg-gray-100 rounded-full"
                >
                  {children}
                </div>
              )}
              renderThumb={({ props }) => (
                <div {...props} key="slider-thumb" className="w-6 h-6 bg-blue-800 rounded-full" />
              )}
              renderMark={({ props, index }) =>
                index > 0 &&
                index !== qualsN + 1 && (
                  <div
                    {...props}
                    key={`slider-mark-${props.key}`}
                    className="w-[2px] h-[8px] bg-blue-500 rounded-full"
                  />
                )
              }
            />
          </div>
        )}
      </div>
      <InsightsTable
        data={detailedSimData}
        columns={detailedColumns}
        leftCol="rank"
        rightCol="RPMean"
        searchCols={["num", "team"]}
        csvFilename={`${eventId}_simulation.csv`}
        includeKey={false}
      />
    </div>
  );
};

export default SimulationSection;
