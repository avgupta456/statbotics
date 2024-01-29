import { useEffect, useState } from "react";

import { useLocation } from "../../contexts/locationContext";
import { APIMatch } from "../../types/api";
import MatchesFilterBar from "./filterBar";

export default function NoteworthyMatches() {
  const [week, setWeek] = useState<number | null>(null);
  const { location } = useLocation();
  const [elim, setElim] = useState<string | null>(null);

  const [data, setData] = useState<APIMatch[]>([]);

  useEffect(() => {
    // TODO
    setData([]);
  }, [week, location, elim]);

  // eslint-disable-next-line no-console
  console.log(data);

  return (
    <div>
      <MatchesFilterBar week={week} setWeek={setWeek} elim={elim} setElim={setElim} />
    </div>
  );
}
