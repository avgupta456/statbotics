import { useEffect, useMemo, useState } from "react";
import { MdGridView, MdOutlineTableChart } from "react-icons/md";

import Link from "next/link";
import { useRouter } from "next/router";

import { Button, Tabs, TextInput } from "@mantine/core";

import { getYearEvents } from "../../api/events";
import FilterBar, { LocationFilter, filterLocation } from "../../components/filterBar";
import QueryHandler from "../../components/queryHandler";
import { Select } from "../../components/select";
import { useData } from "../../contexts/dataContext";
import { LocationContext } from "../../contexts/locationContext";
import TabsLayout, { TabPanel } from "../../layout/tabs";
import { APIEvent, APIYear } from "../../types/api";
import { formatEventName } from "../../utils/utils";

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
  search,
  setSearch,
}: {
  week: number | null;
  // eslint-disable-next-line no-unused-vars
  setWeek: (value: number | null) => void;
  // eslint-disable-next-line no-unused-vars
  setLocation: (value: string | null) => void;
  search: string;
  // eslint-disable-next-line no-unused-vars
  setSearch: (value: string) => void;
}) {
  return (
    <FilterBar
      className="flex w-full flex-row flex-wrap justify-center gap-4 px-4"
      onClearFilters={() => {
        setWeek(null);
        setLocation(null);
      }}
    >
      <Select
        className="w-32"
        value={week?.toString()}
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
  let location = event.country;
  if (event.state) {
    location = `${event.state}, ${location}`;
  }
  if (event.district) {
    location = `${location} (${event.district.toUpperCase()})`;
  }
  return (
    <Link href={`/event/${event.key}`}>
      <div className="m-2 flex h-40 cursor-pointer flex-col rounded border-[1px] p-4 shadow hover:bg-blue-100">
        <div className="mb-4 w-full flex-grow text-lg font-bold">
          {formatEventName(event.name, 45)}
        </div>
        <div className="mb-2 w-full">
          {location} - Week {event.week}
        </div>
        {event.status === "Ongoing" && (
          <div className="w-full">formatOngoingEventStatus(event)</div>
        )}
      </div>
    </Link>
  );
}

function EventsSection({ title, events }: { title: string; events: APIEvent[] }) {
  const [expanded, setExpanded] = useState(false);
  const cutoffN = 4;

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
  const { eventDataDict, setEventDataDict, setYearDataDict, year, setYear } = useData();

  const [tab, setTab] = useState<string>("summary");
  const [location, setLocation] = useState<string | null>(null);
  const [week, setWeek] = useState<number | null>(null);
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
  }, [eventDataDict, year]);

  const [ongoingEvents, upcomingEvents, completedEvents] = useMemo(() => {
    let filtered = eventDataDict[year];
    if (!filtered) {
      return [[], [], []];
    }

    const sortEvents = (a: APIEvent, b: APIEvent) => {
      if (a.week === b.week) {
        return (a.epa.mean ?? -1) - (b.epa.mean ?? -1);
      }
      return a.week - b.week;
    };

    filtered = filtered.sort(sortEvents);

    if (week !== null) {
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

    const ongoing = filtered.filter((event) => event.status === "Ongoing");
    const upcoming = filtered.filter((event) => event.status === "Upcoming");
    const completed = filtered.filter((event) => event.status === "Completed");

    return [ongoing, upcoming, completed];
  }, [eventDataDict, year, week, location, search]);

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
            <EventsFilterBar
              week={week}
              setWeek={setWeek}
              setLocation={setLocation}
              search={search}
              setSearch={setSearch}
            />
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
        </TabPanel>
        <TabPanel value="table" loading={loading} error={error}>
          <div className="h-full w-full">
            <EventsFilterBar
              week={week}
              setWeek={setWeek}
              setLocation={setLocation}
              search={search}
              setSearch={setSearch}
            />
            <div>TODO</div>
          </div>
        </TabPanel>
      </TabsLayout>
    </LocationContext.Provider>
  );
}
