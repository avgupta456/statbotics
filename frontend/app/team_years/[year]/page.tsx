import React from "react";

import { BACKEND_URL } from "../../../constants";
import Tabs from "./tabs";
import { Data } from "./types";

async function getData(year: number) {
  const res = await fetch(`${BACKEND_URL}/team_year/` + year);
  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

async function Page({ params }: { params: { year: number } }) {
  const { year } = params;
  console.log("Fetching event data for year: " + year);
  const start = performance.now();
  const data: Data = await getData(year);
  console.log(
    "Fetched event data for year: " +
      year +
      ". Took " +
      Math.round(performance.now() - start) +
      "ms"
  );

  if (!data) {
    return <div>Year not found</div>;
  }

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <p className="text-3xl lg:text-4xl text-gray-800">{year} Team Lookup</p>
        </div>
        <Tabs data={data} />
      </div>
    </div>
  );
}

export default Page;
