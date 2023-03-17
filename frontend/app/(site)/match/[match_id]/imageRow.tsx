"use client";

import React, { useEffect, useState } from "react";

import Image from "next/image";

import { readTBA } from "../../../../utils";
import { Data } from "./types";

const getMediaUrls = async (teams: number[], year: number) => {
  const urls = [];
  for (const team of teams) {
    const data = await readTBA(`/team/frc${team}/media/${year}`);
    const image = data.filter((item: any) => item?.preferred)?.[0];
    urls.push(image?.direct_url ?? null);
  }
  return urls;
};

const ImageRow = ({ data }: { data: Data }) => {
  const [media, setMedia] = useState<string[] | null>(null);

  const reverseBlue = [...data.match.blue].reverse();
  const teams = data.match.red.concat(reverseBlue);
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
                  <Image src={url} alt="Team Image" fill className="object-contain" />
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
