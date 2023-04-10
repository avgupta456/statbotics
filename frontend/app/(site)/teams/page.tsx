import React from "react";

import { validateFilters } from "../../../components/filter";
import PageContent from "./main";

// cache this page for 5 minutes
export const revalidate = 60 * 5;

export const metadata = {
  title: "Teams - Statbotics",
};

const Page = ({ searchParams: { year, country, state, district } }) => {
  const paramFilters = validateFilters(
    { year, country, state, district },
    ["year", "country", "state", "district"],
    [undefined, "", "", ""]
  );

  return <PageContent paramFilters={paramFilters} />;
};

export default Page;
