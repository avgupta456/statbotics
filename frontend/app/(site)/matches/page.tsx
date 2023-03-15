"use client";

import React, { useContext, useEffect, useState } from "react";

import { BACKEND_URL, CURR_YEAR } from "../../../constants";
import { log, round } from "../../../utils";
import { getWithExpiry, setWithExpiry } from "../../localStorage";
import { AppContext } from "../context";
import PageLayout from "../shared/layout";
import { EventData } from "../types";
import Tabs from "./tabs";

// cache this page for 1 minute
export const revalidate = 60;

const Page = () => {
  const { year, setYear } = useContext(AppContext);
  const [error, setError] = useState(false);

  useEffect(() => {
    setError(false);
  }, [year]);

  return (
    <PageLayout title="Matches" year={year} setYear={setYear}>
      <Tabs year={year} error={error} />
    </PageLayout>
  );
};

export default Page;
