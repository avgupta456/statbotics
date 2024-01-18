"use client";

import React from "react";

import { ResponsiveLine } from "@nivo/line";

import { round } from "../../utils/utils";

type LineData = {
  id: string | number;
  data: { x: number; label: string; y: number }[];
};

function LineChart({
  data,
  xAxis,
  yAxis,
  enableArea,
  xMin,
  xMax,
  yMin,
  yMax,
}: {
  data: LineData[];
  xAxis: string;
  yAxis: string;
  enableArea?: boolean;
  xMin?: number;
  xMax?: number;
  yMin?: number | "auto";
  yMax?: number | "auto";
}) {
  const xLabels = data.reduce((acc: any, curr: LineData) => {
    const xLabel = curr.data.reduce(
      (acc2: any, curr2: any) => ({ ...acc2, [curr2.x]: curr2.label }),
      {},
    );
    return { ...acc, [curr.id]: xLabel };
  }, {});

  const finalXMin = xMin || 0;
  const finalXMax = xMax || (data.length === 0 ? 1 : "auto");

  const finalYMin = yMin || (yAxis.includes("Norm") ? 1200 : 0);
  const finalYMax = yMax || (data.length === 0 ? 1 : "auto");

  const finalEnableArea =
    enableArea !== undefined
      ? enableArea
      : !(yAxis.toLowerCase().includes("rp") || yAxis.includes("Norm"));

  return (
    <div className="flex h-[500px] w-full">
      <ResponsiveLine
        data={data}
        margin={{ top: 20, right: 30, bottom: 50, left: 60 }}
        xScale={{ type: "linear", min: finalXMin, max: finalXMax }}
        yScale={{ type: "linear", min: finalYMin, max: finalYMax }}
        curve="monotoneX"
        axisBottom={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: xAxis,
          legendOffset: 40,
          legendPosition: "middle",
        }}
        axisLeft={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: yAxis,
          legendOffset: -50,
          legendPosition: "middle",
        }}
        colors={{ scheme: "category10" }}
        pointSize={5}
        enableArea={finalEnableArea && data.length <= 1}
        areaOpacity={0.1}
        pointLabel="y"
        pointLabelYOffset={-12}
        useMesh
        // eslint-disable-next-line react/no-unstable-nested-components
        tooltip={({ point }) => {
          const y: any = point.data.yFormatted;
          const xLabel = xLabels[point.serieId][String(point.data.x)];
          return (
            <div className="rounded bg-white p-2 shadow" style={{ color: point.color }}>
              <div className="text-sm font-bold">{`Team ${point.serieId}`}</div>
              <div className="mb-1 text-xs">{xLabel}</div>
              <div className="text-sm">{`${yAxis}: ${round(parseFloat(y))}`}</div>
            </div>
          );
        }}
        legends={[
          {
            anchor: "bottom-right",
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
            itemBackground: "rgba(255, 255, 255, 1)",
          },
        ]}
      />
    </div>
  );
}

export default LineChart;
