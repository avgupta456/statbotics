import React from "react";
import { BsTwitch } from "react-icons/bs";

import Image from "next/image";
import Link from "next/link";

import { BACKEND_URL } from "../../../../constants";
import { formatEventName, log, round } from "../../../../utils";
import NotFound from "../../shared/notFound";
import Tabs from "./tabs";
import { Data } from "./types";

/*
export async function generateMetadata({ params }) {
  const { event_id } = params;
  const data: Data = await getData(event_id);
  if (!data) {
    return { title: "Statbotics" };
  } else {
    return { title: `${data.year.year} ${data.event.name} - Statbotics` };
  }
}
*/

export async function generateMetadata({ params }) {
  const { event_id } = params;
  return { title: `${event_id} - Statbotics` };
}

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

async function getHypotheticalData(event_id: string) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/event/hypothetical/${event_id}`, {
    next: { revalidate: 60 },
  });
  log(`/event/hypothetical/${event_id} took ${round(performance.now() - start, 0)}ms`);

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

  let data: Data | undefined;
  let hypothetical = false;

  if (event_id.length <= 10) {
    data = await getData(event_id);
  } else {
    data = await getHypotheticalData(event_id);
    hypothetical = true;
  }

  if (!data) {
    return <NotFound type="Event" />;
  }

  let truncatedEventName = formatEventName(data.event.name, 30);
  const status = data.event.status;

  return (
    <div className="w-full h-full flex-grow flex flex-col pt-4 md:pt-8 md:pb-4 md:px-4">
      <div className="w-full flex flex-wrap items-center justify-center mb-4 gap-4">
        <p className="text-2xl lg:text-3xl max-w-full">
          {data.year.year} {truncatedEventName}
        </p>
        <div className="flex">
          {!hypothetical && (
            <Link
              href={"https://www.thebluealliance.com/event/" + event_id}
              rel="noopener noreferrer"
              target="_blank"
            >
              <Image src="/tba.png" alt="TBA" height={28} width={28} />
            </Link>
          )}
          {status === "Ongoing" && !hypothetical && (
            <Link
              href={"https://www.thebluealliance.com/gameday/" + event_id}
              rel="noopener noreferrer"
              target="_blank"
              className="ml-2 text-sm"
              style={{ color: "#9146FD" }}
            >
              <BsTwitch className="text-2xl" size={28} />
            </Link>
          )}
        </div>
      </div>
      <Tabs eventId={event_id} year={data.year.year} data={data} />
    </div>
  );
}

export default Page;
