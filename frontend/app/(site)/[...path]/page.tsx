"use client";

import React from "react";

import { notFound, useRouter } from "next/navigation";

const Page = ({ params }: { params: { path: string[] } }) => {
  const router = useRouter();
  const { path } = params;

  if (path.length !== 1) {
    notFound();
  }

  const firstPath = path[0];

  // if all digits
  if (/^\d+$/.test(firstPath)) {
    router.push(`/team/${firstPath}`);
  } else if (firstPath.includes("_")) {
    router.push(`/match/${firstPath}`);
  } else {
    router.push(`/event/${firstPath}`);
  }
};

export default Page;
