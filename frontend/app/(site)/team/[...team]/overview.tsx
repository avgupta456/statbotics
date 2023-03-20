import React, { useEffect, useState } from "react";

import Image from "next/image";
import Link from "next/link";

import MatchTable from "../../../../components/MatchTable";
import { canadaOptions, districtOptions, usaOptions } from "../../../../components/filterConstants";
import { CURR_YEAR, Category10Colors } from "../../../../constants";
import { classnames, getMediaUrl } from "../../../../utils";
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
      className="w-32 h-auto p-2 flex flex-col justify-center items-center text-center rounded-lg"
    >
      <div className="text-2xl font-bold text-white">{rank}</div>
      <div className="text-xs md:text-sm text-white">{label}</div>
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
  const [media, setMedia] = useState<string | null>(null);

  useEffect(() => {
    if (teamData && teamYearData) {
      getMediaUrl(teamData.num, teamYearData.year.year).then((data) => {
        console.log(data);
        setMedia(data);
      });
    }
  }, [teamData, teamYearData]);

  if (!teamData || !teamYearData) {
    return (
      <div className="w-full h-auto flex flex-col justify-center items-center px-2">Loading...</div>
    );
  }

  const year = teamYearData.year;
  const teamYear = teamYearData.team_year;
  const teamEvents = teamYearData.team_events;
  const matches = teamYearData.matches;

  if (year.year !== CURR_YEAR && matches.length === 0) {
    return (
      <div className="w-full h-auto flex flex-col justify-center items-center px-2">
        No matches played.
      </div>
    );
  }

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

  if (
    ["Michigan", "Israel", "Indiana", "Texas", "North Carolina", "Ontario", "Regionals"].includes(
      district
    )
  ) {
    district = undefined;
  }

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full flex flex-wrap">
        <div className={classnames("w-full", media && "lg:w-auto lg:flex-grow")}>
          <div className="w-full mb-4">
            Team {teamData.num} ({teamData.team}) had a record of{" "}
            <strong>
              {teamYear.wins}-{teamYear.losses}-{teamYear.ties}
            </strong>{" "}
            in {year.year}.
          </div>
          <div className="w-full mb-8 lg:mb-12 flex flex-wrap items-center">
            EPA Breakdown:
            {year.year >= 2016 ? (
              <>
                {epaCard(teamYear?.auto_epa?.toFixed(1), "Auto", Category10Colors[0])}
                {epaCard(teamYear?.teleop_epa?.toFixed(1), "Teleop", Category10Colors[1])}
                {epaCard(teamYear?.endgame_epa?.toFixed(1), "Endgame", Category10Colors[2])}
                {epaCard(teamYear?.total_epa?.toFixed(1), "Total", Category10Colors[3])}
              </>
            ) : (
              epaCard(teamYear?.total_epa?.toFixed(1), "Total", Category10Colors[0])
            )}
          </div>
          <div className="w-full mb-8 lg:mb-12 flex justify-center gap-2 md:gap-4">
            {rankCard(teamYear?.epa_rank, teamYear?.epa_count, "Worldwide")}
            {rankCard(teamYear?.country_epa_rank, teamYear?.country_epa_count, teamData?.country)}
            {rankCard(teamYear?.district_epa_rank, teamYear?.district_epa_count, district)}
            {rankCard(teamYear?.state_epa_rank, teamYear?.state_epa_count, state)}
          </div>
        </div>
        {media && (
          <div className="h-[250px] w-[300px] mx-auto lg:ml-8 mb-4 relative">
            <Image src={media} alt="Image" fill className="object-contain" />
          </div>
        )}
      </div>
      <div className="w-full h-1 bg-gray-300" />
      {teamEvents
        .filter((event) => !event.offseason)
        .map((event) => {
          const eventMatches = matches
            .filter((match) => match.event === event.event)
            .sort((a, b) => a.time - b.time);
          return (
            <div key={event.event} className="w-full my-4 flex flex-wrap">
              <div className="w-full lg:w-1/4 h-full flex flex-col">
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
                  {year.year >= 2016 ? (
                    <>
                      {epaCard(event?.auto_epa?.toFixed(1), "Auto", Category10Colors[0])}
                      {epaCard(event?.teleop_epa?.toFixed(1), "Teleop", Category10Colors[1])}
                      {epaCard(event?.endgame_epa?.toFixed(1), "Endgame", Category10Colors[2])}
                      {epaCard(event?.total_epa?.toFixed(1), "Total", Category10Colors[3])}
                    </>
                  ) : (
                    epaCard(event?.total_epa?.toFixed(1), "Total", Category10Colors[0])
                  )}
                </div>
              </div>
              <div className="w-full lg:w-3/4 h-full pl-4 overflow-x-scroll lg:overflow-x-auto overflow-y-hidden">
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
