import React from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { Data } from "./types";

const FigureSection = ({ data }: { data: Data }) => {
  return (
    <BubbleChart
      data={data.team_years}
      filterOptions={["country", "state", "district"]}
      columnOptions={[
        "Auto EPA",
        "Teleop EPA",
        "Endgame EPA",
        "Auto + Endgame EPA",
        "RP 1 EPA",
        "RP 2 EPA",
        "Total EPA",
        "Wins",
        "Win Rate",
      ]}
    />
  );
};

export default FigureSection;
