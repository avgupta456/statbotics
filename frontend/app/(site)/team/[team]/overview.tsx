import React from "react";

import { TeamData, TeamYearData } from "./types";

const OverviewSection = ({
  teamData,
  teamYearData,
}: {
  teamData: TeamData;
  teamYearData: TeamYearData;
}) => {
  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      {teamYearData.team_year.country_epa_rank}
    </div>
  );
};

export default OverviewSection;
