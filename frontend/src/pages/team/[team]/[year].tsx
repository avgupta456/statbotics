"use client";

import React, { useEffect, useState } from "react";

import { useParams } from "next/navigation";

import { CURR_YEAR } from "../../../constants";
import PageContent from "../../../pagesContent/team/main";

const Page = () => {
  const { team, year: paramYear } = useParams();
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

export default Page;
