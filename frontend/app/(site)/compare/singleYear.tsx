"use client";

import React from "react";

import YearLineChart from "../../../components/Figures/YearLine";
import { CURR_YEAR } from "../../../constants";

const SingleYear = ({ teams }: { teams: { [key: string]: any }[] }) => {
  const lineData = teams
    .filter((team) => team?.active ?? true)
    .map((team) => ({
      value: team.num,
      label: `${team.num} | ${team.team}`,
    }))
    .sort((a, b) => a.value - b.value);

  return (
    <div className="mb-4">
      <YearLineChart year={CURR_YEAR} teams={lineData} />
    </div>
  );
};

export default SingleYear;
