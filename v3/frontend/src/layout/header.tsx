import { useEffect, useState } from "react";
import { FaGithub } from "react-icons/fa";
import { MdSearch as IconSearch } from "react-icons/md";
import { RxMoon, RxSun } from "react-icons/rx";

import Image from "next/image";
import Link from "next/link";

import {
  AppShell,
  Autocomplete,
  Burger,
  Group,
  Kbd,
  NavLink as MantineNavLink,
  Menu,
  Text,
  useMantineColorScheme,
} from "@mantine/core";
import { Spotlight, spotlight } from "@mantine/spotlight";

import { BACKEND_URL } from "../utils/constants";
import { getWithExpiry, setWithExpiry } from "../utils/localStorage";
import { classnames, loaderProp, log, round } from "../utils/utils";

function NavLink({ href, label }: { href: string; label: string }) {
  const { colorScheme, setColorScheme } = useMantineColorScheme();

  useEffect(() => {
    if (colorScheme === "auto") {
      setColorScheme("light");
    }
  }, [colorScheme, setColorScheme]);

  return (
    <MantineNavLink
      href={href}
      label={label}
      variant="subtle"
      classNames={{
        label: "text-base font-light",
        root: classnames(
          "rounded",
          colorScheme === "light" ? "hover:bg-gray-50" : "hover:bg-gray-800",
        ),
      }}
    />
  );
}

function Header() {
  const { colorScheme, setColorScheme } = useMantineColorScheme();

  const searchIcon = (
    <IconSearch
      className={classnames(
        "h-9 w-9 cursor-pointer rounded p-2",
        colorScheme === "light" ? "hover:bg-gray-50" : "hover:bg-gray-800",
      )}
      stroke={1.5}
      onClick={spotlight.open}
    />
  );

  const sunIcon = (
    <RxSun
      className="h-9 w-9 cursor-pointer rounded p-2 text-yellow-500 hover:bg-gray-50"
      stroke={4}
      onClick={() => setColorScheme("dark")}
    />
  );
  const moonIcon = (
    <RxMoon
      className="h-9 w-9 cursor-pointer rounded p-2 text-blue-600 hover:bg-gray-800"
      stroke={2.5}
      onClick={() => setColorScheme("light")}
    />
  );

  async function getTeamData() {
    const cacheData = getWithExpiry("full_team_list");
    if (cacheData && cacheData?.length > 1000) {
      log("Used Local Storage: Full Team List");
      return cacheData;
    }

    const start = performance.now();
    const res = await fetch(`${BACKEND_URL}/teams/all`, { next: { revalidate: 60 } });
    log(`/teams/all took ${round(performance.now() - start, 0)}ms`);

    if (!res.ok) {
      return undefined;
    }
    const data = (await res.json())?.data;
    setWithExpiry("full_team_list", data, 60 * 60 * 24 * 7); // 1 week expiry
    return data;
  }

  async function getEventData() {
    const cacheData = getWithExpiry("full_event_list");
    if (cacheData && cacheData?.length > 1000) {
      log("Used Local Storage: Full Event List");
      return cacheData;
    }

    const start = performance.now();
    const res = await fetch(`${BACKEND_URL}/events/all`, { next: { revalidate: 60 } });
    log(`events/all took ${round(performance.now() - start, 0)}ms`);

    if (!res.ok) {
      return undefined;
    }
    const data = (await res.json())?.data;
    setWithExpiry("full_event_list", data, 60 * 60 * 24 * 7); // 1 week expiry
    return data;
  }

  const [teams, setTeams] = useState([]);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    getTeamData().then((data) => setTeams(data));
  }, []);

  useEffect(() => {
    getEventData().then((data) => setEvents(data));
  }, []);

  const seenTeams = new Set();
  const teamOptions = teams
    ?.filter((team: any) => {
      const duplicate = seenTeams.has(team.num);
      seenTeams.add(team.num);
      return !duplicate;
    })
    ?.map((team: any, index: number) => ({
      id: `team-${index}`,
      label: `${team.num} | ${team.team}`,
      url: `/team/${team.num}`,
    }));

  const seenEvents = new Set();
  const eventOptions = events
    ?.filter((event: any) => {
      const duplicate = seenEvents.has(event.key);
      seenEvents.add(event.key);
      return !duplicate;
    })
    ?.map((event: any) => ({ ...event, year: parseInt(event.key.slice(0, 4)) }))
    ?.sort((a, b) => b.year - a.year)
    ?.map((event: any, index: number) => ({
      id: `event-${index}`,
      label: `${event.key.slice(0, 4)} ${event.name}`,
      description: `${event.key.slice(0, 4)} ${event.name}`,
      url: `/event/${event.key}`,
    }));

  const allOptions = [...teamOptions, ...eventOptions];

  const [hideKbd, setHideKbd] = useState(false);

  return (
    <AppShell.Header>
      <Spotlight
        // not rendered, but allows keyboard navigation with Ctrl+K
        actions={allOptions}
        nothingFound="Nothing found..."
        highlightQuery
        limit={20}
        scrollable
        maxHeight={350}
        searchProps={{
          leftSection: <IconSearch className="h-5 w-5" stroke={1.5} />,
          placeholder: "Search...",
        }}
      />
      <div className="m-3 flex items-center">
        <Group className="w-full" gap={0} hiddenFrom="md">
          <Menu
            trigger="click"
            position="bottom"
            width={200}
            openDelay={100}
            classNames={{ label: "w-20" }}
          >
            <Menu.Target>
              <Burger size="sm" />
            </Menu.Target>
            <Menu.Dropdown>
              <Menu.Item component={Link} href="/teams">
                Teams
              </Menu.Item>
              <Menu.Item component={Link} href="/events">
                Events
              </Menu.Item>
              <Menu.Item component={Link} href="/matches">
                Matches
              </Menu.Item>
            </Menu.Dropdown>
          </Menu>
          <div className="flex flex-grow justify-center">
            <div className="flex">
              <Link href="/" className="flex items-center gap-2 text-lg font-thin">
                <Image
                  src="/circ_favicon.ico"
                  alt="logo"
                  width={32}
                  height={32}
                  loader={loaderProp}
                  unoptimized
                />
                Statbotics
              </Link>
            </div>
          </div>
          <div className="flex w-20 justify-end">
            {searchIcon}
            {colorScheme === "light" ? sunIcon : moonIcon}
          </div>
        </Group>
        <Group className="w-full" gap={0} visibleFrom="md">
          <div className="flex">
            <Link href="/" className="mr-4 flex items-center gap-2 text-xl font-thin">
              <Image
                src="/circ_favicon.ico"
                alt="logo"
                width={30}
                height={30}
                loader={loaderProp}
                unoptimized
              />
              Statbotics
            </Link>
          </div>
          <div className="flex w-auto">
            <NavLink href="/teams" label="Teams" />
            <NavLink href="/events" label="Events" />
            <NavLink href="/matches" label="Matches" />
          </div>
          <div className="flex-grow" />
          <div className="mr-4 flex w-auto">
            <Menu trigger="click-hover" position="bottom" width={200} openDelay={100}>
              <Menu.Target>
                <Text
                  className={classnames(
                    "cursor-pointer rounded px-3 py-2 text-base font-light",
                    colorScheme === "light" ? "hover:bg-gray-50" : "hover:bg-gray-800",
                  )}
                >
                  API
                </Text>
              </Menu.Target>
              <Menu.Dropdown>
                <Menu.Label>Setup</Menu.Label>
                <Menu.Item component={Link} href="/api/auth">
                  Get API Key
                </Menu.Item>
                <Menu.Divider />
                <Menu.Label>Documentation</Menu.Label>
                <Menu.Item component={Link} href="/api/rest">
                  REST API
                </Menu.Item>
                <Menu.Item component={Link} href="/api/python">
                  Python API
                </Menu.Item>
              </Menu.Dropdown>
            </Menu>
            <Menu trigger="click-hover" position="bottom" width={200} openDelay={100}>
              <Menu.Target>
                <Text
                  className={classnames(
                    "cursor-pointer rounded px-3 py-2 text-base font-light",
                    colorScheme === "light" ? "hover:bg-gray-50" : "hover:bg-gray-800",
                  )}
                >
                  More
                </Text>
              </Menu.Target>
              <Menu.Dropdown>
                <Menu.Label>Docs</Menu.Label>
                <Menu.Item component={Link} href="/blog">
                  Blog
                </Menu.Item>
                <Menu.Item
                  component={Link}
                  href="https://github.com/avgupta456/statbotics"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  GitHub
                </Menu.Item>
                <Menu.Divider />
                <Menu.Label>Misc</Menu.Label>
                <Menu.Item component={Link} href="/compare">
                  Compare Teams
                </Menu.Item>
                <Menu.Item component={Link} href="/hypothetical" disabled>
                  Hypotheticals
                </Menu.Item>
                <Menu.Divider />
                <Menu.Label>Other</Menu.Label>
                <Menu.Item
                  component={Link}
                  href="https://www.buymeacoffee.com/statbotics"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Buy Me a Coffee
                </Menu.Item>
                <Menu.Item
                  component={Link}
                  href="https://statbotics.canny.io/feature-requests"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Give Feedback
                </Menu.Item>
              </Menu.Dropdown>
            </Menu>
          </div>
          <Autocomplete
            data={[
              { group: "Teams", items: teamOptions.map((team) => team.label) },
              { group: "Events", items: eventOptions.map((event) => event.label) },
            ]}
            onFocus={() => setHideKbd(true)}
            onBlur={() => setHideKbd(false)}
            limit={20}
            maxDropdownHeight={350}
            placeholder="Search"
            leftSection={<IconSearch className="h-5 w-5" stroke={1.5} />}
            rightSection={
              <Kbd
                size="xs"
                onClick={spotlight.open}
                className={classnames(hideKbd ? "hidden" : "", "cursor-pointer")}
              >
                Ctrl + K
              </Kbd>
            }
            rightSectionWidth={72}
            className="mr-4"
          />
          <Link
            href="https://github.com/avgupta456/statbotics"
            target="_blank"
            rel="noopener noreferrer"
            className={classnames(
              "mr-2 h-9 w-9 rounded p-2",
              colorScheme === "light" ? "hover:bg-gray-50" : "hover:bg-gray-800",
            )}
          >
            <FaGithub className="h-5 w-5" stroke={2} />
          </Link>
          {colorScheme === "light" ? sunIcon : moonIcon}
        </Group>
      </div>
    </AppShell.Header>
  );
}

export default Header;
