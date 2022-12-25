import React from "react";

import BarChart from "../../../components/Figures/Bar";
import BubbleChart from "../../../components/Figures/Bubble";
import EventLineChart from "../../../components/Figures/EventLine";
import { Data } from "./types";

const FiguresSection = ({ data }: { data: Data }) => {
  const barData = data.team_events
    .map((teamEvent) => ({
      team: teamEvent.num,
      "Auto EPA": teamEvent.auto_epa,
      "Teleop EPA": teamEvent.teleop_epa,
      "Endgame EPA": teamEvent.endgame_epa,
      sortEpa: teamEvent.total_epa,
    }))
    .sort((a, b) => b.sortEpa - a.sortEpa)
    .slice(0, 16);

  const bubbleData = data.team_events.map((teamEvent) => ({
    ...teamEvent,
    numTeams: data.team_events.length,
  }));

  const lineData = [
    {
      id: "Test",
      data: [
        {
          x: 1,
          y: 2,
        },
        {
          x: 2,
          y: 3,
        },
        {
          x: 3,
          y: 4,
        },
      ],
    },
  ];

  return (
    <div className="w-full h-[1000px] flex flex-col justify-center items-center gap-4">
      <BarChart data={barData} keys={["Auto EPA", "Teleop EPA", "Endgame EPA"]} />
      <BubbleChart
        data={bubbleData}
        filterOptions={[]}
        columnOptions={[
          "Auto",
          "Teleop",
          "Endgame",
          "Auto + Endgame",
          "RP 1",
          "RP 2",
          "Total",
          "Rank",
          "N - Rank",
          "RPs / Match",
          "Wins",
        ]}
      />
      <EventLineChart />
    </div>
  );
};

export default FiguresSection;
