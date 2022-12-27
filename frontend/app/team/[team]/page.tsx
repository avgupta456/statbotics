import React from "react";

import { BACKEND_URL } from "../../../constants";
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
  console.log("Fetching match data for team: " + team);
  const start = performance.now();
  const data: Data = await getData(team);
  console.log(
    "Fetched match data for team: " +
      team +
      ". Took " +
      Math.round(performance.now() - start) +
      "ms"
  );

  if (!data) {
    return <div>Team not found</div>;
  }

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <p className="text-3xl lg:text-4xl">5511 Cortechs Robotics</p>
        </div>
        <div className="w-full flex flex-row flex-wrap justify-center">TODO</div>
      </div>
    </div>
  );
}

export default Page;
