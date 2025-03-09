"use client";

import React, { useEffect } from "react";

import { useRouter } from "next/router";

import { CURR_YEAR } from "../../../constants";
import SiteLayout from "../../../layouts/siteLayout";
import PageContent from "../../../pagesContent/team/main";

const InnerPage = () => {
  const router = useRouter();
  const { team } = router.query;
  const paramYear = CURR_YEAR;

  useEffect(() => {
    document.title = `Team ${team} - Statbotics`;
  }, [team]);

  return <PageContent team={Number(team)} paramYear={paramYear} />;
};

const Page = () => {
  return (
    <SiteLayout>
      <InnerPage />
    </SiteLayout>
  );
};

export default Page;
