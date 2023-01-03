import React from "react";

import Link from "next/link";

import MatchTable from "../../../../components/MatchTable";
import { canadaOptions, districtOptions, usaOptions } from "../../../../components/filterConstants";
import { Category10Colors, RPMapping } from "../../../../constants";
import { TeamData, TeamYearData } from "./types";

const epaCard = (epa: string, label: string, bg: string) => {
  if (!epa || !label || !bg) {
    return null;
  }

  return (
    <span style={{ backgroundColor: bg }} className="px-2 py-1 rounded text-gray-50 text-sm m-1">
      {label}: <strong>{epa}</strong>
    </span>
  );
};

const rankCard = (rank: number, count: number, label: string) => {
  if (!rank || !count || !label) {
    return null;
  }

  return (
    <div
      style={{ backgroundColor: Category10Colors[0] }}
      className="w-32 h-auto p-2 flex flex-col justify-center items-center rounded-lg"
    >
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

  const year = teamYearData.year;
  const teamYear = teamYearData.team_year;
  const teamEvents = teamYearData.team_events;
  const matches = teamYearData.matches;
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
      <div className="w-full mb-4">
        Team {teamData.num} had a record of{" "}
        <strong>
          {teamYear.wins}-{teamYear.losses}-{teamYear.ties}
        </strong>{" "}
        ({winrate.toFixed(1)}% winrate).
      </div>
      <div className="w-full mb-12">
        EPA Breakdown:
        {epaCard(teamYear?.auto_epa?.toFixed(1), "Auto", Category10Colors[0])}
        {epaCard(teamYear?.teleop_epa?.toFixed(1), "Teleop", Category10Colors[1])}
        {epaCard(teamYear?.endgame_epa?.toFixed(1), "Endgame", Category10Colors[2])}
        {epaCard(teamYear?.rp_1_epa?.toFixed(2), RPMapping[year.year][0], Category10Colors[3])}
        {epaCard(teamYear?.rp_2_epa?.toFixed(2), RPMapping[year.year][1], Category10Colors[4])}
        {epaCard(teamYear?.total_epa?.toFixed(1), "Total", Category10Colors[5])}
      </div>
      <div className="w-full flex justify-center mb-12 gap-4">
        {rankCard(teamYear?.epa_rank, teamYear?.epa_count, "Worldwide")}
        {rankCard(teamYear?.country_epa_rank, teamYear?.country_epa_count, teamData?.country)}
        {rankCard(teamYear?.district_epa_rank, teamYear?.district_epa_count, district)}
        {rankCard(teamYear?.state_epa_rank, teamYear?.state_epa_count, state)}
      </div>
      <div className="w-full h-1 bg-gray-300" />
      {teamEvents.map((event) => {
        const eventMatches = matches
          .filter((match) => match.event === event.event)
          .sort((a, b) => a.time - b.time);
        return (
          <div key={event.event} className="w-full my-4 flex">
            <div className="w-1/4 h-full flex flex-col">
              <div className="flex flex-col mb-2">
                <Link href={`/event/${event.event}`} className="text_link text-xl">
                  {event.event_name}
                </Link>
                Week {event.week}
              </div>
              <div className="flex flex-col mb-2">
                {event.rank > 0 && event.num_teams > 0 && (
                  <div>
                    Rank:{" "}
                    <strong>
                      {event.rank} of {event.num_teams}
                    </strong>
                  </div>
                )}
                {event.count > 0 && (
                  <div>
                    Record:{" "}
                    <strong>
                      {event.wins}-{event.losses}-{event.ties}
                    </strong>
                  </div>
                )}
              </div>
              <div className="flex flex-row flex-wrap mb-2">
                {epaCard(event?.auto_epa?.toFixed(1), "Auto", Category10Colors[0])}
                {epaCard(event?.teleop_epa?.toFixed(1), "Teleop", Category10Colors[1])}
                {epaCard(event?.endgame_epa?.toFixed(1), "Endgame", Category10Colors[2])}
                {epaCard(event?.rp_1_epa?.toFixed(2), RPMapping[year.year][0], Category10Colors[3])}
                {epaCard(event?.rp_2_epa?.toFixed(2), RPMapping[year.year][1], Category10Colors[4])}
                {epaCard(event?.total_epa?.toFixed(1), "Total", Category10Colors[5])}
              </div>
            </div>
            <div className="w-3/4 h-full">
              <MatchTable
                year={year.year}
                teamNum={teamData.num}
                matches={eventMatches}
                foulRate={year.foul_rate}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default OverviewSection;
