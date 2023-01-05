"use client";

import React, { useEffect, useState } from "react";

const NotFound = ({ type }: { type: string }) => {
  // wait one second before rendering
  // this is so that the not found page doesn't flash

  const [render, setRender] = useState(false);

  useEffect(() => {
    setTimeout(() => {
      setRender(true);
    }, 1000);
  }, []);

  if (!render) {
    return null;
  }

  return (
    <div className="w-full flex-grow flex flex-col justify-center items-center gap-2">
      <div className="text-xl lg:text-2xl">{type} not found</div>
      <div className="text-xl lg:text-2xl">¯\_(ツ)_/¯</div>
    </div>
  );
};

export default NotFound;
