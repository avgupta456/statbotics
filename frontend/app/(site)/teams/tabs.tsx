"use client";

import React, { useMemo, useState } from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { classnames } from "../../../utils";
import { Data, emptyData } from "../types";
import FigureSection from "./figures";
import InsightsTable from "./insightsTable";

const Tabs = ({ year, data }: { year: number; data: Data | undefined }) => {
  const [tab, setTab] = useState("Insights");

  const MemoizedInsightsTable = useMemo(
    () => <InsightsTable year={year} data={data || emptyData} />,
    [year, data]
  );
  const MemoizedBubbleChart = useMemo(
    () => (
      <BubbleChart
        data={data?.team_years ?? []}
        filterOptions={["country", "state", "district"]}
        columnOptions={[
          "Total EPA",
          "Norm EPA",
          "Auto",
          "Teleop",
          "Endgame",
          "Auto + Endgame",
          "RP 1",
          "RP 2",
          "Wins",
          "Win Rate",
        ]}
      />
    ),
    [data]
  );
  const MemoizedFigureSection = useMemo(
    () => <FigureSection year={year} data={data || emptyData} />,
    [year, data]
  );

  return (
    <div className="w-full flex-grow flex flex-col">
      <div className="w-full flex flex-row">
        {["Insights", "Bubble Chart", "Figures"].map((_tab) => (
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
