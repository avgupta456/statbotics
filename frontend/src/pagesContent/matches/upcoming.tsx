import React, { useEffect, useState } from "react";
import { BsTwitch } from "react-icons/bs";

import Image from "next/image";
import Link from "next/link";

import { getUpcomingMatches } from "../../api/matches";
import MatchTable from "../../components/MatchTable";
import { FilterBar } from "../../components/filterBar";
import { formatMatch } from "../../components/utils";
import { CURR_YEAR } from "../../constants";
import { APIMatch } from "../../types/api";
import { truncate } from "../../utils";

type MatchData = {
  match: APIMatch;
  event_name: string;
}[];

const UpcomingMatch = ({ match }: { match: { match: APIMatch; event_name: string } }) => {
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
  refresh: 0,
};

const UpcomingMatches = ({
  filters,
  setFilters,
}: {
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
}) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState<MatchData>(null);
  const [currFilters, setCurrFilters] = useState({});

  const actualFilters: { [key: string]: any } = Object.keys(defaultFilters).reduce(
    (acc, key) => ({ ...acc, [key]: filters[key] || defaultFilters[key] }),
    {}
  );

  useEffect(() => {
    if (JSON.stringify(currFilters) === JSON.stringify(actualFilters)) {
      return;
    }

    setLoading(true);
    getUpcomingMatches(
      actualFilters.country,
      actualFilters.state,
      actualFilters.district,
      actualFilters.playoff,
      actualFilters.filterMatches,
      actualFilters.sortMatches
    ).then((data) => {
      if (data) {
        setData(data);
        setCurrFilters(actualFilters);
      } else {
        setError(true);
      }
      setLoading(false);
    });
  }, [actualFilters, currFilters]);

  if (error) {
    return (
      <div className="w-full flex-grow flex flex-col items-center justify-center">
        <div className="text-gray-700 mt-4">Error loading data</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      <FilterBar defaultFilters={defaultFilters} filters={actualFilters} setFilters={setFilters} />
      <div className="mt-8 flex flex-col gap-8">
        {data && data?.length > 0 && !loading ? (
          data.map((match) => <UpcomingMatch key={match.match.key} match={match} />)
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
