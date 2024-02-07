/* eslint-disable no-unused-vars */
import { useState } from "react";
import { MdOutlineTableChart } from "react-icons/md";

import { useRouter } from "next/router";

import { Tabs } from "@mantine/core";

import QueryHandler from "../../../components/queryHandler";
import { useData } from "../../../contexts/dataContext";
import TabsLayout, { TabPanel } from "../../../layout/tabs";
import { CURR_YEAR } from "../../../utils/constants";

type TeamData = any;
type TeamYearData = any;

export default function TeamPage() {
  const router = useRouter();

  const { team } = router.query;
  const { year, setYear } = useData();
  const [tab, setTab] = useState("overview");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [teamData, setTeamData] = useState<TeamData | undefined>();
  const [teamYearDataDict, setTeamYearDataDict] = useState<{
    [key: number]: TeamYearData | undefined;
  }>();

  // console.log(team, year, loading, teamData, teamYearDataDict);

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
    <>
      <QueryHandler
        recordTab
        tab={tab}
        setTab={setTab}
        defaultTab="overview"
        tabOptions={["overview"]}
        recordYear
        year={year}
        setYear={setYear}
        recordLocation={false}
        recordWeek={false}
        query={{ team: team as string }}
      />
      <TabsLayout
        showYearSelector
        yearOptions={yearOptions}
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
    </>
  );
}
