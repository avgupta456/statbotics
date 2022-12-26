"use client";

import React, { useState } from "react";

import Image from "next/image";
import Link from "next/link";

const loaderProp = ({ src }) => {
  return src;
};

const Navbar = () => {
  return (
    <div
      className="text-gray-100 shadow-md body-font sticky top-0 z-50 px-4 py-3 flex"
      style={{ background: "#343A40" }}
    >
      <div className="flex items-center gap-2 text-xl font-thin mr-8">
        <Image
          src="/circ_favicon.ico"
          alt="logo"
          width={30}
          height={30}
          loader={loaderProp}
          unoptimized
        />
        <Link href="/">Statbotics</Link>
      </div>
      <div className="flex items-center text-base text-gray-300 hover:text-gray-100 font-thin">
        <Link href="/teams">Teams</Link>
      </div>
      <div className="flex-grow" />
      <div className="flex items-center gap-2 text-base font-thin">Search Bar</div>
    </div>
  );
};

export default Navbar;
