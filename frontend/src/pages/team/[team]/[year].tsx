"use client";

import React, { useEffect, useState } from "react";

import { useRouter } from "next/router";

import { CURR_YEAR } from "../../../constants";
import SiteLayout from "../../../layouts/siteLayout";
import PageContent from "../../../pagesContent/team/main";

const InnerPage = () => {
  const router = useRouter();
  const { team, year: paramYear } = router.query;
  const [year, setYear] = useState(CURR_YEAR);

  useEffect(() => {
    if (paramYear && paramYear !== "-1") {
      const numericYear = Math.min(Math.max(Number(paramYear), 2002), CURR_YEAR);
      setYear(numericYear);
    }
  }, [paramYear]);

  useEffect(() => {
    if (team) {
      document.title = `Team ${team} - Statbotics`;
    }
  }, [team]);

  return <PageContent team={Number(team)} paramYear={year} />;
};

const Page = () => {
  return (
    <SiteLayout>
      <InnerPage />
    </SiteLayout>
  );
};
export default Page;
