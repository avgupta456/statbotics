import React from "react";

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

async function Page({ params }: { params: { event_id: string } }) {
  const { event_id } = params;
  const data: Data = await getData(event_id);

  if (!data) {
    return <NotFound type="Event" />;
  }

  let truncatedEventName = truncate(data.event.name, 30);

  return (
    <div className="w-full h-full flex-grow flex flex-col pt-4 md:pt-8 md:pb-4 md:px-4">
      <div className="h-full h-full flex-grow flex flex-col">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <p className="text-2xl lg:text-3xl">
            {data.year.year} {truncatedEventName}
          </p>
        </div>
        <Tabs eventId={event_id} year={data.year.year} data={data} />
      </div>
    </div>
  );
}

export default Page;
