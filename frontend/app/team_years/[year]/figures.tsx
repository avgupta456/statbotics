import React from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { Data } from "./types";

const FigureSection = ({ data }: { data: Data }) => {
  return <BubbleChart data={data.team_years} yearStats={data.year_stats} />;
};

export default FigureSection;
