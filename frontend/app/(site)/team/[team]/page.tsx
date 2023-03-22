import React from "react";

import { CURR_YEAR } from "../../../../constants";
import PageContent from "./main";
import { getTeamData } from "./shared";
import { TeamData } from "./types";

// do not cache this page
export const revalidate = 0;

export async function generateMetadata({ params }) {
  console.log("HERE");
  const { team } = params;
  const data: TeamData = await getTeamData(team);
  if (!data) {
    return { title: "Statbotics" };
  } else {
    return { title: `Team ${data.num}: ${data.team} - Statbotics` };
  }
}

const Page = ({ params }: { params: { team: number } }) => {
  const { team } = params;
  const paramYear = CURR_YEAR;

  return <PageContent team={team} paramYear={paramYear} />;
};

export default Page;
