import React from "react";

import BarChart from "../../../components/Figures/Bar";
import EventLineChart from "../../../components/Figures/EventLine";
import { Data } from "./types";

const FiguresSection = ({ eventId, data }: { eventId: string; data: Data }) => {
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

  const lineData = data.team_events.map((teamEvent) => ({
    value: teamEvent.num,
    label: `${teamEvent.num} | ${teamEvent.team}`,
  }));

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold text-gray-800 mb-4">Top 16 Teams by EPA</div>
      <BarChart data={barData} keys={["Auto EPA", "Teleop EPA", "Endgame EPA"]} />
      <div className="h-4" />
      <div className="w-full text-2xl font-bold text-gray-800 pt-8 mb-4 border-t-2 border-gray-300">
        Team EPA Over Time
      </div>
      <EventLineChart eventId={eventId} teamEvents={data.team_events} teams={lineData} />
    </div>
  );
};

export default FiguresSection;
