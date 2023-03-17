import React, { useEffect, useState } from "react";
import { BsTwitch } from "react-icons/bs";

import Image from "next/image";
import Link from "next/link";

import MatchTable from "../../../components/MatchTable";
import { FilterBar } from "../../../components/filter";
import { APIMatch } from "../../../components/types/api";
import { formatMatch } from "../../../components/utils";
import { BACKEND_URL, CURR_YEAR } from "../../../constants";
import { log, round, truncate } from "../../../utils";

type MatchData = {
  matches: {
    match: APIMatch;
    event_name: string;
  }[];
  foul_rate: number;
};

const UpcomingMatch = ({
  foulRate,
  match,
}: {
  foulRate: number;
  match: { match: APIMatch; event_name: string };
}) => {
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
        {formatMatch(match.match.comp_level, match.match.match_number, match.match.set_number)}
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
          year={CURR_YEAR}
          teamNum={0}
          matches={[match.match]}
          foulRate={foulRate}
          showHeaders={true}
          showSubHeaders={false}
          showVideo={false}
          stacked={true}
        />
      </div>
    </div>
  );
};

const defaultFilters = {
  country: "",
  state: "",
  district: "",
  vbar: "", // draws vertical bar
  playoff: "",
  filterMatches: "",
  sortMatches: "predicted_time",
};

async function getMatchData(country, state, district, playoff, filterMatches, sortMatches) {
  const start = performance.now();
  let suffix = `?limit=20&metric=${sortMatches}`;
  if (filterMatches) suffix += `&minutes=${filterMatches}`;
  if (country) suffix += `&country=${country}`;
  if (state) suffix += `&state=${state}`;
  if (district) suffix += `&district=${district}`;
  if (district === null) suffix += `&district=regionals`;
  if (playoff) suffix += `&playoff=${playoff}`;

  const res = await fetch(`${BACKEND_URL}/upcoming_matches${suffix}`, { next: { revalidate: 60 } });
  log(`/upcoming_matches/ took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }

  return (await res.json())?.data;
}

const UpcomingMatches = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState<MatchData>(null);
  const [filters, setFilters] = useState(defaultFilters);

  useEffect(() => {
    setLoading(true);
    getMatchData(
      filters.country,
      filters.state,
      filters.district,
      filters.playoff,
      filters.filterMatches,
      filters.sortMatches
    ).then((data) => {
      if (data) {
        setData(data);
      } else {
        setError(true);
      }
      setLoading(false);
    });
  }, [filters]);

  if (error) {
    return (
      <div className="w-full flex-grow flex flex-col items-center justify-center">
        <div className="text-gray-700 mt-4">Error loading data</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      <FilterBar defaultFilters={defaultFilters} filters={filters} setFilters={setFilters} />
      <div className="mt-8 flex flex-col gap-8">
        {data && data?.matches?.length > 0 && !loading ? (
          data.matches.map((match) => (
            <UpcomingMatch key={match.match.key} foulRate={data.foul_rate} match={match} />
          ))
        ) : (
          <div className="w-full flex-grow flex flex-col items-center justify-center">
            <div className="text-gray-700 mt-4">
              {loading ? "Loading data, please wait..." : "No upcoming matches"}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UpcomingMatches;
