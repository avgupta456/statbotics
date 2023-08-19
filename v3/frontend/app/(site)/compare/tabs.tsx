"use client";

import React, { useEffect, useMemo, useState } from "react";

import { BACKEND_URL } from "../../../constants";
import { log, round } from "../../../utils";
import { getWithExpiry, setWithExpiry } from "../../localStorage";
import PageLayout from "../shared/layout";
import TabsSection from "../shared/tabs";
import MultiYear from "./multiYear";
import SingleYear from "./singleYear";

// copied from navbar.tsx
// TODO: consolidate with navbar.tsx
async function getTeamData() {
  const cacheData = getWithExpiry("full_team_list");
  if (cacheData && cacheData?.length > 1000) {
    log("Used Local Storage: Full Team List");
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/teams/all`, { next: { revalidate: 60 } });
  log(`/teams/all took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  setWithExpiry("full_team_list", data, 60 * 60 * 24 * 7); // 1 week expiry
  return data;
}

const Tabs = () => {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    getTeamData().then((data) => setTeams(data));
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
