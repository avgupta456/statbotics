import React from "react";

import YearLineChart from "../../../components/Figures/YearLine";
import { Data } from "../types";

const FigureSection = ({ year, data }: { year: number; data: Data }) => {
  const lineData = data.team_years
    .map((teamYear) => ({
      value: teamYear.num,
      label: `${teamYear.num} | ${teamYear.team}`,
    }))
    .sort((a, b) => a.value - b.value);

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold mb-4">Team EPA Over Time</div>
      <YearLineChart year={year} teamYears={data.team_years} teams={lineData} />
    </div>
  );
};

export default FigureSection;
