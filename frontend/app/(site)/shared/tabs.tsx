"use client";

import React, { useState } from "react";

import { classnames } from "../../../utils";

const TabsSection = ({
  tabs,
  loading,
}: {
  tabs: { title: string; content: React.ReactNode }[];
  loading: boolean;
}) => {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <div className="w-full flex-grow flex flex-col">
      <div className="w-full flex flex-row text-sm md:text-base">
        {tabs.map((tab, index) => (
          <div
            key={`tab-${tab.title}`}
            className={classnames(activeTab === index ? "" : "border-b-[1px] border-gray-200")}
          >
            <button
              className={classnames(
                "border-t-[1px] border-x-[1px] py-2 px-4 rounded-t",
                activeTab === index
                  ? "text-gray-800 border-gray-200"
                  : "text-blue-500 hover:text-blue-600 border-white hover:border-gray-200"
              )}
              onClick={() => setActiveTab(index)}
            >
              {tab.title}
            </button>
          </div>
        ))}
        <div className="flex-grow border-b-[1px] border-gray-200" />
      </div>
      <div className="w-full flex-grow pt-4 px-4 shadow">
        {loading ? (
          <div className="w-full flex-grow flex flex-col items-center justify-center">
            <div className="text-gray-700 mt-4">Loading data, please wait...</div>
          </div>
        ) : (
          <>
            {tabs.map((tab, index) => (
              <div key={`tab-${tab.title}`} className={activeTab === index ? "w-full" : "hidden"}>
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