"use client";

import React, { useMemo } from "react";

import { EventsData } from "../../../types/data";
import TabsSection from "../shared/tabs";
import Table from "./insightsTable";
import Summary from "./summary";

const Tabs = ({
  data,
  error,
  filters,
  setFilters,
}: {
  data: EventsData;
  error: boolean;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
}) => {
  const MemoizedSummary = useMemo(
    () => (
      <Summary
        data={data}
        filters={filters}
        setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
      />
    ),
    [data, filters, setFilters]
  );
  const MemoizedTable = useMemo(
    () => (
      <Table
        data={data}
        filters={filters}
        setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
      />
    ),
    [data, filters, setFilters]
  );
  const tabs = [
    { title: "Summary", content: MemoizedSummary },
    { title: "Table", content: MemoizedTable },
  ];

  return <TabsSection loading={data === undefined} error={error} tabs={tabs} />;
};

export default Tabs;
