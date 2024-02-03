import { useEffect, useState } from "react";
import { FaGithub } from "react-icons/fa";
import { MdMenu as IconMenu, MdSearch as IconSearch } from "react-icons/md";
import { RxMoon, RxSun } from "react-icons/rx";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/router";

import { AppShell, Button, Group, Kbd, NavLink as MantineNavLink, Menu, Text } from "@mantine/core";
import { Spotlight, spotlight } from "@mantine/spotlight";

import { getAllEvents, getAllTeams } from "../api/header";
import { usePreferences } from "../contexts/preferencesContext";
import { APIShortEvent, APIShortTeam } from "../types/api";
import { loaderProp } from "../utils/utils";

function NavLink({ href, label }: { href: string; label: string }) {
  const { colorScheme, setColorScheme } = usePreferences();

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
        root: "rounded h-9 hover:bg-zinc-600 dark:hover:bg-zinc-800",
      }}
    />
  );
}

function Header() {
  const router = useRouter();

  const { colorScheme, setColorScheme } = usePreferences();

  const searchIcon = (
    <IconSearch
      className="h-9 w-9 cursor-pointer rounded p-2 hover:bg-zinc-600 dark:hover:bg-zinc-800"
      stroke={1.5}
      onClick={spotlight.open}
    />
  );

  const sunIcon = (
    <RxSun
      className="h-9 w-9 cursor-pointer rounded p-2 text-yellow-500 hover:bg-zinc-600"
      stroke={4}
      onClick={() => setColorScheme("dark")}
    />
  );
  const moonIcon = (
    <RxMoon
      className="h-9 w-9 cursor-pointer rounded p-2 hover:bg-zinc-800"
      stroke={2.5}
      onClick={() => setColorScheme("light")}
    />
  );

  const [teams, setTeams] = useState<APIShortTeam[]>([]);
  const [events, setEvents] = useState<APIShortEvent[]>([]);

  useEffect(() => {
    getAllTeams().then((data) => setTeams(data));
  }, []);

  useEffect(() => {
    getAllEvents().then((data) => setEvents(data));
  }, []);

  const seenTeams = new Set();
  const teamOptions = teams
    ?.filter((team: any) => {
      const duplicate = seenTeams.has(team.team);
      seenTeams.add(team.team);
      return !duplicate;
    })
    ?.sort((a: any, b: any) => a.team - b.team)
    ?.map((team: any) => ({
      id: `team-${team.team}`,
      label: `${team.team} | ${team.name}`,
      value: `${team.team} | ${team.name}`,
      onClick: () => router.push(`/team/${team.team}`),
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
    ?.map((event: any) => ({
      id: `event-${event.key}`,
      label: `${event.key.slice(0, 4)} ${event.name}`,
      value: `${event.key.slice(0, 4)} ${event.name}`,
      onClick: () => router.push(`/event/${event.key}`),
    }));

  const allOptions = [...teamOptions, ...eventOptions];

  return (
    <AppShell.Header className="bg-zinc-700 text-white dark:border-zinc-700 dark:bg-zinc-900">
      <Spotlight
        // not rendered, but allows keyboard navigation with Ctrl+K
        actions={allOptions}
        nothingFound="Nothing found..."
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
            shadow="md"
            classNames={{ label: "w-20" }}
          >
            <Menu.Target>
              <div>
                <IconMenu className="h-5 w-5" />
              </div>
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
            <Menu trigger="click-hover" position="bottom" width={200} openDelay={100} shadow="md">
              <Menu.Target>
                <Text className="flex h-9 cursor-pointer items-center rounded px-3 text-base font-light hover:bg-zinc-600 dark:hover:bg-zinc-800">
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
            <Menu trigger="click-hover" position="bottom" width={200} openDelay={100} shadow="md">
              <Menu.Target>
                <Text className="flex h-9 cursor-pointer items-center rounded px-3 text-base font-light hover:bg-zinc-600 dark:hover:bg-zinc-800">
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
          <Button
            justify="space-between"
            leftSection={
              <div className="flex items-center">
                <IconSearch className="mr-2 h-5 w-5" stroke={1.5} />
                Search
              </div>
            }
            rightSection={<Kbd size="xs">Ctrl + K</Kbd>}
            onClick={spotlight.open}
            variant="light"
            color="zinc"
            className="mantine-focus-never mr-4 w-60 border border-zinc-500 bg-zinc-50 font-thin text-zinc-500 dark:bg-zinc-800"
          />
          <Link
            href="https://github.com/avgupta456/statbotics"
            target="_blank"
            rel="noopener noreferrer"
            className="mr-2 flex h-9 cursor-pointer items-center rounded p-2 hover:bg-zinc-600 dark:hover:bg-zinc-800"
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
