"use client";

import React, { useContext } from "react";

import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import { TeamYearData } from "../types";
import Tabs from "./tabs";

const Page = () => {
  const { teamYearDataDict, year, setYear } = useContext(AppContext);
  const data: TeamYearData | undefined = teamYearDataDict[year];

  return (
    <PageLayout title="Teams" year={year} setYear={setYear}>
      <Tabs year={year} data={data} />
    </PageLayout>
  );
};

export default Page;
