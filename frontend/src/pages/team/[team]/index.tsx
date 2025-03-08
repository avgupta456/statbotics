"use client";

import React, { useEffect } from "react";

import { useParams } from "next/navigation";

import { CURR_YEAR } from "../../../constants";
import PageContent from "../../../pagesContent/team/main";

const Page = () => {
  const { team } = useParams();
  const paramYear = CURR_YEAR;

  useEffect(() => {
    document.title = `Team ${team} - Statbotics`;
  }, [team]);

  return <PageContent team={Number(team)} paramYear={paramYear} />;
};

export default Page;
