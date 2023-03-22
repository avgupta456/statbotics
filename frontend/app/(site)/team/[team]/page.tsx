"use client";

import React from "react";

import { CURR_YEAR } from "../../../../constants";
import PageContent from "./main";

// do not cache this page
export const revalidate = 0;

const Page = ({ params }: { params: { team: number } }) => {
  const { team } = params;
  const paramYear = CURR_YEAR;

  return <PageContent team={team} paramYear={paramYear} />;
};

export default Page;
