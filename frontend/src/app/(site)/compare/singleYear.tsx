"use client";

import React, { useEffect, useState } from "react";

import { getYearTeamYears } from "../../../api/teams";
import YearLineChart from "../../../components/Figures/YearLine";
import { CURR_YEAR } from "../../../constants";
import { APITeamYear } from "../../../types/api";
import { ShortTeam } from "../../../types/data";

const SingleYear = ({ teams }: { teams: ShortTeam[] }) => {
  const [teamYears, setTeamYears] = useState<APITeamYear[]>([]);

  useEffect(() => {
    getYearTeamYears(CURR_YEAR).then((data) => setTeamYears(data.team_years));
  }, []);

  const lineData = teams
    .filter((team) => team?.active ?? true)
    .map((team) => ({
      value: team.team,
      label: `${team.team} | ${team.name}`,
    }))
    .sort((a, b) => parseInt(a.value) - parseInt(b.value));

  return (
    <div className="mb-4">
      <YearLineChart year={CURR_YEAR} teamYears={teamYears} teams={lineData} />
    </div>
  );
};

export default SingleYear;
