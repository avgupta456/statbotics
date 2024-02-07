import { useMemo, useState } from "react";
import { GiPodium } from "react-icons/gi";
import { IoMdStopwatch } from "react-icons/io";

import { Tabs } from "@mantine/core";

import QueryHandler from "../../components/queryHandler";
import { LocationContext } from "../../contexts/locationContext";
import TabsLayout, { TabPanel } from "../../layout/tabs";
import { CURR_YEAR } from "../../utils/constants";
import NoteworthyMatches from "./noteworthy";
import UpcomingMatches from "./upcoming";

export default function MatchesPage() {
  const [year, setYear] = useState(CURR_YEAR);
  const [location, setLocation] = useState<string | null>(null);
  const [_tab, setTab] = useState<string>("upcoming");

  let tab = _tab;
  if (tab === "upcoming" && year !== CURR_YEAR) {
    tab = "noteworthy";
  }

  const memoizedLocation = useMemo(() => ({ location, setLocation }), [location, setLocation]);

  return (
    <LocationContext.Provider value={memoizedLocation}>
      <QueryHandler
        recordTab
        tab={tab}
        setTab={setTab}
        defaultTab="upcoming"
        tabOptions={["upcoming", "noteworthy"]}
        recordYear
        year={year}
        setYear={setYear}
        recordLocation
        location={location}
        setLocation={setLocation}
        recordWeek={false}
      />
      <TabsLayout
        showYearSelector
        year={year}
        setYear={setYear}
        title="Matches"
        tab={tab}
        setTab={setTab}
        defaultTab="upcoming"
      >
        <Tabs.List>
          {year === CURR_YEAR && (
            <Tabs.Tab value="upcoming" leftSection={<IoMdStopwatch />}>
              Upcoming
            </Tabs.Tab>
          )}
          <Tabs.Tab value="noteworthy" leftSection={<GiPodium />}>
            Noteworthy
          </Tabs.Tab>
        </Tabs.List>
        <TabPanel value="upcoming" loading={false} error={false}>
          <UpcomingMatches />
        </TabPanel>
        <TabPanel value="noteworthy" loading={false} error={false}>
          <NoteworthyMatches year={year} />
        </TabPanel>
      </TabsLayout>
    </LocationContext.Provider>
  );
}
