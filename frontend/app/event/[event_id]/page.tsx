import React from "react";

import { BACKEND_URL } from "../../../constants";
import { truncate } from "../../../utils";
import Tabs from "./tabs";
import { Data } from "./types";

async function getData(event_id: string) {
  const res = await fetch(`${BACKEND_URL}/event/` + event_id);
  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

async function Page({ params }: { params: { event_id: string } }) {
  const { event_id } = params;
  console.log("Fetching event data for event_id: " + event_id);
  const start = performance.now();
  const data: Data = await getData(event_id);
  console.log(
    "Fetched event data for event_id: " +
      event_id +
      ". Took " +
      Math.round(performance.now() - start) +
      "ms"
  );

  if (!data) {
    return <div>Event not found</div>;
  }

  let truncatedEventName = truncate(data.event_name, 30);

  return (
    <div className="w-full h-full flex-grow flex flex-col p-4">
      <div className="h-full container mx-auto flex-grow flex flex-col">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <p className="text-2xl lg:text-3xl">{truncatedEventName}</p>
        </div>
        <Tabs eventId={event_id} data={data} />
      </div>
    </div>
  );
}

export default Page;
