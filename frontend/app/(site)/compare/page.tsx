import React from "react";

import PageLayout from "../shared/layout";
import Tabs from "./tabs";

export const metadata = {
  title: "Compare Teams - Statbotics",
};

const Page = () => {
  return (
    <PageLayout title="Compare Teams">
      <Tabs />
    </PageLayout>
  );
};

export default Page;
