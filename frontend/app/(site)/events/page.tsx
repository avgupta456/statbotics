import React from "react";

import { validateFilters } from "../../../components/filter";
import PageContent from "./main";

// cache this page for 1 hour
export const revalidate = 60 * 60;

export const metadata = {
  title: "Events - Statbotics",
};

const Page = ({ searchParams: { year, week, country, state, district, search } }) => {
  const paramFilters = validateFilters(
    { year, week, country, state, district, search },
    ["year", "week", "country", "state", "district", "search"],
    [undefined, "", "", "", "", ""]
  );

  return <PageContent paramFilters={paramFilters} />;
};

export default Page;
