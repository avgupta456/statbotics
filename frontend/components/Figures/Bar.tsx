"use client";

import React, { useEffect } from "react";

import { ResponsiveBar } from "@nivo/bar";

const BarChart = ({ data, keys }: { data: any[]; keys: any[] }) => {
  return (
    <div className="w-full h-[500px] flex">
      <ResponsiveBar
        motionConfig={"gentle"}
        data={data}
        keys={keys}
        indexBy="team"
        margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
        padding={0.1}
        groupMode="stacked"
        colors={{ scheme: "set1" }}
        tooltip={({ id, data, value, color }) => {
          const hashId = `bar-tooltip-${data["team"]}-${id}`;
          setTimeout(() => {
            const tooltip = document.getElementById(hashId);
            if (tooltip) {
              tooltip.classList.remove("invisible");
            }
          }, 200);
          return (
            <div id={hashId} className="invisible bg-white rounded shadow p-2" style={{ color }}>
              <div className="text-sm font-bold">{`Team ${data["team"]}`}</div>
              <div className="text-sm">{`${id}: ${value}`}</div>
            </div>
          );
        }}
        borderColor={{ from: "color", modifiers: [["darker", 1.6]] }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "Team",
          legendPosition: "middle",
          legendOffset: 32,
        }}
        axisLeft={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "EPA",
          legendPosition: "middle",
          legendOffset: -40,
        }}
        enableLabel={false}
        legends={[
          {
            dataFrom: "keys",
            anchor: "bottom-right",
            direction: "column",
            justify: false,
            translateX: 120,
            translateY: 0,
            itemsSpacing: 2,
            itemWidth: 100,
            itemHeight: 20,
            itemDirection: "left-to-right",
            itemOpacity: 0.85,
            symbolSize: 20,
            effects: [
              {
                on: "hover",
                style: {
                  itemOpacity: 1,
                },
              },
            ],
          },
        ]}
      />
    </div>
  );
};

export default BarChart;
