"use client";

import { useEffect, useState } from "react";
import { BsTwitch } from "react-icons/bs";

import Image from "next/image";
import Link from "next/link";
import { useParams } from "next/navigation";

import { getEvent } from "../../../../api/event";
import { EventData } from "../../../../types/data";
import { formatEventName } from "../../../../utils";
import NotFound from "../../shared/notFound";
import Tabs from "./tabs";

const Page = () => {
  const { event_id } = useParams();

  const [data, setData] = useState<EventData | undefined>();

  useEffect(() => {
    const fetchEventData = async () => {
      if (!event_id || data) return;

      try {
        const eventData = await getEvent(event_id as string);
        setData(eventData);
      } catch (error) {
        console.error("Error fetching event data:", error);
      }
    };

    fetchEventData();
  }, [event_id, data]);

  useEffect(() => {
    if (event_id) {
      document.title = `${event_id} - Statbotics`;
    }
  }, [event_id]);

  if (!data) {
    return <NotFound type="Event" />;
  }

  const truncatedEventName = formatEventName(data.event.name, 30);
  const status = data.event.status;

  return (
    <div className="w-full h-full flex-grow flex flex-col pt-4 md:pt-8 md:pb-4 md:px-4">
      <div className="w-full flex flex-wrap items-center justify-center mb-4 gap-4">
        <p className="text-2xl lg:text-3xl max-w-full">
          {data.year.year} {truncatedEventName}
        </p>
        <div className="flex">
          <Link
            href={`https://www.thebluealliance.com/event/${event_id}`}
            rel="noopener noreferrer"
            target="_blank"
          >
            <Image src="/tba.png" alt="TBA" height={28} width={28} />
          </Link>

          {status === "Ongoing" && (
            <Link
              href={`https://www.thebluealliance.com/gameday/${event_id}`}
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
      <Tabs eventId={event_id as string} year={data.year.year} data={data} />
    </div>
  );
};

export default Page;
