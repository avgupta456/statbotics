import React from "react";

import BubbleChart from "../../../components/Figures/Bubble";
import { Data } from "./types";

const FigureSection = ({ data }: { data: Data }) => {
  return (
    <BubbleChart
      data={data.team_years}
      filterOptions={["country", "state", "district"]}
      columnOptions={[
        "Auto",
        "Teleop",
        "Endgame",
        "Auto + Endgame",
        "RP 1",
        "RP 2",
        "Total",
        "Wins",
        "Win Rate",
      ]}
    />
  );
};

export default FigureSection;
