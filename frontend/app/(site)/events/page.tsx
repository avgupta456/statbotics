"use client";

import React, { useContext } from "react";
import Select from "react-select";

import { yearOptions } from "../../../components/filterConstants";
import { AppContext } from "../context";
// store types in (site) root so layout can access them
import { EventData } from "../types";
import Tabs from "./tabs";

const Page = () => {
  const { eventDataDict, year, setYear } = useContext(AppContext);
  const data: EventData | undefined = eventDataDict[year];

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
          <p className="text-2xl lg:text-3xl ml-4">Event Lookup</p>
        </div>
        <Tabs data={data} />
      </div>
    </div>
  );
};

export default Page;
