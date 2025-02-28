"use client";

import React, { useEffect, useState } from "react";
import { BsArrowLeft, BsArrowRight } from "react-icons/bs";

import Link from "next/link";

import { getMatch } from "../../../../server/match";
import { MatchData } from "../../../../types/data";
import { formatEventName } from "../../../../utils";
import NotFound from "../../shared/notFound";
import ImageRow from "./imageRow";
import Summary from "./summary";
import MatchTable from "./table";
import Video from "./video";

// do not cache this page
export const revalidate = 0;

const Page = ({ params }: { params: { match_id: string } }) => {
  const { match_id } = params;
  const [data, setData] = useState<MatchData | undefined>();

  useEffect(() => {
    const getMatchData = async (match_id: string) => {
      if (data) {
        return;
      }

      setData(await getMatch(match_id));
    };

    getMatchData(match_id);
  }, [match_id, data]);

  useEffect(() => {
    document.title = `${match_id} - Statbotics`;
  }, [match_id]);

  if (!data) {
    return <NotFound type="Match" />;
  }

  let truncatedEventName = formatEventName(data.event.name, 40);

  let prevMatch: string | null = null;
  if (!data.match.elim && data.match.match_number > 1) {
    prevMatch = `${data.match.event}_qm${(data.match.match_number - 1).toString()}`;
  }

  let nextMatch: string | null = null;
  if (!data.match.elim && data.match.match_number < data.event.qual_matches) {
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
};

export default Page;
