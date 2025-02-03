import React from "react";

import TeamLineChart from "../../../../components/Figures/TeamLine";
import { APITeamMatch, APITeamYear } from "../../../../types/api";

const FigureSection = ({
  teamNum,
  year,
  teamYear,
  matches,
}: {
  teamNum: number;
  year: number;
  teamYear: APITeamYear;
  matches: APITeamMatch[];
}) => {
  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold mb-4">EPA Over Time</div>
      <TeamLineChart teamNum={teamNum} year={year} teamYear={teamYear} data={matches} />
    </div>
  );
};

export default FigureSection;
