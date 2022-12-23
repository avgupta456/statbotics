"use client";

import { line } from "d3-shape";
import regression from "regression";

import React from "react";

import { ResponsiveScatterPlot } from "@nivo/scatterplot";

// TypeScript Hack
const BestFitLine: any = (props) => {
  const { nodes, xScale, yScale } = props;

  console.log(nodes);
  nodes.sort((a, b) => a.data.x - b.data.x);
  const points = nodes.map(function (node, i) {
    return [node.data.x, node.data.y];
  });

  let results1 = regression.logarithmic(points);
  let results2 = regression.linear(points);
  let results = results1;
  if (Math.abs(results2["r2"]) > Math.abs(results1["r2"])) {
    results = results2;
  }

  const lineGenerator_1: any = line();
  const lineGenerator_2: any = lineGenerator_1.x((node) => xScale(node.data.x));
  const lineGenerator = lineGenerator_2.y((node) => yScale(results.predict(node.data.x)[1]));

  return (
    <path
      d={lineGenerator(nodes)}
      fill="none"
      stroke={"rgb(76, 175, 74)"}
      style={{ pointerEvents: "none" }}
    />
  );
};

const ScatterPlot = ({ data, axis }: { data: any; axis: any }) => {
  if (data === undefined || data.length === 0) {
    return <div></div>;
  }

  let cleanData = data.filter((x) => x.data[0]["x"] > 0 && x.data[0]["y"] > 0);

  return (
    <ResponsiveScatterPlot
      data={cleanData}
      margin={{ top: 60, right: 40, bottom: 70, left: 90 }}
      xScale={{ type: "linear", min: "auto", max: "auto" }}
      yScale={{ type: "linear", min: "auto", max: "auto" }}
      tooltip={({ node }) => {
        const hashId = `scatter-tooltip-${node.id}`;
        setTimeout(() => {
          const tooltip = document.getElementById(hashId);
          if (tooltip) {
            tooltip.classList.remove("invisible");
          }
        }, 200);
        return (
          <strong
            id={hashId}
            style={{ color: "rgb(55,126,184)" }}
            className="invisible bg-white p-2 rounded text-sm"
          >
            {parseInt(node["id"])}: (Rank: {node["data"]["x"]}, {axis}: {node["data"]["y"]})
          </strong>
        );
      }}
      colors="rgb(55,126,184)"
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
  );
};

export default ScatterPlot;
