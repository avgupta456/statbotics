import React from "react";
import { BsArrowLeft, BsArrowRight } from "react-icons/bs";

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

  let prevMatch: string | null = null;
  if (!data.match.playoff && data.match.match_number > 1) {
    prevMatch = `${data.match.event}_qm${(data.match.match_number - 1).toString()}`;
  }

  let nextMatch: string | null = null;
  if (!data.match.playoff && data.match.match_number < data.event.qual_matches) {
    nextMatch = `${data.match.event}_qm${(data.match.match_number + 1).toString()}`;
  }

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="w-full flex flex-row justify-center items-center mb-4">
          {prevMatch ? (
            <Link href={`/match/${prevMatch}`} className="mr-16">
              <BsArrowLeft className="text-3xl lg:text-4xl text_link" />
            </Link>
          ) : (
            <BsArrowLeft className="text-3xl lg:text-4xl text-white mr-16" />
          )}
          <div className="flex flex-row flex-wrap items-end justify-center">
            <p className="text-3xl lg:text-4xl">{data.match.match_name}</p>
            <Link href={`/event/${data.match.event}`} className="lg:text-2xl ml-2 text_link">
              {truncatedEventName}
            </Link>
          </div>
          {nextMatch ? (
            <Link href={`/match/${nextMatch}`} className="ml-16">
              <BsArrowRight className="text-3xl lg:text-4xl text_link" />
            </Link>
          ) : (
            <BsArrowRight className="text-3xl lg:text-4xl text-white ml-16" />
          )}
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
