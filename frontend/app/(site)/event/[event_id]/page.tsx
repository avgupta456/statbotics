import React from "react";
import { BsTwitch } from "react-icons/bs";

import Image from "next/image";
import Link from "next/link";

import { BACKEND_URL } from "../../../../constants";
import { log, round, truncate } from "../../../../utils";
import NotFound from "../../shared/notFound";
import Tabs from "./tabs";
import { Data } from "./types";

async function getData(event_id: string) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/event/` + event_id, { next: { revalidate: 60 } });
  log(`/event/${event_id} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

// do not cache this page
export const revalidate = 0;

async function Page({ params }: { params: { event_id: string } }) {
  const { event_id } = params;
  const data: Data = await getData(event_id);

  if (!data) {
    return <NotFound type="Event" />;
  }

  let truncatedEventName = truncate(data.event.name, 30);
  const status = data.event.status;

  return (
    <div className="w-full h-full flex-grow flex flex-col pt-4 md:pt-8 md:pb-4 md:px-4">
      <div className="h-full h-full flex-grow flex flex-col">
        <div className="w-full flex items-center justify-center mb-4">
          <p className="text-2xl lg:text-3xl mr-6">
            {data.year.year} {truncatedEventName}
          </p>

          <Link
            href={"https://www.thebluealliance.com/event/" + event_id}
            rel="noopener noreferrer"
            target="_blank"
          >
            <Image src="/tba.png" alt="TBA" height={24} width={24} />
          </Link>
          {status === "Ongoing" && (
            <Link
              href={"https://www.thebluealliance.com/gameday/" + event_id}
              rel="noopener noreferrer"
              target="_blank"
              className="ml-2 text-sm"
              style={{ color: "#6441a5" }}
            >
              <BsTwitch className="text-2xl" />
            </Link>
          )}
        </div>
        <Tabs eventId={event_id} year={data.year.year} data={data} />
      </div>
    </div>
  );
}

export default Page;
