import React from "react";

import { BACKEND_URL } from "../../../../constants";
import { round, truncate } from "../../../../utils";
import Summary from "./summary";
import MatchTable from "./table";
import { Data } from "./types";
import Video from "./video";

async function getData(match_id: string) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/match/` + match_id);
  console.log(`/match/${match_id} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

async function Page({ params }: { params: { match_id: string } }) {
  const { match_id } = params;
  const data: Data = await getData(match_id);

  if (!data) {
    return <div>Match not found</div>;
  }

  let truncatedEventName = truncate(data.event_name, 30);

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="w-full flex flex-row items-end justify-center mb-4">
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
        <div className="w-full flex flex-row flex-wrap justify-center">
          <Summary data={data} />
          <Video video={data.match.video} />
          <MatchTable data={data} />
        </div>
      </div>
    </div>
  );
}

export default Page;
