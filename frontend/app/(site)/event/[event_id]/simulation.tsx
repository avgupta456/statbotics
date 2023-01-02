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

    workerRef.current.postMessage({ type: "indexSim", data: data, index: 0, simCount: 100 });
  }, [workerMessages, data]);

  if (workerMessages.length == 0) {
    return <div>Simulating...</div>;
  }

  const { simRanks, simRPs } = workerMessages[workerMessages.length - 1]; // TODO: aggregate results

  return (
    <div>
      {data.team_events
        .sort((a, b) => simRanks[a.num] - simRanks[b.num])
        .map((teamEvent) => (
          <div key={teamEvent.num} className="flex gap-16">
            <div>{teamEvent.num}</div>
            <div>{simRanks[teamEvent.num]}</div>
            <div>{simRPs[teamEvent.num]}</div>
          </div>
        ))}
    </div>
  );
};

export default SimulationSection;
