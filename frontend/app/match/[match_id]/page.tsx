import React from "react";

import PredTable from "./predTable";
import ResultTable from "./resultTable";
import Summary from "./summary";
import Video from "./video";
import { Data } from "./types";
import { TableKey } from "../../../components/MatchTables";
import { BACKEND_URL } from "../../../constants";

async function getData(match_id: string) {
  const res = await fetch(`${BACKEND_URL}/match/` + match_id);
  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

async function Match({ params }: { params: { match_id: string } }) {
  const { match_id } = params;
  console.log("Fetching match data for match_id: " + match_id);
  const start = performance.now();
  const data: Data = await getData(match_id);
  console.log(
    "Fetched match data for match_id: " +
      match_id +
      ". Took " +
      Math.round(performance.now() - start) +
      "ms"
  );

  if (!data) {
    return <div>Match not found</div>;
  }

  let truncatedEventName = data.event_name;
  if (data.event_name.length > 30) {
    truncatedEventName = data.event_name.slice(0, 27) + "...";
  }

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="flex flex-row items-end mb-4">
          <p className="text-3xl lg:text-4xl">{data.match_name}</p>
          <a
            href={`/event/${data.match.event}`}
            target="_blank"
            rel="noopener noreferrer"
            className="lg:text-2xl ml-2 text-blue-500 hover:text-blue-600 cursor-pointer underline"
          >
            {truncatedEventName}
          </a>
        </div>
        <div className="w-full flex flex-row flex-wrap">
          <Summary data={data} />
          <Video video={data.match.video} />
          <PredTable data={data} />
          <ResultTable data={data} />
        </div>
        <TableKey />
      </div>
    </div>
  );
}

export default Match;
