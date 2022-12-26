"use client";

import React, { useMemo, useState } from "react";

import { classnames } from "../../../utils";
import FigureSection from "./figures";
import InsightsTable from "./insightsTable";
import { Data } from "./types";

const Tab = ({ data }: { data: Data }) => {
  const [tab, setTab] = useState("Insights");

  const MemoizedInsightsTable = useMemo(() => <InsightsTable data={data} />, [data]);
  const MemoizedFigureSection = useMemo(() => <FigureSection data={data} />, [data]);

  return (
    <div className="w-full">
      <div className="w-full flex flex-row">
        {["Insights", "Bubble Chart"].map((_tab) => (
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
      <div className="w-full flex flex-row flex-wrap justify-center pt-4 px-4 shadow">
        <div className={tab === "Insights" ? "w-full" : "hidden"}>{MemoizedInsightsTable}</div>
        <div className={tab === "Bubble Chart" ? "w-full" : "hidden"}>{MemoizedFigureSection}</div>
      </div>
    </div>
  );
};

export default Tab;
