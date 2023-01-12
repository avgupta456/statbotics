"use client";

import React, { useMemo } from "react";

import TabsSection from "../shared/tabs";
import { EventData } from "../types";
import Summary from "./summary";

const Tabs = ({ data, error }: { data: EventData; error: boolean }) => {
  const MemoizedSummary = useMemo(() => <Summary data={data} />, [data]);
  const tabs = [{ title: "Summary", content: MemoizedSummary }];

  return <TabsSection loading={data === undefined} error={error} tabs={tabs} />;
};

export default Tabs;
