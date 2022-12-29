"use client";

import React, { useEffect } from "react";
import WindowedSelect, { createFilter } from "react-windowed-select";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { Option } from "../components/multiSelect";
import { BACKEND_URL } from "../constants";
import { round } from "../utils";
import { getWithExpiry, setWithExpiry } from "./localStorage";

const loaderProp = ({ src }) => {
  return src;
};

async function getData() {
  const cacheData = getWithExpiry("full_team_list");
  if (cacheData && cacheData?.length > 1000) {
    console.log("Used Local Storage: Full Team List");
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/teams/all`);
  console.log(`/teams/all took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  setWithExpiry("full_team_list", data, 60 * 60 * 24 * 7); // 1 week expiry
  return data;
}

const Navbar = () => {
  const router = useRouter();

  const [teams, setTeams] = React.useState([]);

  useEffect(() => {
    getData().then((data) => setTeams(data));
  }, []);

  const teamOptions = teams.map((team: any) => ({
    value: team.num,
    label: `${team.num} | ${team.team}`,
  }));

  return (
    <div
      className="text-gray-100 shadow-md body-font sticky top-0 z-50 px-4 py-3 flex"
      style={{ background: "#343A40" }}
    >
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
      <div className="flex items-center text-base text-gray-300 hover:text-gray-100 font-thin">
        <Link href="/teams">Teams</Link>
      </div>
      <div className="flex-grow" />
      <div className="flex items-center gap-2 font-thin text-gray-800">
        <WindowedSelect
          instanceId={"team-select"}
          className="w-60 text-xs mr-2"
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={teamOptions}
          onChange={(e: any) => {
            if (e) {
              router.push(`/team/${e.value}`);
            }
          }}
          placeholder="Search Teams and Events"
          filterOption={createFilter({ ignoreAccents: false })}
          windowThreshold={50}
          components={{
            Option: Option,
          }}
        />
      </div>
    </div>
  );
};

export default Navbar;
