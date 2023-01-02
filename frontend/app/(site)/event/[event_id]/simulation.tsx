import React, { useEffect, useRef, useState } from "react";

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

  return (
    <div>
      {data.team_events
        .sort((a, b) => rankMean[a.num] - rankMean[b.num])
        .map((teamEvent) => (
          <div key={teamEvent.num} className="flex gap-16">
            <div>{teamEvent.num}</div>
            <div>{teamEvent.team}</div>
            <div>{rankMean[teamEvent.num]}</div>
            <div>{rank5[teamEvent.num]}</div>
            <div>{rank50[teamEvent.num]}</div>
            <div>{rank95[teamEvent.num]}</div>
            <div>{RPMean[teamEvent.num]}</div>
          </div>
        ))}
    </div>
  );
};

export default SimulationSection;
