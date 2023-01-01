"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";

import BubbleChart from "../../../../components/Figures/Bubble";
import { classnames } from "../../../../utils";
import FiguresSection from "./figures";
import InsightsTable from "./insightsTable";
import MatchSection from "./matches";
import { Data } from "./types";

const Tabs = ({ eventId, data }: { eventId: string; data: Data }) => {
  const [tab, setTab] = useState("Insights");

  const tsWorkerRef = useRef<Worker | null>();
  const [tsWorkerMessages, setTsWorkerMessages] = useState<String[]>([]);

  const appendTsWorkerMessage = (message: string) => {};

  useEffect(() => {
    // From https://webpack.js.org/guides/web-workers/#syntax
    if (tsWorkerRef.current) {
      return;
    }

    tsWorkerRef.current = new Worker(new URL("./ts.worker.ts", import.meta.url));
    tsWorkerRef.current.addEventListener("message", (evt) => {
      console.log("Message from TS worker:", evt.data);
      const newMessages = [...tsWorkerMessages, evt.data];
      setTsWorkerMessages(newMessages);
    });

    tsWorkerRef.current.postMessage({ type: "start" });
  }, [tsWorkerMessages]);

  console.log("TS worker messages:", tsWorkerMessages);

  const MemoizedInsightsTable = useMemo(
    () => <InsightsTable eventId={eventId} data={data} />,
    [eventId, data]
  );

  const MemoizedMatchSection = useMemo(
    () => <MatchSection eventId={eventId} data={data} />,
    [eventId, data]
  );

  const bubbleData = data.team_events.map((teamEvent) => ({
    ...teamEvent,
    numTeams: data.team_events.length,
  }));

  const MemoizedBubbleChart = useMemo(
    () => (
      <BubbleChart
        data={bubbleData}
        filterOptions={[]}
        columnOptions={[
          "Total EPA",
          "Norm EPA",
          "Auto",
          "Teleop",
          "Endgame",
          "Auto + Endgame",
          "RP 1",
          "RP 2",
          "Rank",
          "N - Rank",
          "RPs / Match",
          "Wins",
        ]}
      />
    ),
    [bubbleData]
  );
  const MemoizedFigureSection = useMemo(
    () => <FiguresSection eventId={eventId} data={data} />,
    [eventId, data]
  );

  return (
    <div className="w-full flex-grow flex flex-col">
      <div className="w-full flex flex-row">
        {["Insights", "Matches", "Bubble Chart", "Figures"].map((_tab) => (
          <div
            key={`tab-${_tab}`}
            className={classnames(tab === _tab ? "" : "border-b-[1px] border-gray-200")}
          >
            <button
              className={classnames(
                "border-t-[1px] border-x-[1px] py-2 px-4 rounded-t",
                tab === _tab
                  ? "text-gray-800 border-gray-200"
                  : "text-blue-500 hover:text-blue-600 border-white hover:border-gray-200"
              )}
              onClick={() => setTab(_tab)}
            >
              {_tab}
            </button>
          </div>
        ))}
        <div className="flex-grow border-b-[1px] border-gray-200" />
      </div>
      <div className="w-full flex-grow flex flex-row flex-wrap justify-center pt-4 px-4 shadow">
        {data === undefined ? (
          <div className="w-full flex-grow flex flex-col items-center justify-center">
            <div className="text-gray-700 mt-4">Loading data, please wait...</div>
          </div>
        ) : (
          <>
            <div className={tab === "Insights" ? "w-full" : "hidden"}>{MemoizedInsightsTable}</div>
            <div className={tab === "Matches" ? "w-full" : "hidden"}>{MemoizedMatchSection}</div>
            <div className={tab === "Bubble Chart" ? "w-full" : "hidden"}>
              {MemoizedBubbleChart}
            </div>
            <div className={tab === "Figures" ? "w-full" : "hidden"}>{MemoizedFigureSection}</div>
          </>
        )}
      </div>
    </div>
  );
};

export default Tabs;
