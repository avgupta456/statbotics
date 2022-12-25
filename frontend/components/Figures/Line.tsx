"use client";

import React from "react";

import { ResponsiveLine } from "@nivo/line";

import { LineData } from "../types/figures";

const LineChart = ({ data }: { data: LineData[] }) => {
  return (
    <ResponsiveLine
      data={data}
      margin={{ top: 20, right: 30, bottom: 50, left: 60 }}
      xScale={{ type: "linear", min: "auto", max: "auto" }}
      yScale={{ type: "linear", min: 0, max: "auto" }}
      curve="linear"
      axisBottom={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: "X",
        legendOffset: 40,
        legendPosition: "middle",
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: "Y",
        legendOffset: -50,
        legendPosition: "middle",
      }}
      colors={{ scheme: "set1" }}
      pointSize={10}
      pointLabel="y"
      pointLabelYOffset={-12}
      useMesh={true}
      legends={[
        {
          anchor: "top-right",
          direction: "column",
          justify: false,
          translateX: 12,
          translateY: 0,
          itemsSpacing: 0,
          itemDirection: "left-to-right",
          itemWidth: 80,
          itemHeight: 20,
          itemOpacity: 0.75,
          symbolSize: 12,
          symbolShape: "circle",
          symbolBorderColor: "rgba(0, 0, 0, .5)",
          effects: [
            {
              on: "hover",
              style: {
                itemBackground: "rgba(0, 0, 0, .03)",
                itemOpacity: 1,
              },
            },
          ],
        },
      ]}
    />
  );
};

export default LineChart;
