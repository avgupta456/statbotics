"use client";

import React, { useEffect, useMemo, useState } from "react";

import { getAllTeams } from "../../../api/header";
import { ShortTeam } from "../../../types/data";
import PageLayout from "../shared/layout";
import TabsSection from "../shared/tabs";
import MultiYear from "./multiYear";
import SingleYear from "./singleYear";

const Tabs = () => {
  const [teams, setTeams] = useState<ShortTeam[]>([]);

  useEffect(() => {
    getAllTeams().then((data) => setTeams(data));
  }, []);

  const MemoizedSingleYear = useMemo(() => <SingleYear teams={teams} />, [teams]);
  const MemoizedMultiYear = useMemo(() => <MultiYear teams={teams} />, [teams]);

  let tabs = [
    { title: "This Year", content: MemoizedSingleYear },
    { title: "All Time", content: MemoizedMultiYear },
  ].filter((tab) => tab.title !== "");

  return (
    <PageLayout title="Compare Teams">
      <TabsSection loading={teams?.length === 0} error={false} tabs={tabs} />
    </PageLayout>
  );
};

export default Tabs;
