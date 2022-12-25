import React from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { Data } from "./types";

const FigureSection = ({ data }: { data: Data }) => {
  return (
    <div className="w-full flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-2">Figures</p>
      <BubbleChart data={data.team_years} yearStats={data.year_stats} />
    </div>
  );
};

export default FigureSection;
