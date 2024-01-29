import { useEffect, useState } from "react";

import { useLocation } from "../../contexts/locationContext";
import { APIMatch } from "../../types/api";
import MatchesFilterBar from "./filterBar";

export default function UpcomingMatches() {
  const [week, setWeek] = useState<number | null>(null);
  const { location } = useLocation();
  const [elim, setElim] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<string | null>(null);
  const [sort, setSort] = useState<string>("time");
  const [refresh, setRefresh] = useState<number>(0);

  const incrementRefresh = () => setRefresh((prev) => prev + 1);

  const [data, setData] = useState<APIMatch[]>([]);

  useEffect(() => {
    // TODO
    setData([]);
  }, [week, location, elim, timeRange, sort, refresh]);

  // eslint-disable-next-line no-console
  console.log(data);

  return (
    <div>
      <MatchesFilterBar
        week={week}
        setWeek={setWeek}
        elim={elim}
        setElim={setElim}
        timeRange={timeRange}
        setTimeRange={setTimeRange}
        sort={sort}
        setSort={setSort}
        incrementRefresh={incrementRefresh}
      />
    </div>
  );
}
