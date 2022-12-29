"use client";

import React, { useMemo, useState } from "react";

import { TeamMatch } from "../../../../components/types/api";
import { classnames } from "../../../../utils";
import FigureSection from "./figures";
import OverviewSection from "./overview";
import { Data } from "./types";

const Tabs = ({
  teamNum,
  year,
  teamData,
  teamYearData,
}: {
  teamNum: number;
  year: number;
  teamData: Data;
  teamYearData: TeamMatch[];
}) => {
  const [tab, setTab] = useState("Overview");

  const MemoizedOverviewSection = useMemo(() => <OverviewSection />, []);

  const MemoizedFigureSection = useMemo(
    () => <FigureSection teamNum={teamNum} teamYearData={teamYearData} />,
    [teamNum, teamYearData]
  );

  return (
    <div className="w-full flex-grow flex flex-col">
      <div className="w-full flex flex-row">
        {["Overview", "Figures"].map((_tab) => (
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
        {teamData === undefined || teamYearData === undefined ? (
          <div className="w-full flex-grow flex flex-col items-center justify-center">
            <div className="text-gray-700 mt-4">Loading data, please wait...</div>
          </div>
        ) : (
          <>
            <div className={tab === "Overview" ? "w-full" : "hidden"}>
              {MemoizedOverviewSection}
            </div>
            <div className={tab === "Figures" ? "w-full" : "hidden"}>{MemoizedFigureSection}</div>
          </>
        )}
      </div>
    </div>
  );
};

export default Tabs;
