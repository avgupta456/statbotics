"use client";

import React, { useEffect } from "react";
import WindowedSelect, { createFilter } from "react-windowed-select";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { Option } from "../components/multiSelect";
import { BACKEND_URL } from "../constants";

const loaderProp = ({ src }) => {
  return src;
};

const Navbar = () => {
  const router = useRouter();

  const [teams, setTeams] = React.useState([]);

  useEffect(() => {
    fetch(`${BACKEND_URL}/team/all`)
      .then((res) => res.json())
      .then((data) => {
        setTeams(data.data);
      })
      .catch((err) => {
        console.log(err);
      });
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
