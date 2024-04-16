import React from "react";

import YearLineChart from "../../../components/Figures/YearLine";
import { TeamYearsData } from "../../../types/data";
import { sortTeamNums } from "../../../utils";

const FigureSection = ({ year, data }: { year: number; data: TeamYearsData }) => {
  const lineData = data.team_years
    .map((teamYear) => ({
      value: teamYear.team,
      label: `${teamYear.team} | ${teamYear.name}`,
    }))
    .sort((a, b) => sortTeamNums(a.value, b.value));

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold mb-4">Team EPA Over Time</div>
      <YearLineChart year={year} teamYears={data.team_years} teams={lineData} />
    </div>
  );
};

export default FigureSection;
