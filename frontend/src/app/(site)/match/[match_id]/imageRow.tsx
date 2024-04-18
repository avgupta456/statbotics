"use client";

import React, { useEffect, useState } from "react";

import Image from "next/image";

import { MatchData } from "../../../../types/data";
import { getMediaUrls } from "../../../../utils";

const ImageRow = ({ data }: { data: MatchData }) => {
  const [media, setMedia] = useState<string[] | null>(null);

  const reverseBlue = [...data?.match?.alliances?.blue?.team_keys].reverse();
  const teams = data?.match?.alliances?.red?.team_keys?.concat(reverseBlue);
  const year = data.year.year;

  useEffect(() => {
    if (teams) {
      getMediaUrls(teams, year).then((data) => {
        setMedia(data);
      });
    }
  }, [teams, year]);

  if (!media || media?.filter((url) => url?.length > 0)?.length === 0) {
    return null;
  }

  return (
    <div className="w-full">
      <p className="text-2xl lg:text-3xl mt-8 mb-4 w-full text-center">Team Photos</p>
      <div className="w-full h-auto flex flex-row flex-wrap justify-center">
        {media?.map((url, index) => {
          return (
            <div className="w-1/3 lg:w-1/6 p-1" key={index}>
              <div className="w-full h-40 relative">
                {url ? (
                  <Image src={url} alt="Team Image" fill className="object-contain" unoptimized />
                ) : (
                  <div className="w-full h-40 flex justify-center items-center text-center">
                    <p>No image available</p>
                  </div>
                )}
              </div>
              <div className="w-full h-8 bg-gray-900 bg-opacity-50 flex justify-center items-center">
                <p className="text-white text-sm">Team {teams[index]}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ImageRow;
