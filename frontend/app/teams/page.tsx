"use client";

import React, { useEffect, useState } from "react";
import Select from "react-select";

import { yearOptions } from "../../components/filterConstants";
import { BACKEND_URL } from "../../constants";
import Tabs from "./tabs";
import { Data } from "./types";

async function getData(year: number) {
  const res = await fetch(`${BACKEND_URL}/team_years/` + year);
  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

const Page = () => {
  const [year, setYear] = useState(2022);
  const [dataDict, setDataDict] = useState<{ [key: number]: Data }>({});

  useEffect(() => {
    async function fetchData() {
      if (dataDict[year]) {
        return;
      }

      console.log("Fetching event data for year: " + year);
      const start = performance.now();
      const data: Data = await getData(year);
      console.log(
        "Fetched event data for year: " +
          year +
          ". Took " +
          Math.round(performance.now() - start) +
          "ms"
      );
      setDataDict((prev) => ({ ...prev, [year]: data }));
    }

    fetchData();
  }, [dataDict, year]);

  const data: Data | undefined = dataDict[year];

  return (
    <div className="w-full h-full flex-grow flex flex-col p-4">
      <div className="h-full container mx-auto flex-grow flex flex-col">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <Select
            instanceId={"year-select"}
            className="w-28"
            styles={{
              menu: (provided) => ({ ...provided, zIndex: 9999 }),
            }}
            options={yearOptions}
            onChange={(e) => setYear((e?.value ?? 2023) as number)}
            value={{
              value: year.toString(),
              label: year.toString(),
            }}
          />
          <p className="text-2xl lg:text-3xl text-gray-800 ml-3">Team Lookup</p>
        </div>
        <Tabs year={year} data={data} />
      </div>
    </div>
  );
};

export default Page;
