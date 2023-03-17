"use client";

import React, { useEffect, useState } from "react";
import { BsThreeDots } from "react-icons/bs";
import { GiHamburgerMenu as HamburgerIcon } from "react-icons/gi";
import WindowedSelect, { createFilter } from "react-windowed-select";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { Option } from "../components/multiSelect";
import { BACKEND_URL } from "../constants";
import { classnames, log, round } from "../utils";
import { getWithExpiry, setWithExpiry } from "./localStorage";

const loaderProp = ({ src }) => {
  return src;
};

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

const Navbar = () => {
  const router = useRouter();

  const [toggle, setToggle] = useState(false);

  const [teams, setTeams] = useState([]);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    getTeamData().then((data) => setTeams(data));
  }, []);

  useEffect(() => {
    getEventData().then((data) => setEvents(data));
  }, []);

  const teamOptions = teams?.map((team: any) => ({
    value: `/team/${team.num}`,
    label: `${team.num} | ${team.team}`,
  }));

  const eventOptions = events?.reverse()?.map((event: any) => ({
    value: `/event/${event.key}`,
    label: `${event.key.slice(0, 4)} ${event.name}`,
  }));

  const allOptions = [...teamOptions, ...eventOptions];

  const TeamSelect = () => {
    return (
      <WindowedSelect
        instanceId={"team-select"}
        className="w-60 text-xs mr-2 text-gray-800"
        styles={{
          menu: (provided) => ({ ...provided, zIndex: 9999 }),
        }}
        options={allOptions}
        onChange={(e: any) => {
          if (e) {
            router.push(e.value);
            setToggle(false);
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

  return (
    <div className="w-full flex flex-col shadow-md text-gray-100" style={{ background: "#343A40" }}>
      <div className="body-font sticky top-0 z-50 px-4 py-3 flex">
        <Link href="/" className="flex items-center gap-2 text-xl font-thin mr-8">
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
        <div className="hidden md:flex items-center text-base text-gray-300 hover:text-gray-100 font-thin mr-4">
          <Link href="/teams">Teams</Link>
        </div>
        <div className="hidden md:flex items-center text-base text-gray-300 hover:text-gray-100 font-thin mr-4">
          <Link href="/events">Events</Link>
        </div>
        <div className="hidden md:flex items-center text-base text-gray-300 hover:text-gray-100 font-thin">
          <Link href="/matches">Matches</Link>
        </div>
        <div className="hidden md:inline dropdown dropdown-end dropdown-hover" tabIndex={0}>
          <div className="h-10 flex items-center ml-4 cursor-pointer">
            <p className="h-auto text-base text-gray-300 hover:text-gray-100 font-thin">Misc</p>
          </div>
          <ul
            tabIndex={0}
            className="h-auto w-40 dropdown-content p-2 rounded shadow-lg bg-white text-gray-800"
          >
            <li>
              <Link href="/compare">
                <div className="w-36 py-1 text-sm text-center">Compare Teams</div>
              </Link>
            </li>
          </ul>
        </div>
        <div className="flex-grow" />
        <div className="hidden md:inline dropdown dropdown-end dropdown-hover" tabIndex={0}>
          <div className="h-10 flex items-center mr-4 cursor-pointer">
            <p className="h-auto text-base text-gray-300 hover:text-gray-100 font-thin">API</p>
          </div>
          <ul
            tabIndex={0}
            className="h-auto w-40 dropdown-content p-2 rounded shadow-lg bg-white text-gray-800"
          >
            <li>
              <Link href="/api/rest">
                <div className="w-36 py-1 text-sm text-center border-b-[1px]">REST API Docs</div>
              </Link>
            </li>
            <li>
              <Link href="/api/python">
                <div className="w-36 py-1 text-sm text-center">Python API Docs</div>
              </Link>
            </li>
          </ul>
        </div>
        <div className="hidden md:flex items-center text-base text-gray-300 hover:text-gray-100 font-thin mr-4">
          <Link href="/blog">Blog</Link>
        </div>
        <div className="dropdown dropdown-end dropdown-hover" tabIndex={0}>
          <BsThreeDots className="no_hover_icon mr-4 text-gray-300 hover:text-gray-100" />
          <ul
            tabIndex={0}
            className="h-auto w-40 dropdown-content p-2 rounded shadow-lg bg-white text-gray-800"
          >
            <li>
              <Link
                href="https://github.com/avgupta456/statbotics"
                target="_blank"
                rel="noopener noreferrer"
              >
                <div className="w-36 py-1 text-sm text-center border-b-[1px]">View GitHub</div>
              </Link>
            </li>
            <li>
              <Link
                href="https://statbotics.canny.io/feature-requests"
                target="_blank"
                rel="noopener noreferrer"
              >
                <div className="w-36 py-1 text-sm text-center border-b-[1px]">Give Feedback</div>
              </Link>
            </li>
            <li>
              <Link
                href="https://www.buymeacoffee.com/statbotics"
                target="_blank"
                rel="noopener noreferrer"
              >
                <div className="w-36 py-1 text-sm text-center">Buy Me a Coffee</div>
              </Link>
            </li>
          </ul>
        </div>
        <div className="hidden md:flex items-center gap-2 font-thin text-gray-800">
          <TeamSelect />
        </div>
        <div className="md:hidden flex ml-auto items-center">
          <button type="button" className="outline-none" onClick={() => setToggle(!toggle)}>
            <HamburgerIcon className="w-6 h-6" />
          </button>
        </div>
      </div>
      <div
        className={classnames(
          "pt-0 border-t-[1px] border-gray-500 w-full flex flex-col gap-2",
          "md:hidden", // Hide on desktop
          !toggle && "hidden"
        )}
      >
        <div className="h-2" />
        <Link href="/teams" className="ml-4" onClick={() => setToggle(false)}>
          Teams
        </Link>
        <Link href="/events" className="ml-4" onClick={() => setToggle(false)}>
          Events
        </Link>
        <Link href="/matches" className="ml-4" onClick={() => setToggle(false)}>
          Matches
        </Link>
        <Link href="/blog" className="ml-4" onClick={() => setToggle(false)}>
          Blog
        </Link>
        <div className="my-2 h-[1px] bg-gray-600" />
        <div className="mx-auto">
          <TeamSelect />
        </div>
        <div className="h-2" />
      </div>
    </div>
  );
};

export default Navbar;
