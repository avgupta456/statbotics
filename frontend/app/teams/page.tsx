"use client";

import React, { useEffect, useState } from "react";
import Select from "react-select";

import { yearOptions } from "../../components/filterConstants";
import { BACKEND_URL } from "../../constants";
import Tabs from "./tabs";
import { Data } from "./types";

async function getData(year: number) {
  const res = await fetch(`${BACKEND_URL}/team_year/` + year);
  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

const Page = () => {
  const [year, setYear] = useState(2022);
  const [data, setData] = useState<Data | undefined>(undefined);

  // TODO: Store previous data in state so we don't have to refetch

  useEffect(() => {
    async function fetchData() {
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
      setData(data);
    }

    fetchData();
  }, [year]);

  // TODO: Create a loading sreen

  if (!data) {
    return <div>Year not found</div>;
  }

  return (
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
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
          <p className="text-3xl lg:text-4xl text-gray-800 ml-2">Team Lookup</p>
        </div>
        <Tabs year={year} data={data} />
      </div>
    </div>
  );
};

export default Page;
