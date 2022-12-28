import React from "react";

import { BACKEND_URL } from "../../../../constants";
import Tabs from "./tabs";
import { Data } from "./types";

async function getData(team: number) {
  const res = await fetch(`${BACKEND_URL}/team/${team}`);
  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

async function Page({ params }: { params: { team: number } }) {
  const { team } = params;
  const year = 2022;

  console.log("Fetching data for team: " + team);
  const start = performance.now();
  const data: Data = await getData(team);
  console.log(
    "Fetched data for team: " + team + ". Took " + Math.round(performance.now() - start) + "ms"
  );

  if (!data) {
    return <div>Team not found</div>;
  }

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <p className="text-2xl lg:text-3xl text-gray-800">
            Team {data.num} - {data.team}
          </p>
        </div>
        <Tabs year={year} data={data} />
      </div>
    </div>
  );
}

export default Page;
