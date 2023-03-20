"use client";

import React, { useMemo } from "react";

import { CURR_YEAR } from "../../../constants";
import TabsSection from "../shared/tabs";
import NoteworthyMatches from "./noteworthy";
import UpcomingMatches from "./upcoming";

const Tabs = ({
  year,
  error,
  filters,
  setFilters,
}: {
  year: number;
  error: boolean;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
}) => {
  const MemoizedUpcoming = useMemo(
    () => (
      <UpcomingMatches
        filters={filters}
        setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
      />
    ),
    [filters, setFilters]
  );
  const MemoizedNoteworthy = useMemo(
    () => (
      <NoteworthyMatches
        year={year}
        filters={filters}
        setFilters={(newFilters) => setFilters({ ...filters, ...newFilters })}
      />
    ),
    [year, filters, setFilters]
  );

  const tabs = [
    year === CURR_YEAR && { title: "Upcoming", content: MemoizedUpcoming },
    { title: "Noteworthy", content: MemoizedNoteworthy },
  ].filter(Boolean);

  return <TabsSection loading={false} error={error} tabs={tabs} />;
};

export default Tabs;
