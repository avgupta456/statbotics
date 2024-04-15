"use client";

import React from "react";

import { ResponsiveBar } from "@nivo/bar";

import { capitalize } from "../../utils";

const DelayedTooltip = ({ indexBy, id, data, value, color }) => {
  const hashId = `bar-tooltip-${data[indexBy]}-${id}`;
  setTimeout(() => {
    const tooltip = document.getElementById(hashId);
    if (tooltip) {
      tooltip.classList.remove("invisible");
    }
  }, 200);
  return (
    <div id={hashId} className="invisible bg-white rounded shadow p-2" style={{ color }}>
      <div className="text-sm font-bold">{`${capitalize(indexBy)} ${data[indexBy]}`}</div>
      <div className="text-sm">{`${id}: ${value}`}</div>
    </div>
  );
};

const sharedConfig: any = (indexBy: string) => ({
  motionConfig: "gentle",
  indexBy: indexBy,
  padding: 0.1,
  tooltip: (args) => DelayedTooltip({ indexBy, ...args }),
  groupMode: "stacked",
  colors: { scheme: "category10" },
  borderColor: { from: "color", modifiers: [["darker", 1.6]] },
  axisTop: null,
  axisRight: null,
  axisBottom: {
    tickSize: 5,
    tickPadding: 5,
    tickRotation: 0,
    legend: capitalize(indexBy),
    legendPosition: "middle",
    legendOffset: 32,
  },
  axisLeft: {
    tickSize: 5,
    tickPadding: 5,
    tickRotation: 0,
    legend: "EPA",
    legendPosition: "middle",
    legendOffset: -40,
  },
  enableLabel: false,
});

export const BarChart = ({
  data,
  indexBy,
  keys,
}: {
  data: any[];
  indexBy: string;
  keys: any[];
}) => {
  return (
    <div className="w-full h-[500px] flex">
      <ResponsiveBar
        {...sharedConfig(indexBy)}
        data={data}
        keys={keys}
        margin={{ top: 20, right: 130, bottom: 50, left: 60 }}
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

export const BarChartNoLegend = ({
  data,
  indexBy,
  keys,
}: {
  data: any[];
  indexBy;
  keys: any[];
}) => {
  return (
    <div className="w-full h-[500px] flex">
      <ResponsiveBar
        {...sharedConfig(indexBy)}
        data={data}
        keys={keys}
        margin={{ top: 20, right: 0, bottom: 50, left: 60 }}
      />
    </div>
  );
};
