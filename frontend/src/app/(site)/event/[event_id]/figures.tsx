import { useContext, useState } from "react";

import { BarChart, BarChartNoLegend } from "../../../../components/Figures/Bar";
import EventLineChart from "../../../../components/Figures/EventLine";
import ScatterPlot from "../../../../components/Figures/Scatter";
import { ColorsContext } from "../../../../components/Figures/colors";
import { MAX_TEAM } from "../../../../constants";
import { EventData } from "../../../../types/data";

const FiguresSection = ({
  year,
  eventId,
  data,
}: {
  year: number;
  eventId: string;
  data: EventData;
}) => {
  const [showColors, setShowColors] = useState(false);
  const { isLoading: loadingColors } = useContext(ColorsContext);

  const barData = data.team_events
    .map((teamEvent) => ({
      team: teamEvent.team,
      "Total EPA": teamEvent?.epa.breakdown?.total_points?.mean ?? 0,
      "Auto EPA": teamEvent?.epa.breakdown?.auto_points?.mean ?? 0,
      "Teleop EPA": teamEvent?.epa.breakdown?.teleop_points?.mean ?? 0,
      "Endgame EPA": teamEvent?.epa.breakdown?.endgame_points?.mean ?? 0,
      sortEpa: teamEvent?.epa.breakdown?.total_points?.mean ?? 0,
    }))
    .sort((a, b) => b.sortEpa - a.sortEpa)
    .slice(0, 16);

  const lineData = data.team_events // Filter out offseason teams
    .filter((teamEvent) => parseInt(teamEvent.team) <= MAX_TEAM)
    .map((teamEvent) => ({
      value: teamEvent.team,
      label: `${teamEvent.team} | ${teamEvent.team}`,
    }))
    .sort((a, b) => (a.value > b.value ? 1 : -1));

  const scatterData = data.team_events // Filter out offseason teams
    .filter((teamEvent) => parseInt(teamEvent.team) <= MAX_TEAM && teamEvent.record.qual.rank > 0)
    .map((teamEvent) => ({
      id: teamEvent.team,
      data: [
        {
          id: teamEvent.team,
          x: teamEvent.record.qual.rank,
          y: teamEvent.epa.breakdown.total_points,
        },
      ],
    }));

  console.log(scatterData);

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
