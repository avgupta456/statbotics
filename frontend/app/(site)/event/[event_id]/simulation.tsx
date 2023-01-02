"use client";

import React, { useEffect, useRef, useState } from "react";

import SimulationTable from "../../../../components/Table/SimulationTable";
import { Data } from "./types";

type SimResults = {
  index: number;
  simRanks: Record<number, number>;
  simRPs: Record<number, number>;
};

const SimulationSection = ({ data }: { data: Data }) => {
  const workerRef = useRef<Worker | null>();
  const [workerMessages, setWorkerMessages] = useState<SimResults[]>([]);

  useEffect(() => {
    // From https://webpack.js.org/guides/web-workers/#syntax
    if (workerRef.current || data == null || data == undefined) {
      return;
    }

    workerRef.current = new Worker(new URL("./worker.ts", import.meta.url));
    workerRef.current.addEventListener("message", (evt) => {
      setWorkerMessages([...workerMessages, evt.data]);
    });

    workerRef.current.postMessage({ type: "indexSim", data: data, index: 0, simCount: 1000 });
  }, [workerMessages, data]);

  if (workerMessages.length == 0) {
    return <div>Simulating...</div>;
  }

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

  for (const teamNum of Object.keys(simRanks)) {
    RPMean[teamNum] = simRPs[teamNum].reduce((a, b) => a + b, 0) / simRPs[teamNum].length;

    const sortedRanks = simRanks[teamNum].sort((a, b) => a - b);
    rankMean[teamNum] = sortedRanks.reduce((a, b) => a + b, 0) / sortedRanks.length;
    rank5[teamNum] = sortedRanks[Math.floor(sortedRanks.length * 0.05)];
    rank50[teamNum] = sortedRanks[Math.floor(sortedRanks.length * 0.5)];
    rank95[teamNum] = sortedRanks[Math.floor(sortedRanks.length * 0.95)];
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

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <SimulationTable data={simulationData} />
    </div>
  );
};

export default SimulationSection;
