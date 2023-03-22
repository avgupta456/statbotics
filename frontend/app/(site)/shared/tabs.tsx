"use client";

import React, { useState } from "react";

import { useRouter } from "next/navigation";

import { classnames } from "../../../utils";

const TabsSection = ({
  tabs,
  loading,
  error,
}: {
  tabs: { title: string; content: React.ReactNode }[];
  loading: boolean;
  error: boolean;
}) => {
  const router = useRouter();

  let hash = "";
  // check window is defined to prevent build errors
  if (typeof window !== "undefined") {
    hash = window.location.href.split("#")[1];
  }

  const [activeTab, _setActiveTab] = useState(hash);

  const setActiveTab = (title: string) => {
    const formattedTitle = title.toLowerCase().replace(/ /g, "-");
    _setActiveTab(formattedTitle);

    // check window is defined to prevent build errors
    if (typeof window === "undefined") {
      return;
    }

    // remove anything after the last # in the path
    const pathnameNoHash = window?.location?.href?.replace(/#.*$/, "");
    const newPathname = pathnameNoHash + "#" + formattedTitle;
    router.replace(newPathname);
  };

  const rawIndex = tabs.findIndex(
    (tab) => tab.title.toLowerCase().replace(/ /g, "-") === activeTab
  );

  const currIndex = rawIndex >= 0 ? rawIndex : 0;

  return (
    <div className="w-full flex-grow flex flex-col">
      <div className="w-full flex flex-row text-sm md:text-base overflow-x-scroll md:overflow-x-auto scrollbar-hide">
        {tabs.map((tab, index) => (
          <div
            key={`tab-${tab.title}`}
            className={classnames(currIndex === index ? "" : "border-b-[1px] border-gray-200")}
          >
            <button
              className={classnames(
                "w-32 border-t-[1px] border-x-[1px] py-2 rounded-t",
                currIndex === index
                  ? "text-gray-800 border-gray-200"
                  : "text-blue-500 hover:text-blue-600 border-white hover:border-gray-200"
              )}
              onClick={() => setActiveTab(tab.title)}
            >
              {tab.title}
            </button>
          </div>
        ))}
        <div className="flex-grow border-b-[1px] border-gray-200" />
      </div>
      <div className="w-full flex-grow pt-4 px-4 shadow">
        {error ? (
          <div className="w-full flex-grow flex flex-col items-center justify-center">
            <div className="text-gray-700 mt-4">An error occurred, please try again later.</div>
          </div>
        ) : loading ? (
          <div className="w-full flex-grow flex flex-col items-center justify-center">
            <div className="text-gray-700 mt-4">Loading data, please wait...</div>
          </div>
        ) : (
          <>
            {tabs.map((tab, index) => (
              <div key={`tab-${tab.title}`} className={currIndex === index ? "w-full" : "hidden"}>
                {tab.content}
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
};

export default TabsSection;
