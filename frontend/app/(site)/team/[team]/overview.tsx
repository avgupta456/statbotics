import React from "react";

import { canadaOptions, districtOptions, usaOptions } from "../../../../components/filterConstants";
import { Category10Colors } from "../../../../constants";
import { TeamData, TeamYearData } from "./types";

const rankCard = (rank: number, count: number, label: string) => {
  if (!rank || !count || !label) {
    return null;
  }

  return (
    <div className="w-32 h-auto p-4 flex flex-col justify-center items-center rounded-lg shadow-md bg-gradient-to-br from-blue-400 to-blue-600 hover:from-blue-500 hover:to-blue-700">
      <div className="text-2xl font-bold text-white">{rank}</div>
      <div className="text-sm text-white">{label}</div>
      <div className="text-xs text-white">out of {count}</div>
    </div>
  );
};

const OverviewSection = ({
  teamData,
  teamYearData,
}: {
  teamData: TeamData | undefined;
  teamYearData: TeamYearData | undefined;
}) => {
  if (!teamData || !teamYearData) {
    return (
      <div className="w-full h-auto flex flex-col justify-center items-center px-2">Loading...</div>
    );
  }

  const teamYear = teamYearData.team_year;
  const winrate = ((teamYear.wins + teamYear.ties / 2) / teamYear.count) * 100;

  let state = teamData.state;
  usaOptions.forEach((option) => {
    if (option.value === teamData.state) {
      state = option.label;
    }
  });

  canadaOptions.forEach((option) => {
    if (option.value === teamData.state) {
      state = option.label;
    }
  });

  let district: any = teamData.district;
  districtOptions.forEach((option) => {
    if (option.value === teamData.district) {
      district = option.label;
    }
  });

  if (["Michigan", "Israel", "Indiana", "Texas", "North Carolina", "Ontario"].includes(district)) {
    district = undefined;
  }

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-center">
        Team {teamData.num} went{" "}
        <strong>
          {teamYear.wins}-{teamYear.losses}-{teamYear.ties}
        </strong>{" "}
        ({winrate.toFixed(1)}% winrate)
      </div>
      <div className="w-full text-center mt-2">
        EPA Breakdown:{" "}
        <span style={{ color: Category10Colors[0] }}>
          Auto: <strong>{teamYear.auto_epa.toFixed(2)}</strong>
        </span>{" "}
        |{" "}
        <span style={{ color: Category10Colors[1] }}>
          Teleop: <strong>{teamYear.teleop_epa.toFixed(2)}</strong>
        </span>{" "}
        |{" "}
        <span style={{ color: Category10Colors[2] }}>
          Endgame: <strong>{teamYear.endgame_epa.toFixed(2)}</strong>
        </span>{" "}
        |{" "}
        <span style={{ color: Category10Colors[3] }}>
          RP 1: <strong>{teamYear.rp_1_epa.toFixed(2)}</strong>
        </span>{" "}
        |{" "}
        <span style={{ color: Category10Colors[4] }}>
          RP 2: <strong>{teamYear.rp_2_epa.toFixed(2)}</strong>
        </span>{" "}
        |{" "}
        <span style={{ color: Category10Colors[5] }}>
          Total: <strong>{teamYear.epa.toFixed(2)}</strong>
        </span>
      </div>
      <div className="w-full flex justify-center mt-4 mb-4 gap-4">
        {rankCard(teamYear.epa_rank, teamYear.epa_count, "Worldwide")}
        {rankCard(teamYear.country_epa_rank, teamYear.country_count, teamData.country)}
        {rankCard(teamYear.district_epa_rank, teamYear.district_count, district)}
        {rankCard(teamYear.state_epa_rank, teamYear.state_count, state)}
      </div>
    </div>
  );
};

export default OverviewSection;
