"use client";

import React, { useMemo } from "react";

import { CURR_YEAR } from "../../../constants";
import TabsSection from "../shared/tabs";
import NoteworthyMatches from "./noteworthy";
import UpcomingMatches from "./upcoming";

const Tabs = ({ year, error }: { year: number; error: boolean }) => {
  const MemoizedUpcoming = useMemo(() => <UpcomingMatches />, []);
  const MemoizedNoteworthy = useMemo(() => <NoteworthyMatches year={year} />, [year]);

  const tabs = [
    year === CURR_YEAR && { title: "Upcoming", content: MemoizedUpcoming },
    { title: "Noteworthy", content: MemoizedNoteworthy },
  ].filter(Boolean);

  return <TabsSection loading={false} error={error} tabs={tabs} />;
};

export default Tabs;
