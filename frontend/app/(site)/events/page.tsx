"use client";

import React, { useContext } from "react";

import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import { EventData } from "../types";
import Tabs from "./tabs";

const Page = () => {
  const { eventDataDict, year, setYear } = useContext(AppContext);
  const data: EventData | undefined = eventDataDict[year];

  return (
    <PageLayout title="Events" year={year} setYear={setYear}>
      <Tabs data={data} />
    </PageLayout>
  );
};

export default Page;
