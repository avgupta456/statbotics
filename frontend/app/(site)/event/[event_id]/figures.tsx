import { useContext, useState } from "react";

import { BarChart, BarChartNoLegend } from "../../../../components/Figures/Bar";
import EventLineChart from "../../../../components/Figures/EventLine";
import ScatterPlot from "../../../../components/Figures/Scatter";
import { ColorsContext } from "../../../../components/Figures/colors";
import { MAX_TEAM } from "../../../../constants";
import { Data } from "./types";

const FiguresSection = ({ year, eventId, data }: { year: number; eventId: string; data: Data }) => {
  const [showColors, setShowColors] = useState(false);
  const { isLoading: loadingColors } = useContext(ColorsContext);

  const barData = data.team_events
    .map((teamEvent) => ({
      team: teamEvent.num,
      "Total EPA": teamEvent.total_epa,
      "Auto EPA": teamEvent.auto_epa,
      "Teleop EPA": teamEvent.teleop_epa,
      "Endgame EPA": teamEvent.endgame_epa,
      sortEpa: teamEvent.total_epa,
    }))
    .sort((a, b) => b.sortEpa - a.sortEpa)
    .slice(0, 16);

  const lineData = data.team_events
    .filter((teamEvent) => teamEvent.num <= MAX_TEAM) // Filter out offseason teams
    .map((teamEvent) => ({
      value: teamEvent.num,
      label: `${teamEvent.num} | ${teamEvent.team}`,
    }))
    .sort((a, b) => a.value - b.value);

  const scatterData = data.team_events
    .filter((teamEvent) => teamEvent.num <= MAX_TEAM && teamEvent.rank > 0) // Filter out offseason teams
    .map((teamEvent) => ({
      id: teamEvent.num.toString(),
      data: [
        {
          id: teamEvent.num.toString(),
          x: teamEvent.rank,
          y: teamEvent.total_epa,
        },
      ],
    }));

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold mb-4">Top 16 Teams by EPA</div>
      <div className="w-full flex md:hidden">
        <BarChartNoLegend
          data={barData}
          indexBy="team"
          keys={year >= 2016 ? ["Auto EPA", "Teleop EPA", "Endgame EPA"] : ["Total EPA"]}
        />
      </div>
      <div className="w-full hidden md:flex">
        <BarChart
          data={barData}
          indexBy="team"
          keys={year >= 2016 ? ["Auto EPA", "Teleop EPA", "Endgame EPA"] : ["Total EPA"]}
        />
      </div>
      <div className="h-4" />
      <div className="h-4" />
      <div className="flex items-center w-full pt-8 mb-4 border-t-2 border-gray-300">
        <div className="text-2xl font-bold mr-2">Team EPA vs. Rank</div>
        <button
          className="h-10 p-2 rounded bg-gray-100 flex items-center justify-center disabled:cursor-progress disabled:opacity-50 hover:bg-gray-200 disabled:bg-gray-100"
          type="button"
          disabled={loadingColors}
          onClick={() => setShowColors((value) => !value)}
        >
          {showColors ? "Hide" : "Use"} Team Colors
        </button>
      </div>
      <ScatterPlot data={scatterData} axis={"Total EPA"} showColors={showColors} />
      <div className="h-4" />
      <div className="w-full text-2xl font-bold pt-8 mb-4 border-t-2 border-gray-300">
        Team EPA Over Time
      </div>
      <EventLineChart
        eventId={eventId}
        year={data.event.year}
        teamEvents={data.team_events}
        teams={lineData}
      />
    </div>
  );
};

export default FiguresSection;
