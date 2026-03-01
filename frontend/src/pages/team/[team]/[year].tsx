"use client";

import React, { useEffect } from "react";

import { useRouter } from "next/router";

import { CURR_YEAR } from "../../../constants";
import SiteLayout from "../../../layouts/siteLayout";
import PageContent from "../../../pagesContent/team/main";

const InnerPage = () => {
  const router = useRouter();
  const { team, year: paramYear } = router.query;

  useEffect(() => {
    if (team) {
      document.title = `Team ${team} - Statbotics`;
    }
  }, [team]);

  if (!router.isReady) return null;

  const urlYear =
    paramYear && !Array.isArray(paramYear) && paramYear !== "-1"
      ? Math.min(Math.max(Number(paramYear), 2002), CURR_YEAR)
      : CURR_YEAR;

  return <PageContent team={Number(team)} paramYear={urlYear} />;
};

const Page = () => {
  return (
    <SiteLayout>
      <InnerPage />
    </SiteLayout>
  );
};
export default Page;
