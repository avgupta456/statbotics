"use client";

import React, { useMemo, useState } from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { RPMapping } from "../../../constants";
import { classnames } from "../../../utils";
import { TeamYearData, emptyTeamYearData } from "../types";
import FigureSection from "./figures";
import InsightsTable from "./insightsTable";

const Tabs = ({ year, data }: { year: number; data: TeamYearData | undefined }) => {
  const [tab, setTab] = useState("Insights");

  const MemoizedInsightsTable = useMemo(
    () => <InsightsTable year={year} data={data || emptyTeamYearData} />,
    [year, data]
  );
  const MemoizedBubbleChart = useMemo(
    () => (
      <BubbleChart
        year={year}
        data={data?.team_years ?? []}
        filterOptions={["country", "state", "district"]}
        columnOptions={[
          "Total EPA",
          "Auto",
          "Teleop",
          "Endgame",
          "Auto + Endgame",
          `${RPMapping[year][0]}`,
          `${RPMapping[year][1]}`,
          "Wins",
          "Win Rate",
        ]}
      />
    ),
    [data, year]
  );
  const MemoizedFigureSection = useMemo(
    () => <FigureSection year={year} data={data || emptyTeamYearData} />,
    [year, data]
  );

  return (
    <div className="w-full flex-grow flex flex-col">
      <div className="w-full flex flex-row text-sm md:text-base">
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
      <div className="w-full flex-grow pt-4 px-4 shadow">
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
