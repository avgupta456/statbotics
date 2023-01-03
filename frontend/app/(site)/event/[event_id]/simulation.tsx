"use client";

import React, { useEffect, useRef, useState } from "react";
import { Range } from "react-range";

import SimulationTable from "../../../../components/Table/SimulationTable";
import { Data } from "./types";

type SimResults = {
  index: number;
  simRanks: Record<number, number>;
  simRPs: Record<number, number>;
};

const SimulationSection = ({ data }: { data: Data }) => {
  const [index, setIndex] = useState(0);
  const [finalIndex, setFinalIndex] = useState(0);

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

    workerRef.current.postMessage({
      type: "indexSim",
      data,
      index: finalIndex,
      simCount: 1000,
    });
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

  const qualsN = data.matches.filter((m) => !m.playoff).length;

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
          <strong>{index === 0 ? "Schedule Release" : "Qualification Match " + index}</strong>
        </div>
        <div className="px-16">
          <Range
            step={1}
            min={0}
            max={qualsN}
            values={[index]}
            onChange={(values) => setIndex(values[0])}
            onFinalChange={(values) => {
              setFinalIndex(values[0]);
            }}
            renderTrack={({ props, children }) => (
              <div
                key="slider-track"
                {...props}
                className="w-full h-[2px] pr-2 my-4 bg-gray-200 rounded-md"
              >
                {children}
              </div>
            )}
            renderThumb={({ props }) => (
              <div key="slider-thumb" {...props} className="w-4 h-4 bg-blue-800 rounded-full" />
            )}
            renderMark={({ props }) => (
              <div
                key={`slider-mark-${props.key}`}
                {...props}
                className="w-[2px] h-[2px] bg-blue-500 rounded-full"
              />
            )}
          />
        </div>
      </div>
      <SimulationTable data={simulationData} />
    </div>
  );
};

export default SimulationSection;
