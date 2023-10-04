"use client";

import { line } from "d3-shape";
import regression from "regression";

import React from "react";

import { ResponsiveScatterPlot } from "@nivo/scatterplot";

import { round } from "../../utils";
import { useColors } from "./use-colors";

const BestFitLine = ({ nodes, xScale, yScale }) => {
  nodes.sort((a, b) => a.data["x"] - b.data["x"]);
  const points = nodes.map(function (x, i) {
    return [x.data["x"], x.data["y"]];
  });

  let results1 = regression.logarithmic(points);
  let results2 = regression.linear(points);
  let results = results1;
  if (Math.abs(results2["r2"]) > Math.abs(results1["r2"])) {
    results = results2;
  }

  const lineGenerator = line()
    .x((x) => xScale(x.data["x"]))
    .y((x) => yScale(results.predict(x.data["x"])[1]));

  return (
    <path
      d={lineGenerator(nodes)}
      fill="none"
      stroke={"rgb(76, 175, 74)"}
      style={{ pointerEvents: "none" }}
    />
  );
};

const ScatterPlot = ({ data, axis }: { data: any[]; axis: string }) => {
  const colors = useColors(data.map((datum) => Number(datum.id)));
  const getColor = (num: number) => colors.get(num) ?? "rgb(55,126,184)";

  return (
    <div className="w-full h-[500px] flex">
      <ResponsiveScatterPlot
        data={data}
        margin={{ top: 20, right: 40, bottom: 70, left: 90 }}
        xScale={{ type: "linear", min: "auto", max: "auto" }}
        yScale={{ type: "linear", min: "auto", max: "auto" }}
        tooltip={({ node }) => {
          return (
            <div
              className="bg-white rounded shadow p-2"
              style={{ color: getColor(Number(node["data"]["id"])) }}
            >
              <div className="text-sm font-bold">{`Team ${node["data"]["id"]}`}</div>
              <div className="text-xs mb-1">{`Rank ${node["data"]["x"]}`}</div>
              <div className="text-sm">{`${axis}: ${round(
                parseFloat(node["data"]["y"].toString())
              )}`}</div>
            </div>
          );
        }}
        colors={(datum) => getColor(Number(datum.serieId))}
        blendMode="multiply"
        axisTop={null}
        axisRight={null}
        axisBottom={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "Actual Rank",
          legendPosition: "middle",
          legendOffset: 46,
        }}
        axisLeft={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: `${axis}`,
          legendPosition: "middle",
          legendOffset: -60,
        }}
        useMesh={false}
        legends={[]}
        layers={["grid", "axes", BestFitLine, "nodes", "markers", "mesh", "legends", "annotations"]}
      />
    </div>
  );
};

export default ScatterPlot;
