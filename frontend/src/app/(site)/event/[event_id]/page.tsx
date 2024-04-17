"use client";

import { useEffect, useState } from "react";
import { BsTwitch } from "react-icons/bs";

import Image from "next/image";
import Link from "next/link";

import { getEvent } from "../../../../api/event";
import { ColorsProvider } from "../../../../components/Figures/colors";
import { EventData } from "../../../../types/data";
import { formatEventName } from "../../../../utils";
import NotFound from "../../shared/notFound";
import Tabs from "./tabs";

// do not cache this page
export const revalidate = 0;

const Page = ({ params }: { params: { event_id: string } }) => {
  const { event_id } = params;

  const hypothetical = event_id.length > 10;
  const [data, setData] = useState<EventData | undefined>();

  useEffect(() => {
    const getEventData = async (event_id: string, hypothetical: boolean) => {
      if (data) {
        return;
      }

      if (hypothetical) {
        // setData(await getHypotheticalData(event_id));
      } else {
        setData(await getEvent(event_id));
      }
    };

    getEventData(event_id, hypothetical);
  }, [event_id, hypothetical, data]);

  useEffect(() => {
    document.title = `${event_id} - Statbotics`;
  }, [event_id]);

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
      <ColorsProvider teams={data?.team_events.map((x) => x.team) ?? []}>
        <Tabs eventId={event_id} year={data.year.year} data={data} />
      </ColorsProvider>
    </div>
  );
};

export default Page;
