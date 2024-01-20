import { useEffect, useMemo, useState } from "react";
import { MdGridView, MdOutlineTableChart } from "react-icons/md";

import { useRouter } from "next/router";

import { Tabs } from "@mantine/core";

import { getYearEvents } from "../../api/events";
import FilterBar, { LocationFilter } from "../../components/filterBar";
import QueryHandler from "../../components/queryHandler";
import { Select } from "../../components/select";
import { useData } from "../../contexts/dataContext";
import { LocationContext } from "../../contexts/locationContext";
import TabsLayout, { TabPanel } from "../../layout/tabs";
import { APIEvent, APIYear } from "../../types/api";

const weekOptions = [
  { value: "0", label: "Week 0" },
  { value: "1", label: "Week 1" },
  { value: "2", label: "Week 2" },
  { value: "3", label: "Week 3" },
  { value: "4", label: "Week 4" },
  { value: "5", label: "Week 5" },
  { value: "6", label: "Week 6" },
  { value: "7", label: "Week 7" },
  { value: "8", label: "Week 8" },
  { value: "9", label: "Offseason" },
];

function EventsFilterBar({
  week,
  setWeek,
  setLocation,
}: {
  week: number | null;
  // eslint-disable-next-line no-unused-vars
  setWeek: (value: number | null) => void;
  // eslint-disable-next-line no-unused-vars
  setLocation: (value: string | null) => void;
}) {
  return (
    <FilterBar
      onClearFilters={() => {
        setWeek(null);
        setLocation(null);
      }}
    >
      <Select
        className="w-40"
        value={week?.toString()}
        onChange={(value) => (value ? setWeek(parseInt(value)) : setWeek(null))}
        data={weekOptions}
        placeholder="All Weeks"
        allowDeselect={false}
        clearable
      />
      <LocationFilter />
    </FilterBar>
  );
}

export default function EventsPage() {
  const { isReady } = useRouter();
  const { eventDataDict, setEventDataDict, setYearDataDict, year, setYear } = useData();

  const [tab, setTab] = useState<string>("summary");
  const [location, setLocation] = useState<string | null>(null);
  const [week, setWeek] = useState<number | null>(null);

  const memoizedLocation = useMemo(() => ({ location, setLocation }), [location, setLocation]);

  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const getDataForYear = async (yearNum: number) => {
      setLoading(true);
      const {
        year: yearData,
        events: eventsData,
      }: {
        year: APIYear;
        events: APIEvent[];
      } = await getYearEvents(yearNum);
      if (eventsData && yearData) {
        setEventDataDict((prev: { [key: number]: APIEvent[] }) => ({
          ...prev,
          [yearNum]: eventsData,
        }));
        setYearDataDict((prev: { [key: number]: APIYear }) => ({ ...prev, [yearNum]: yearData }));
      } else {
        setError(true);
      }
      setLoading(false);
    };

    if (isReady && !error && !eventDataDict[year] && !loading) {
      getDataForYear(year);
    }
  }, [eventDataDict, year]);

  const data = eventDataDict[year];

  console.log(data);

  return (
    <LocationContext.Provider value={memoizedLocation}>
      <QueryHandler
        tab={tab}
        setTab={setTab}
        defaultTab="summary"
        tabOptions={["summary", "table"]}
        year={year}
        setYear={setYear}
        location={location}
        setLocation={setLocation}
        week={week}
        setWeek={setWeek}
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
        <TabPanel value="summary" loading={loading} error={error}>
          <div className="h-full w-full">
            <EventsFilterBar week={week} setWeek={setWeek} setLocation={setLocation} />
            <div>TODO</div>
          </div>
        </TabPanel>
        <TabPanel value="table" loading={loading} error={error}>
          <div className="h-full w-full">
            <EventsFilterBar week={week} setWeek={setWeek} setLocation={setLocation} />
            <div>TODO</div>
          </div>
        </TabPanel>
      </TabsLayout>
    </LocationContext.Provider>
  );
}
