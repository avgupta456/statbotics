import React from "react";

import LineChart from "../../../../components/Figures/Line";
import { CURR_YEAR } from "../../../../constants";
import { round } from "../../../../utils";
import { TeamData, TeamYearsData } from "./types";

const SummaryOverviewSection = ({
  teamData,
  teamYearsData,
}: {
  teamData: TeamData | undefined;
  teamYearsData: TeamYearsData | undefined;
}) => {
  if (!teamData || !teamYearsData) {
    return (
      <div className="w-full h-auto flex flex-col justify-center items-center px-2">Loading...</div>
    );
  }

  const filteredTeamYearsData = teamYearsData
    .filter((x) => x.year >= teamData.rookie_year && x.year < CURR_YEAR)
    .sort((a, b) => a.year - b.year);

  const xMin = Math.min(...filteredTeamYearsData.map((x) => x.year));
  const xMax = Math.max(...filteredTeamYearsData.map((x) => x.year));

  let roundedYMin = Math.floor(Math.min(...filteredTeamYearsData.map((x) => x.norm_epa)) / 50) * 50;
  roundedYMin = Math.min(1400, Math.max(roundedYMin - 50, 1200));

  let roundedYMax = Math.ceil(Math.max(...filteredTeamYearsData.map((x) => x.norm_epa)) / 50) * 50;
  roundedYMax = Math.min(roundedYMax + 50, 2200);

  let lineData = [
    {
      id: teamData.num.toString(),
      data: filteredTeamYearsData.map((teamYear) => ({
        x: teamYear.year,
        y: round(teamYear.norm_epa, 0),
        label: teamYear.year.toString(),
      })),
    },
    {
      id: "Baseline",
      data: [
        {
          x: xMin,
          y: 1500,
          label: xMin.toString(),
        },
        {
          x: xMax,
          y: 1500,
          label: xMax.toString(),
        },
      ],
    },
  ];

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <LineChart
        data={lineData}
        xAxis="Year"
        yAxis="Norm EPA"
        enableArea
        xMin={xMin}
        xMax={xMax}
        yMin={roundedYMin}
        yMax={roundedYMax}
      />
    </div>
  );
};

export default SummaryOverviewSection;
