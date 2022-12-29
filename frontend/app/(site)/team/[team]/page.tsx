import React from "react";

import { TeamMatch } from "../../../../components/types/api";
import { BACKEND_URL } from "../../../../constants";
import { round } from "../../../../utils";
import Tabs from "./tabs";
import { Data } from "./types";

async function getTeamData(team: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team/${team}`);
  console.log(`/team/${team} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }

  const data = await res.json();
  return data?.data;
}

async function getTeamYearData(team: number, year: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team_year/${year}/${team}`);
  console.log(`/team_year/${year}/${team} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

async function Page({ params }: { params: { team: number } }) {
  const { team } = params;
  const year = 2022;

  // fetch in parallel
  const [teamData, teamYearData]: [Data, TeamMatch[]] = await Promise.all([
    getTeamData(team),
    getTeamYearData(team, year),
  ]);

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <p className="text-2xl lg:text-3xl text-gray-800">
            Team {team} - {teamData?.team}
          </p>
        </div>
        <Tabs teamNum={team} year={year} teamData={teamData} teamYearData={teamYearData} />
      </div>
    </div>
  );
}

export default Page;