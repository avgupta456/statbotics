import React from "react";

import BarChart from "../../../components/Figures/Bar";
import ScatterPlot from "../../../components/Figures/Scatter";
import { Data } from "./types";

const FiguresSection = ({ data }: { data: Data }) => {
  const barData = data.team_events
    .map((teamEvent) => ({
      team: teamEvent.num,
      "Auto EPA": teamEvent.auto_epa,
      "Teleop EPA": teamEvent.teleop_epa,
      "Endgame EPA": teamEvent.endgame_epa,
      sortEpa: teamEvent.epa,
    }))
    .sort((a, b) => b.sortEpa - a.sortEpa)
    .slice(0, 16);

  const scatterData = data.team_events.map((teamEvent) => ({
    id: teamEvent.num,
    data: [{ x: teamEvent.rank, y: teamEvent.epa }],
  }));

  return (
    <div className="w-3/4 h-[1000px] flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-2">Figures</p>
      <BarChart data={barData} keys={["Auto EPA", "Teleop EPA", "Endgame EPA"]} />
      <ScatterPlot data={scatterData} axis="EPA" />
    </div>
  );
};

export default FiguresSection;
