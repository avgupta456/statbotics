"use client";

import React, { useMemo, useState } from "react";

import { classnames } from "../../../utils";
import FiguresSection from "./figures";
import InsightsTable from "./insightsTable";
import { Data } from "./types";

const Tabs = ({ event_id, data }: { event_id: string; data: Data }) => {
  const [tab, setTab] = useState("Insights");

  const MemoizedInsightsTable = useMemo(() => <InsightsTable data={data} />, [data]);
  const MemoizedFigureSection = useMemo(
    () => <FiguresSection event_id={event_id} data={data} />,
    [event_id, data]
  );

  return (
    <div className="w-full">
      <div className="w-full flex flex-row">
        {["Insights", "Figures"].map((_tab) => (
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
      <div className="w-full flex flex-row flex-wrap justify-center pt-4">
        <div className={tab === "Insights" ? "w-full" : "hidden"}>{MemoizedInsightsTable}</div>
        <div className={tab === "Figures" ? "w-full" : "hidden"}>{MemoizedFigureSection}</div>
      </div>
    </div>
  );
};

export default Tabs;
