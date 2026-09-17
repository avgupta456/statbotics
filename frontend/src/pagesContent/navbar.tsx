"use client";

import React, { useState } from "react";
import { BsThreeDots } from "react-icons/bs";
import { GiHamburgerMenu as HamburgerIcon } from "react-icons/gi";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

import SearchSelect from "../components/searchSelect";
import { classnames } from "../utils";

const loaderProp = ({ src }) => {
  return src;
};

const Navbar = () => {
  const [toggle, setToggle] = useState(false);

  // The home page renders its own search on mobile, so the menu doesn't need one there
  const isHome = usePathname() === "/";

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
        <div className="hidden md:flex items-center text-base text-gray-300 hover:text-gray-100 font-thin mr-4">
          <Link href="/docs/rest">API</Link>
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
                <div className="w-36 py-1 text-sm text-center">View GitHub</div>
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
          <SearchSelect instanceId="navbar-search" className="w-60 mr-2" />
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
        {!isHome && (
          <>
            <div className="my-2 h-[1px] bg-gray-600" />
            <div className="mx-auto">
              <SearchSelect
                instanceId="navbar-search-mobile"
                className="w-60 mr-2"
                onSelect={() => setToggle(false)}
              />
            </div>
          </>
        )}
        <div className="h-2" />
      </div>
    </div>
  );
};

export default Navbar;
