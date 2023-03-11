"use client";

import React, { useMemo } from "react";

import TabsSection from "../shared/tabs";
import { EventData } from "../types";
import Table from "./insightsTable";
import Summary from "./summary";

const Tabs = ({ year, data, error }: { year: number; data: EventData; error: boolean }) => {
  const MemoizedSummary = useMemo(() => <Summary year={year} data={data} />, [year, data]);
  const MemoizedTable = useMemo(() => <Table year={year} data={data} />, [year, data]);
  const tabs = [
    { title: "Summary", content: MemoizedSummary },
    { title: "Table", content: MemoizedTable },
  ];

  return <TabsSection loading={data === undefined} error={error} tabs={tabs} />;
};

export default Tabs;
