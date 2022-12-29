"use client";

import React, { useMemo, useState } from "react";

import { classnames } from "../../../../utils";
import FigureSection from "./figures";
import OverviewSection from "./overview";
import { TeamData, TeamYearData, emptyTeamData, emptyTeamYearData } from "./types";

const Tabs = ({
  teamNum,
  year,
  teamData,
  teamYearData,
  fallbackTeamYearData,
}: {
  teamNum: number;
  year: number;
  teamData: TeamData | undefined;
  teamYearData: TeamYearData | undefined;
  fallbackTeamYearData: TeamYearData | undefined;
}) => {
  const [tab, setTab] = useState("Overview");

  const MemoizedOverviewSection = useMemo(
    () => (
      <OverviewSection
        teamData={teamData || emptyTeamData}
        teamYearData={teamYearData || emptyTeamYearData}
      />
    ),
    [teamData, teamYearData]
  );

  const MemoizedFigureSection = useMemo(() => {
    const matches = teamYearData?.matches || fallbackTeamYearData?.matches || [];
    return (
      <FigureSection
        teamNum={teamNum}
        year={year}
        // creates smooth transition
        matches={matches}
      />
    );
  }, [teamNum, year, teamYearData, fallbackTeamYearData]);

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
        <>
          <div className={tab === "Overview" ? "w-full" : "hidden"}>{MemoizedOverviewSection}</div>
          <div className={tab === "Figures" ? "w-full" : "hidden"}>{MemoizedFigureSection}</div>
        </>
      </div>
    </div>
  );
};

export default Tabs;
