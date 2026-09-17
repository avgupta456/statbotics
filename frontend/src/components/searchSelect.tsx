"use client";

import React, { useEffect, useState } from "react";
import WindowedSelect, { createFilter } from "react-windowed-select";

import { useRouter } from "next/navigation";

import { getAllEvents, getAllTeams } from "../api/header";
import { ShortEvent, ShortTeam } from "../types/data";
import { classnames } from "../utils";
import { Option } from "./multiSelect";

// Shared across instances so the navbar and home page trigger one fetch each, not one per select
let teamsPromise: Promise<ShortTeam[]> | undefined;
let eventsPromise: Promise<ShortEvent[]> | undefined;

const loadTeams = () => (teamsPromise ??= getAllTeams());
const loadEvents = () => (eventsPromise ??= getAllEvents());

// Search box for teams and events. Used in the navbar and on the mobile home page.
const SearchSelect = ({
  instanceId,
  className,
  onSelect,
}: {
  instanceId: string;
  className?: string;
  onSelect?: () => void;
}) => {
  const router = useRouter();

  const [teams, setTeams] = useState<ShortTeam[]>([]);
  const [events, setEvents] = useState<ShortEvent[]>([]);

  useEffect(() => {
    loadTeams().then((data) => setTeams(data));
  }, []);

  useEffect(() => {
    loadEvents().then((data) => setEvents(data));
  }, []);

  const teamOptions = teams
    ?.filter((team) => team.active)
    ?.sort((a, b) => parseInt(a.team) - parseInt(b.team))
    ?.map((team: ShortTeam) => ({
      value: `/team/${team.team}`,
      label: `${team.team} | ${team.name}`,
    }));

  const eventOptions = events
    ?.sort((a, b) => parseInt(b.key.slice(0, 4)) - parseInt(a.key.slice(0, 4)))
    ?.map((event: any) => ({
      value: `/event/${event.key}`,
      label: `${event.key.slice(0, 4)} ${event.name}`,
    }));

  const allOptions = [...teamOptions, ...eventOptions];

  return (
    <WindowedSelect
      instanceId={instanceId}
      className={classnames("text-xs text-gray-800", className)}
      styles={{
        menu: (provided) => ({ ...provided, zIndex: 9999 }),
      }}
      options={allOptions}
      onChange={(e: any) => {
        if (e) {
          router.push(e.value);
          onSelect?.();
        }
      }}
      placeholder="Search Teams and Events"
      filterOption={createFilter({ ignoreAccents: false })}
      windowThreshold={50}
      components={{
        Option: Option,
      }}
    />
  );
};

export default SearchSelect;
