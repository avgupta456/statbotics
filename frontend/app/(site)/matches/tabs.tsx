"use client";

import React, { useMemo } from "react";

import { CURR_YEAR } from "../../../constants";
import TabsSection from "../shared/tabs";
import UpcomingMatches from "./upcoming";

const Tabs = ({ year, error }: { year: number; error: boolean }) => {
  const MemoizedUpcoming = useMemo(() => <UpcomingMatches />, []);
  const tabs = [year === CURR_YEAR && { title: "Upcoming", content: MemoizedUpcoming }].filter(
    Boolean
  );

  return <TabsSection loading={false} error={error} tabs={tabs} />;
};

export default Tabs;
