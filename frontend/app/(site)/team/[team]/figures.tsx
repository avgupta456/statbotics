import React from "react";

import TeamLineChart from "../../../../components/Figures/TeamLine";

const FigureSection = ({ year, teamNum }: { year: number; teamNum: number }) => {
  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold mb-4">EPA Over Time</div>
      <TeamLineChart year={year} teamNum={teamNum} />
    </div>
  );
};

export default FigureSection;
