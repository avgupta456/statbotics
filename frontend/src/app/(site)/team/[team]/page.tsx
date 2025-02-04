"use client";

import React, { useEffect } from "react";

import { CURR_YEAR } from "../../../../constants";
import PageContent from "./main";

// do not cache this page
export const revalidate = 0;

const Page = ({ params }: { params: { team: number } }) => {
  const { team } = params;
  const paramYear = CURR_YEAR;

  useEffect(() => {
    document.title = `Team ${team} - Statbotics`;
  }, [team]);

  return <PageContent team={team} paramYear={paramYear} />;
};

export default Page;
