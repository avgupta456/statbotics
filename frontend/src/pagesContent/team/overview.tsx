import React, { useEffect, useState } from "react";

import Image from "next/image";
import Link from "next/link";

import MatchTable from "../../components/MatchTable";
import { canadaOptions, districtOptions, usaOptions } from "../../components/filterConstants";
import { CURR_YEAR, Category10Colors } from "../../constants";
import { APITeam, APITeamYear } from "../../types/api";
import { TeamYearData } from "../../types/data";
import { classnames, getMediaUrl } from "../../utils";
import { MdAssessment } from "react-icons/md";


type Config = {
  points: {
    [keyToName: string]: string;
  };
  gamepieces: {
    [keyToName: string]: string;
  } | undefined;
};

const pre2016Keys: Config = {
  points: {
    total_points: "Total Points",
  },
  gamepieces: undefined
}

const post2015Keys: Config = {
  points: {
    auto_points: "Auto Points",
    teleop_points: "Teleop Points",
    endgame_points: "Endgame Points",
    total_points: "Total Points",
  },
  gamepieces: undefined
}

const configs: { [key: number]: Config } = {
  2025: {
    points: post2015Keys.points,
    gamepieces: {
      auto_coral: "Auto Coral",
      coral_l1: "L1",
      coral_l2: "L2",
      coral_l3: "L3",
      coral_l4: "L4",
      processor_algae: "Processor",
      net_algae: "Net",
      total_game_pieces: "Total Game Pieces",
    }
  },
  2024: {
    points: post2015Keys.points,
    gamepieces: {
      auto_notes: "Auto Notes",
      speaker_notes: "Speaker",
      amplified_notes: "Amplified Speaker",
      amp_notes: "Amp",
      total_notes: "Total Game Pieces",
    },
  },
};

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

const rankCard = (rank: number, count: number, label: string, filter: string) => {
  if (!rank || !count || !label) {
    return null;
  }

  return (
    <Link
      href={`/teams${filter}`}
      style={{ backgroundColor: Category10Colors[0] }}
      className="w-32 h-auto p-2 flex flex-col justify-center items-center text-center rounded-lg"
    >
      <div className="text-2xl font-bold text-white">{rank}</div>
      <div className="text-xs md:text-sm text-white">{label}</div>
      <div className="text-xs text-white">out of {count}</div>
    </Link>
  );
};

const epaCards = (year: number, breakdown: { [key: string]: number; }, gamepieces: boolean, gamepieceSettingCallback?: (v: boolean) => void, header: boolean = false) => {

  if (!gamepieceSettingCallback) {
    gamepieceSettingCallback = (bool) => { };
  }

  const fallbackConfig = year < 2016 ? pre2016Keys : post2015Keys;
  const config = configs[year] || fallbackConfig;

  const cardTemplates: [string, string][] = []
  if (gamepieces) {
    Object.entries(config.gamepieces || {}).forEach(([key, label]) => {
      const epa = breakdown?.[key]?.toFixed(1) || "0.0";
      cardTemplates.push([epa, label]);
    });
  } else {
    Object.entries(config.points).forEach(([key, label]) => {
      const epa = breakdown?.[key]?.toFixed(1) || "0.0";
      cardTemplates.push([epa, label]);
    });
  }

  var colorIndex = 0;
  const cards = cardTemplates.map(([epa, label]) => {
    const bg = Category10Colors[colorIndex % Category10Colors.length];
    colorIndex++;
    return epaCard(epa, label, bg);
  });

  if (header) {
    const text = gamepieces ? "GP Breakdown" : "EPA Breakdown";
    const swapText = gamepieces ? "Swap to EPA" : "Swap to Gamepieces";
    return (
      <div className="w-full mb-8 lg:mb-12">
        <div className="flex" >
          <div className="tooltip" data-tip={swapText}>
            <MdAssessment
              className="tooltip hover_icon mr-1 cursor-pointer"
              onClick={() => gamepieceSettingCallback(!gamepieces)}
            />
          </div>
          <strong className="h-1 mt-2">{text}: </strong>
        </div>
        <div className="flex flex-row flex-wrap mb-2">{cards}</div>
      </div>
    );
  } else {
    return (
      <div className="flex flex-row flex-wrap mb-2">
        {cards}
      </div>
    );
  }
}

const OverviewSection = ({ teamYearData }: { teamYearData: TeamYearData | undefined }) => {
  const [alliance, setAlliance] = useState<boolean>(true);
  const [gamepieceEpa, setGamepieceEpa] = useState<boolean>(true);
  const [media, setMedia] = useState<string | null>(null);

  const teamNum = teamYearData?.team_year?.team;
  const teamName = teamYearData?.team_year?.name;
  const teamState = teamYearData?.team_year?.state;
  const teamDistrict = teamYearData?.team_year?.district;
  const teamCountry = teamYearData?.team_year?.country;

  useEffect(() => {
    if (teamYearData?.team_year) {
      getMediaUrl(teamNum, teamYearData.year.year).then((data) => setMedia(data));
    }
  }, [teamNum, teamYearData]);

  if (!teamYearData) {
    return (
      <div className="w-full h-auto flex flex-col justify-center items-center px-2">Loading...</div>
    );
  }

  const year = teamYearData.year;
  const teamYear = teamYearData?.team_year;
  const teamEvents = teamYearData?.team_events;
  const matches = teamYearData?.matches || [];

  if (year.year !== CURR_YEAR && matches.length === 0) {
    return (
      <div className="w-full h-auto flex flex-col justify-center items-center px-2">
        No matches played.
      </div>
    );
  }

  let state = teamState;
  usaOptions.forEach((option) => {
    if (option.value === teamState) {
      state = option.label;
    }
  });

  canadaOptions.forEach((option) => {
    if (option.value === teamState) {
      state = option.label;
    }
  });

  let district: any = teamDistrict;
  districtOptions.forEach((option) => {
    if (option.value === teamDistrict) {
      district = option.label;
    }
  });

  if (
    [
      "Michigan",
      "Israel",
      "Indiana",
      "Texas",
      "North Carolina",
      "South Carolina",
      "Ontario",
      "Regionals",
    ].includes(district)
  ) {
    district = undefined;
  }

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full flex flex-wrap">
        <div className={classnames("w-full", media && "lg:w-auto lg:flex-grow")}>
          <div className="w-full mb-4">
            Team {teamNum} ({teamName}) had a record of{" "}
            <strong>
              {teamYear?.record?.wins}-{teamYear?.record?.losses}-{teamYear?.record?.ties}
            </strong>{" "}
            in {year.year}.
          </div>
          {epaCards(teamYear?.year, teamYear?.epa?.breakdown, gamepieceEpa, setGamepieceEpa, true)}
          <div className="w-full mb-8 lg:mb-12 flex justify-center gap-2 md:gap-4">
            {rankCard(
              teamYear?.epa?.ranks?.total?.rank,
              teamYear?.epa?.ranks?.total?.team_count,
              "Worldwide",
              ""
            )}
            {rankCard(
              teamYear?.epa?.ranks?.country?.rank,
              teamYear?.epa?.ranks?.country?.team_count,
              teamCountry,
              `?country=${teamCountry}`
            )}
            {rankCard(
              teamYear?.epa?.ranks?.district?.rank,
              teamYear?.epa?.ranks?.district?.team_count,
              district,
              `?district=${teamDistrict}`
            )}
            {rankCard(
              teamYear?.epa?.ranks?.state?.rank,
              teamYear?.epa?.ranks?.state?.team_count,
              state,
              `?state=${teamState}`
            )}
          </div>
        </div>
        {media && (
          <div className="h-[250px] w-[300px] mx-auto lg:ml-8 mb-4 relative">
            <Image src={media} alt="Image" fill className="object-contain" unoptimized />
          </div>
        )}
      </div>
      <div className="w-full h-1 bg-gray-300" />
      <div className="w-full my-4 flex flex-wrap justify-center items-center">
        <strong className="mr-2">Perspective: </strong>
        <div
          className="mr-4 flex items-center hover:bg-blue-50 p-1 rounded cursor-pointer"
          onClick={() => setAlliance(true)}
        >
          <input
            type="radio"
            className="radio-sm mr-1 cursor-pointer"
            checked={alliance}
            onChange={() => {}}
          />
          <span>Team (Green = Team Won Match)</span>
        </div>
        <div
          className="flex items-center hover:bg-blue-50 p-1 rounded cursor-pointer"
          onClick={() => setAlliance(false)}
        >
          <input
            type="radio"
            className="radio-sm mr-1 cursor-pointer"
            checked={!alliance}
            onChange={() => {}}
          />
          <span>Predicted Winner (Green = Correct Prediction)</span>
        </div>
      </div>
      {teamEvents.map((event) => {
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
                {event?.record?.qual?.rank > 0 && event?.record?.qual?.num_teams > 0 && (
                  <div>
                    Rank:{" "}
                    <strong>
                      {event?.record?.qual?.rank} of {event?.record?.qual?.num_teams}
                    </strong>
                  </div>
                )}
                {event?.record?.total?.count > 0 && (
                  <div>
                    Record:{" "}
                    <strong>
                      {event?.record?.total?.wins}-{event?.record?.total?.losses}-
                      {event?.record?.total?.ties}
                    </strong>
                  </div>
                )}
              </div>
              {epaCards(event?.year, event?.epa?.breakdown, gamepieceEpa)}
            </div>
            <div className="w-full lg:w-3/4 h-full pl-4 overflow-x-scroll lg:overflow-x-auto overflow-y-hidden">
              <MatchTable
                year={year.year}
                teamNum={teamNum}
                matches={eventMatches}
                myAlliance={alliance}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default OverviewSection;
