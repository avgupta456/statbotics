"use client";

import React, { useEffect } from "react";

import { CURR_YEAR } from "../../../../../constants";
import PageContent from "../main";

// do not cache this page
export const revalidate = 0;

const Page = ({ params }: { params: { team: number; year: number } }) => {
  let { team, year: paramYear } = params;

  if (paramYear !== -1) {
    paramYear = Math.max(paramYear, 2002);
    paramYear = Math.min(paramYear, CURR_YEAR);
  }

  useEffect(() => {
    document.title = `Team ${team} - Statbotics`;
  }, [team]);

  return <PageContent team={team} paramYear={paramYear} />;
};

export default Page;
