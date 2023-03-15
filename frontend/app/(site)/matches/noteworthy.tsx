import React, { useEffect, useState } from "react";

import MatchTable from "../../../components/MatchTable";
import { FilterBar } from "../../../components/filter";
import { APIMatch } from "../../../components/types/api";
import { BACKEND_URL } from "../../../constants";
import { log, round } from "../../../utils";

export type MatchData = {
  high_epa: APIMatch[];
  high_score: APIMatch[];
};

const defaultFilters = {
  country: "",
  state: "",
  district: "",
  playoff: "",
  week: "",
};

async function getMatchData(year, country, state, district, playoff, week) {
  const start = performance.now();
  let suffix = "";
  if (country) suffix += `?country=${country}`;
  if (state) suffix += (suffix ? "&" : "?") + `state=${state}`;
  if (district) suffix += (suffix ? "&" : "?") + `district=${district}`;
  if (playoff) suffix += (suffix ? "&" : "?") + `playoff=${playoff}`;
  if (week) suffix += (suffix ? "&" : "?") + `week=${week}`;

  const res = await fetch(`${BACKEND_URL}/noteworthy_matches/${year}${suffix}`, {
    next: { revalidate: 60 },
  });
  log(`/noteworthy_matches/${year}/ took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }

  return (await res.json())?.data;
}

const NoteworthyMatches = ({ year }: { year: number }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState<MatchData>(null);
  const [filters, setFilters] = useState(defaultFilters);

  useEffect(() => {
    setLoading(true);
    getMatchData(
      year,
      filters.country,
      filters.state,
      filters.district,
      filters.playoff,
      filters.week
    ).then((data) => {
      if (data) {
        setData(data);
      } else {
        setError(true);
      }
      setLoading(false);
    });
  }, [year, filters]);

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
        {data !== null && !loading ? (
          <MatchTable
            year={year}
            teamNum={0}
            matches={data.high_epa}
            foulRate={0}
            showHeaders={true}
            showSubHeaders={false}
            sorted={false}
            showVideo={true}
            stacked={false}
          />
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

  return <div>Noteworthy Matches</div>;
};

export default NoteworthyMatches;
