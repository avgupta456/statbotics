import { useEffect, useMemo, useState } from "react";
import { MdGridView, MdOutlineTableChart } from "react-icons/md";

import Link from "next/link";
import { useRouter } from "next/router";

import { Button, Tabs, TextInput } from "@mantine/core";

import { getYearEvents } from "../../api/events";
import FilterBar, { LocationFilter, filterLocation } from "../../components/filterBar";
import QueryHandler from "../../components/queryHandler";
import { Select } from "../../components/select";
import EventsTable from "../../components/tables/eventsTable";
import { useData } from "../../contexts/dataContext";
import { LocationContext, useLocation } from "../../contexts/locationContext";
import TabsLayout, { TabPanel } from "../../layout/tabs";
import { APIEvent, APIYear } from "../../types/api";
import { CURR_YEAR } from "../../utils/constants";
import { weekOptions } from "../../utils/filterOptions";
import { formatEventName, formatOngoingEventStatus } from "../../utils/formatting";

function EventsFilterBar({
  week,
  setWeek,
  search,
  setSearch,
}: {
  week: number | null;
  // eslint-disable-next-line no-unused-vars
  setWeek: (value: number | null) => void;
  search: string;
  // eslint-disable-next-line no-unused-vars
  setSearch: (value: string) => void;
}) {
  const { setLocation } = useLocation();
  return (
    <FilterBar
      className="flex w-full flex-row flex-wrap justify-center gap-2 px-4"
      onClearFilters={() => {
        setWeek(null);
        setLocation(null);
        setSearch("");
      }}
    >
      <Select
        className="w-32"
        value={week?.toString() ?? null}
        onChange={(value) => (value ? setWeek(parseInt(value)) : setWeek(null))}
        data={weekOptions}
        placeholder="All Weeks"
        allowDeselect={false}
        clearable
      />
      <LocationFilter />
      <TextInput
        className="w-40"
        visibleFrom="sm"
        value={search}
        onChange={(event) => setSearch(event.currentTarget.value)}
        placeholder="Search events"
      />
    </FilterBar>
  );
}

function EventCard({ event }: { event: APIEvent }) {
  const formatDates = (start: Date, end: Date) => {
    const startMonth = start.toLocaleString("default", { month: "short" });
    const endMonth = end.toLocaleString("default", { month: "short" });
    const startDate = start.getDate();
    const endDate = end.getDate();
    if (startMonth === endMonth && startDate === endDate) {
      return `${startMonth} ${startDate}`;
    }
    return `${startMonth} ${startDate} to ${endMonth} ${endDate}`;
  };

  return (
    <Link href={`/event/${event.key}`}>
      <div className="m-2 flex h-40 cursor-pointer flex-col rounded border-[1px] p-4 shadow hover:bg-blue-100">
        <div className="mb-4 w-full flex-grow text-lg font-bold">
          {formatEventName(event.name, 45)}
        </div>
        <div className="mb-2 w-full">
          Week {event.week}, {formatDates(new Date(event.start_date), new Date(event.end_date))}
        </div>
        <div className="w-full">{formatOngoingEventStatus(event)}</div>
      </div>
    </Link>
  );
}

function EventsSection({ title, events }: { title: string; events: APIEvent[] }) {
  const [expanded, setExpanded] = useState(false);
  const cutoffN = 8;

  const count = events.length;
  const showEvents = events.slice(0, expanded ? undefined : cutoffN);

  return (
    <div className="w-full">
      <div className="mb-4 mt-4 flex w-full items-center">
        <div className="text-xl font-bold md:text-2xl">{`${title} Events (${count})`}</div>
        {count > cutoffN && (
          <Button className="ml-4 px-2" onClick={() => setExpanded(!expanded)}>
            {expanded ? "Show Less" : "Show More"}
          </Button>
        )}
      </div>
      <div className="mb-4 flex w-full flex-wrap items-center justify-center">
        {showEvents.map((event) => (
          <div key={event.key} className="w-full md:w-1/2 lg:w-1/4">
            <EventCard event={event} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default function EventsPage() {
  const { isReady } = useRouter();
  const { eventDataDict, setEventDataDict, setYearDataDict } = useData();

  const [tab, setTab] = useState<string>("summary");
  const [year, setYear] = useState<number>(CURR_YEAR);
  const [location, setLocation] = useState<string | null>(null);
  const [week, setWeek] = useState<number | null>(-1);
  const [search, setSearch] = useState<string>("");

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
  }, [isReady, eventDataDict, year]);

  const [data, setData] = useState<APIEvent[]>([]);

  useEffect(() => {
    let filtered = eventDataDict[year] ?? [];

    const sortEvents = (a: APIEvent, b: APIEvent) => {
      if ((a.status === "Ongoing" && b.status === "Ongoing") || a.start_date === b.start_date) {
        return (b.epa.mean ?? -1) - (a.epa.mean ?? -1);
      }
      return a.start_date > b.start_date ? 1 : -1;
    };

    filtered = filtered.sort(sortEvents);

    if (week !== null && week >= 0) {
      filtered = filtered.filter((event) => event.week === week);
    }

    if (location !== null) {
      filtered = filtered.filter((event) => filterLocation(location, event));
    }

    if (search !== "") {
      filtered = filtered.filter(
        (event) =>
          event.name.toLowerCase().includes(search.toLowerCase()) ||
          event.key.toLowerCase().includes(search.toLowerCase()),
      );
    }

    setData(filtered);
  }, [eventDataDict, year, week, location, search]);

  const ongoingEvents = data.filter((event) => event.status === "Ongoing");
  const upcomingEvents = data.filter((event) => event.status === "Upcoming");
  const completedEvents = data.filter((event) => event.status === "Completed");

  return (
    <div className="flex-grow pb-4">
      <LocationContext.Provider value={memoizedLocation}>
        <QueryHandler
          recordTab
          tab={tab}
          setTab={setTab}
          defaultTab="summary"
          tabOptions={["summary", "table"]}
          recordYear
          year={year}
          setYear={setYear}
          recordLocation
          location={location}
          setLocation={setLocation}
        />
        <TabsLayout
          showYearSelector
          year={year}
          setYear={setYear}
          title="Events"
          tab={tab}
          setTab={setTab}
          defaultTab="summary"
        >
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
              <EventsFilterBar
                week={week}
                setWeek={setWeek}
                search={search}
                setSearch={setSearch}
              />
              <div className="p-2 md:p-0">
                {[
                  { name: "Ongoing", events: ongoingEvents },
                  { name: "Upcoming", events: upcomingEvents },
                  { name: "Completed", events: completedEvents },
                ]
                  .filter(({ events }) => events.length > 0)
                  .map(({ name, events }) => (
                    <EventsSection key={name} title={name} events={events} />
                  ))}
              </div>
            </div>
          </TabPanel>
          <TabPanel value="table" loading={loading} error={error}>
            <div className="h-full w-full">
              <EventsFilterBar
                week={week}
                setWeek={setWeek}
                search={search}
                setSearch={setSearch}
              />
              <div className="h-4" />
              <EventsTable data={data} />
            </div>
          </TabPanel>
        </TabsLayout>
      </LocationContext.Provider>
    </div>
  );
}
