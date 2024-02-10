/* eslint-disable no-unused-vars */
import { useState } from "react";
import { MdOutlineTableChart } from "react-icons/md";

import { useRouter } from "next/router";

import { Tabs } from "@mantine/core";

import QueryHandler from "../../../components/queryHandler";
import TabsLayout, { TabPanel } from "../../../layout/tabs";
import { CURR_YEAR } from "../../../utils/constants";

type TeamData = any;
type TeamYearData = any;

export function PageContent({
  team,
  paramYear,
  interpolation,
}: {
  team: string;
  paramYear: number;
  interpolation: { [key: string]: any };
}) {
  const [year, setYear] = useState(paramYear);
  const [tab, setTab] = useState("overview");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [teamData, setTeamData] = useState<TeamData | undefined>();
  const [teamYearDataDict, setTeamYearDataDict] = useState<{
    [key: number]: TeamYearData | undefined;
  }>();

  if (!loading && !teamData) {
    return <div>Team not found</div>;
  }

  const rookieYear = 2002;

  let yearOptions = Array.from({ length: CURR_YEAR - rookieYear + 1 }, (_, i) =>
    (CURR_YEAR - i).toString(),
  ).reverse();

  if (teamYearDataDict) {
    yearOptions = Object.keys(teamYearDataDict).sort((a, b) => parseInt(b) - parseInt(a));
  }

  return (
    <div className="flex-grow pb-4">
      <QueryHandler
        recordTab
        tab={tab}
        setTab={setTab}
        defaultTab="overview"
        tabOptions={["overview"]}
        recordYear={false}
        recordLocation={false}
        query={interpolation}
      />
      <TabsLayout
        showYearSelector
        yearOptions={yearOptions}
        year={year}
        setYear={setYear}
        title="Team"
        tab={tab}
        setTab={setTab}
        defaultTab="overview"
      >
        <Tabs.List>
          <Tabs.Tab value="overview" leftSection={<MdOutlineTableChart />}>
            Overview
          </Tabs.Tab>
        </Tabs.List>
        <TabPanel value="overview" loading={loading} error={error}>
          <div className="h-full w-full">
            <p>Team {team}</p>
          </div>
        </TabPanel>
      </TabsLayout>
    </div>
  );
}

export default function TeamPage() {
  const router = useRouter();
  const { team } = router.query;
  return <PageContent team={team as string} paramYear={CURR_YEAR} interpolation={{ team }} />;
}
