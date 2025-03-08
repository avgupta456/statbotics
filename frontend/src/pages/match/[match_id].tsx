"use client";

import React, { useEffect, useState } from "react";
import { BsArrowLeft, BsArrowRight } from "react-icons/bs";

import Link from "next/link";
import { useParams } from "next/navigation";

import { getMatch } from "../../api/match";
import ImageRow from "../../pagesContent/match/[match_id]/imageRow";
import Summary from "../../pagesContent/match/[match_id]/summary";
import MatchTable from "../../pagesContent/match/[match_id]/table";
import Video from "../../pagesContent/match/[match_id]/video";
import NotFound from "../../pagesContent/shared/notFound";
import { MatchData } from "../../types/data";
import { formatEventName } from "../../utils";

const Page = () => {
  const { match_id } = useParams();
  const [data, setData] = useState<MatchData | undefined>();

  useEffect(() => {
    const fetchMatchData = async () => {
      if (!match_id || data) return;

      try {
        const matchData = await getMatch(match_id as string);
        setData(matchData);
      } catch (error) {
        console.error("Error fetching match data:", error);
      }
    };

    fetchMatchData();
  }, [match_id, data]);

  useEffect(() => {
    if (match_id) {
      document.title = `${match_id} - Statbotics`;
    }
  }, [match_id]);

  if (!data) {
    return <NotFound type="Match" />;
  }

  const truncatedEventName = formatEventName(data.event.name, 40);

  const prevMatch =
    !data.match.elim && data.match.match_number > 1
      ? `${data.match.event}_qm${data.match.match_number - 1}`
      : null;

  const nextMatch =
    !data.match.elim && data.match.match_number < data.event.qual_matches
      ? `${data.match.event}_qm${data.match.match_number + 1}`
      : null;

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
