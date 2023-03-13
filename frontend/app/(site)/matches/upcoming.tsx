import React from "react";
import { BsTwitch } from "react-icons/bs";

import Image from "next/image";
import Link from "next/link";

import MatchTable from "../../../components/MatchTable";
import { APIMatch } from "../../../components/types/api";
import { formatMatch } from "../../../components/utils";
import { truncate } from "../../../utils";
import { MatchData } from "../types";

const UpcomingMatches = ({ data }: { data: MatchData }) => {
  return (
    <div className="flex flex-col gap-8">
      {data.upcoming_matches
        .sort((a, b) => a.match.predicted_time - b.match.predicted_time)
        .map((match) => {
          const eventId = match.match.event;

          return (
            <div key={match.match.key} className="w-full">
              <div className="w-full flex flex-wrap items-center justify-center text-lg mb-2">
                <Link
                  className="font-bold mr-1 underline text-blue-600 hover:text-blue-700 cursor-pointer"
                  href={`/event/${eventId}`}
                >
                  {truncate(match.event_name, 30)}
                </Link>
                {" - "}
                {formatMatch(
                  match.match.comp_level,
                  match.match.match_number,
                  match.match.set_number
                )}
                <div className="flex ml-4">
                  <Link
                    href={"https://www.thebluealliance.com/event/" + eventId}
                    rel="noopener noreferrer"
                    target="_blank"
                  >
                    <Image src="/tba.png" alt="TBA" height={24} width={24} />
                  </Link>
                  <Link
                    href={"https://www.thebluealliance.com/gameday/" + eventId}
                    rel="noopener noreferrer"
                    target="_blank"
                    className="ml-2 text-sm"
                    style={{ color: "#9146FD" }}
                  >
                    <BsTwitch className="text-2xl" size={24} />
                  </Link>
                </div>
              </div>
              <div className="w-full md:w-2/3 lg:w-1/2 overflow-x-scroll scrollbar-hide mx-auto">
                <MatchTable
                  year={2023}
                  teamNum={0}
                  matches={[match.match]}
                  foulRate={0}
                  showHeaders={true}
                  showSubHeaders={false}
                  showVideo={false}
                  stacked={true}
                />
              </div>
            </div>
          );
        })}
    </div>
  );
};

export default UpcomingMatches;
