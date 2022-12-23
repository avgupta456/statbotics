import React from "react";

import BarChart from "../../../components/Figures/Bar";
import { Data } from "./types";

const FiguresSection = ({ data }: { data: Data }) => {
  const epaData = data.team_events
    .map((teamEvent) => ({
      team: teamEvent.num,
      "Auto EPA": teamEvent.auto_epa,
      "Teleop EPA": teamEvent.teleop_epa,
      "Endgame EPA": teamEvent.endgame_epa,
      sortEpa: teamEvent.epa,
    }))
    .sort((a, b) => b.sortEpa - a.sortEpa)
    .slice(0, 16);

  return (
    <div className="w-3/4 h-[500px] flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-2">Figures</p>
      <BarChart data={epaData} keys={["Auto EPA", "Teleop EPA", "Endgame EPA"]} />
    </div>
  );
};

export default FiguresSection;
