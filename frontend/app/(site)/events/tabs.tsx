"use client";

import React, { useMemo } from "react";

import TabsSection from "../shared/tabs";
import { EventData } from "../types";
import Table from "./insightsTable";
import Summary from "./summary";

const Tabs = ({ data, error }: { data: EventData; error: boolean }) => {
  const MemoizedSummary = useMemo(() => <Summary data={data} />, [data]);
  const MemoizedTable = useMemo(() => <Table data={data} />, [data]);
  const tabs = [
    { title: "Summary", content: MemoizedSummary },
    { title: "Table", content: MemoizedTable },
  ];

  return <TabsSection loading={data === undefined} error={error} tabs={tabs} />;
};

export default Tabs;
