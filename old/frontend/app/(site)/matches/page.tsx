import React from "react";

import { validateFilters } from "../../../components/filter";
import PageContent from "./main";

// cache this page for 1 minute
export const revalidate = 60;

export const metadata = {
  title: "Matches - Statbotics",
};

const Page = ({ searchParams: { year, week, country, state, district } }) => {
  const paramFilters = validateFilters(
    { year, week, country, state, district },
    ["year", "week", "country", "state", "district"],
    [undefined, "", "", "", "", ""]
  );

  return <PageContent paramFilters={paramFilters} />;
};

export default Page;
