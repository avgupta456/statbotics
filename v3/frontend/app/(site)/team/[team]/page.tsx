import React from "react";

import { CURR_YEAR } from "../../../../constants";
import PageContent from "./main";

/*
export async function generateMetadata({ params }) {
  const { team } = params;
  const data: TeamData = await getTeamData(team);
  if (!data) {
    return { title: "Statbotics" };
  } else {
    return { title: `Team ${data.num} - ${data.team} - Statbotics` };
  }
}
*/

export async function generateMetadata({ params }) {
  const { team } = params;
  return { title: `Team ${team} - Statbotics` };
}

// do not cache this page
export const revalidate = 0;

const Page = ({ params }: { params: { team: number } }) => {
  const { team } = params;
  const paramYear = CURR_YEAR;

  return <PageContent team={team} paramYear={paramYear} />;
};

export default Page;
