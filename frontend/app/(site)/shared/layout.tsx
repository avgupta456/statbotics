"use client";

import React from "react";
import Select from "react-select";

import { yearOptions } from "../../../components/filterConstants";

const PageLayout = ({
  title,
  year,
  setYear,
  minYear,
  children,
}: {
  title: string;
  year: number;
  setYear: (year: number) => void;
  minYear?: number;
  children: React.ReactNode;
}) => {
  const filteredYearOptions = yearOptions.filter(
    (option) => parseInt(option.value) >= (minYear ?? 2002)
  );

  return (
    <div className="w-full h-full flex-grow flex flex-col pt-4 md:pt-8 md:pb-4 md:px-4">
      <div className="w-full h-full flex-grow flex flex-col">
        <div className="w-full flex flex-row items-end justify-center mb-4">
          <Select
            instanceId="year-select"
            className="w-28"
            styles={{
              menu: (provided) => ({ ...provided, zIndex: 9999 }),
            }}
            options={filteredYearOptions}
            onChange={(e) => setYear((e?.value ?? 2023) as number)}
            value={{
              value: year.toString(),
              label: year.toString(),
            }}
          />
          <p className="text-2xl lg:text-3xl ml-3">{title}</p>
        </div>
        {children}
      </div>
    </div>
  );
};

export default PageLayout;