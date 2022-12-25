import React from "react";

import { BACKEND_URL } from "../../../constants";
import FiguresSection from "./figures";
import InsightsTable from "./insightsTable";
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

  let truncatedEventName = data.event_name;
  if (data.event_name.length > 30) {
    truncatedEventName = data.event_name.slice(0, 27) + "...";
  }

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <p className="text-3xl lg:text-4xl">{truncatedEventName}</p>
        </div>
        <div className="w-full flex flex-row flex-wrap justify-center">
          <InsightsTable data={data} />
          <FiguresSection data={data} />
        </div>
      </div>
    </div>
  );
}

export default Page;
