import React from "react";

import Link from "next/link";

import { BACKEND_URL } from "../../../../constants";
import { log, round, truncate } from "../../../../utils";
import NotFound from "../../shared/notFound";
import ImageRow from "./imageRow";
import Summary from "./summary";
import MatchTable from "./table";
import { Data } from "./types";
import Video from "./video";

async function getData(match_id: string) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/match/` + match_id, { next: { revalidate: 60 } });
  log(`/match/${match_id} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

// do not cache this page
export const revalidate = 0;

async function Page({ params }: { params: { match_id: string } }) {
  const { match_id } = params;
  const data: Data = await getData(match_id);

  if (!data) {
    return <NotFound type="Match" />;
  }

  let truncatedEventName = truncate(data.event.name, 40);

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="w-full flex flex-row flex-wrap items-end justify-center mb-4">
          <p className="text-3xl lg:text-4xl">{data.match.match_name}</p>
          <Link href={`/event/${data.match.event}`} className="lg:text-2xl ml-2 text_link">
            {truncatedEventName}
          </Link>
        </div>
        <div className="w-full flex flex-row flex-wrap justify-center">
          <Summary data={data} />
          <MatchTable data={data} />
          <ImageRow data={data} />
          <Video video={data.match.video} />
        </div>
      </div>
    </div>
  );
}

export default Page;
