import React from "react";

import TeamLineChart from "../../../../components/Figures/TeamLine";
import { TeamMatch } from "../../../../components/types/api";

const FigureSection = ({
  teamNum,
  year,
  matches,
}: {
  teamNum: number;
  year: number;
  matches: TeamMatch[];
}) => {
  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold mb-4">EPA Over Time</div>
      <TeamLineChart teamNum={teamNum} year={year} data={matches} />
    </div>
  );
};

export default FigureSection;
