import { useMemo, useState } from "react";
import { MdGridView, MdOutlineTableChart } from "react-icons/md";

import { Tabs } from "@mantine/core";

import QueryHandler from "../../components/queryHandler";
import { LocationContext } from "../../contexts/locationContext";
import TabsLayout, { TabPanel } from "../../layout/tabs";

export default function EventsPage() {
  const [location, setLocation] = useState<string | null>(null);
  const [tab, setTab] = useState<string>("summary");

  const memoizedLocation = useMemo(() => ({ location, setLocation }), [location, setLocation]);

  const [error] = useState(false);

  return (
    <LocationContext.Provider value={memoizedLocation}>
      <QueryHandler
        tab={tab}
        setTab={setTab}
        defaultTab="summary"
        tabOptions={["summary", "table"]}
      />
      <TabsLayout showYearSelector title="Events" tab={tab} setTab={setTab} defaultTab="summary">
        <Tabs.List>
          <Tabs.Tab value="summary" leftSection={<MdGridView />}>
            Summary
          </Tabs.Tab>
          <Tabs.Tab value="table" leftSection={<MdOutlineTableChart />}>
            Table
          </Tabs.Tab>
        </Tabs.List>
        <TabPanel value="summary" error={error}>
          <div className="mt-4 h-full w-full">
            <div>TODO</div>
          </div>
        </TabPanel>
        <TabPanel value="table" error={error}>
          <div className="mt-4 h-full w-full">
            <div>TODO</div>
          </div>
        </TabPanel>
      </TabsLayout>
    </LocationContext.Provider>
  );
}
