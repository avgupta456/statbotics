import React from "react";

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

  return <div className="w-full h-auto flex flex-col justify-center items-center px-2">TODO</div>;
};

export default SummaryOverviewSection;
