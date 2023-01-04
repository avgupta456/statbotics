"use client";

import React, { useMemo } from "react";

import TabsSection from "../shared/tabs";
import { EventData } from "../types";
import Summary from "./summary";

const Tabs = ({ data }: { data: EventData }) => {
  const MemoizedSummary = useMemo(() => <Summary data={data} />, [data]);
  const tabs = [{ title: "Summary", content: MemoizedSummary }];

  return <TabsSection loading={data === undefined} tabs={tabs} />;
};

export default Tabs;
