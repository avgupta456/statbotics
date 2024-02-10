import { useEffect, useState } from "react";
import { BsTwitch } from "react-icons/bs";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/router";

import { getUpcomingMatches } from "../../api/matches";
import MatchTable from "../../components/matchTable";
import { useLocation } from "../../contexts/locationContext";
import { APIMatch } from "../../types/api";
import { CURR_YEAR } from "../../utils/constants";
import { formatMatch, truncate } from "../../utils/formatting";
import MatchesFilterBar from "./filterBar";

type UpcomingMatchObj = {
  match: APIMatch;
  event_name: string;
};

function UpcomingMatch({ match }: { match: UpcomingMatchObj }) {
  const eventId = match.match.event;

  return (
    <div key={match.match.key} className="w-full">
      <div className="mb-2 flex w-full flex-wrap items-center justify-center text-lg">
        <Link
          className="mr-1 cursor-pointer font-bold text-blue-600 underline hover:text-blue-700"
          href={`/event/${eventId}`}
        >
          {truncate(match.event_name, 30)}
        </Link>
        {" - "}
        {formatMatch(match.match.comp_level, match.match.match_number, match.match.set_number)}
        <div className="ml-4 flex">
          <Link
            href={`https://www.thebluealliance.com/event/${eventId}`}
            rel="noopener noreferrer"
            target="_blank"
          >
            <Image src="/tba.png" alt="TBA" height={24} width={24} />
          </Link>
          <Link
            href={`https://www.thebluealliance.com/gameday/${eventId}`}
            rel="noopener noreferrer"
            target="_blank"
            className="ml-2 text-sm"
            style={{ color: "#9146FD" }}
          >
            <BsTwitch className="text-2xl" size={24} />
          </Link>
        </div>
      </div>
      <div className="scrollbar-hide mx-auto w-full overflow-x-scroll md:w-2/3 lg:w-1/2">
        <MatchTable
          year={CURR_YEAR}
          teamNum=""
          matches={[match.match]}
          showHeaders
          showSubHeaders={false}
          showVideo={false}
          stacked
        />
      </div>
    </div>
  );
}

export default function UpcomingMatches() {
  const { isReady } = useRouter();
  const { location } = useLocation();
  const [elim, setElim] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<string | null>(null);
  const [sort, setSort] = useState<string>("time");
  const [refresh, setRefresh] = useState<number>(0);

  const incrementRefresh = () => setRefresh((prev) => prev + 1);

  const [loading, setLoading] = useState<boolean>(true);
  const [data, setData] = useState<UpcomingMatchObj[]>([]);

  useEffect(() => {
    const getData = async () => {
      setLoading(true);
      const upcomingMatches = await getUpcomingMatches(location, elim, timeRange, sort);
      setData(upcomingMatches);
      setLoading(false);
    };
    if (isReady) {
      getData();
    }
  }, [location, elim, timeRange, sort, refresh]);

  return (
    <div>
      <MatchesFilterBar
        elim={elim}
        setElim={setElim}
        timeRange={timeRange}
        setTimeRange={setTimeRange}
        sort={sort}
        setSort={setSort}
        incrementRefresh={incrementRefresh}
      />
      <div className="mt-8 flex flex-col gap-8">
        {data && data?.length > 0 && !loading ? (
          data.map((match) => <UpcomingMatch key={match.match.key} match={match} />)
        ) : (
          <div className="flex w-full flex-grow flex-col items-center justify-center">
            <div className="mt-4">
              {loading ? "Loading data, please wait..." : "No upcoming matches"}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
