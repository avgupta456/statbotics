import React from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { Data } from "./types";

const FigureSection = ({ data }: { data: Data }) => {
  const scatterData = data.team_years.map((teamYear) => ({
    x: teamYear.teleop_epa,
    y: teamYear.auto_epa + teamYear.endgame_epa,
    z: teamYear.endgame_epa,
    num: teamYear.num,
    auto: teamYear.auto_epa,
    total: teamYear.total_epa,
  }));

  return (
    <div className="w-3/4 flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-2">Figures</p>
      <BubbleChart data={scatterData} />
    </div>
  );
};

export default FigureSection;
