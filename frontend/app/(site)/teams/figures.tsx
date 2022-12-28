import React from "react";

import YearLineChart from "../../../components/Figures/YearLine";
import { Data } from "../types";

const FigureSection = ({ year, data }: { year: number; data: Data }) => {
  const lineData = data.team_years
    .map((teamEvent) => ({
      value: teamEvent.num,
      label: `${teamEvent.num} | ${teamEvent.team}`,
    }))
    .sort((a, b) => a.value - b.value);

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold text-gray-800 mb-4">Team EPA Over Time</div>
      <YearLineChart year={year} teamYears={data.team_years} teams={lineData} />
    </div>
  );
};

export default FigureSection;
