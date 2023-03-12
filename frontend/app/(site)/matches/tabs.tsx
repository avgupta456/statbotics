"use client";

import React, { useMemo } from "react";

import { CURR_YEAR } from "../../../constants";
import TabsSection from "../shared/tabs";
import { MatchData } from "../types";
import UpcomingMatches from "./upcoming";

const Tabs = ({ year, data, error }: { year: number; data: MatchData; error: boolean }) => {
  const MemoizedUpcoming = useMemo(() => <UpcomingMatches data={data} />, [data]);
  const tabs = [year === CURR_YEAR && { title: "Upcoming", content: MemoizedUpcoming }].filter(
    Boolean
  );

  return <TabsSection loading={data === undefined} error={error} tabs={tabs} />;
};

export default Tabs;
