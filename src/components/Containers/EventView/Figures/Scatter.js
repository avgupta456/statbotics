import React from "react";

import regression from "regression";

import { ResponsiveScatterPlot } from "@nivo/scatterplot";
import { line } from "d3-shape";

import styles from "./../EventView.module.css";

const BestFitLine = ({ data, xScale, yScale }) => {
  data.sort((a, b) => a.data[0]["x"] - b.data[0]["x"]);
  const points = data.map(function (x, i) {
    return [x.data[0]["x"], x.data[0]["y"]];
  });

  let results1 = regression.logarithmic(points);
  let results2 = regression.linear(points);
  let results = results1;
  if (Math.abs(results2["r2"]) > Math.abs(results1["r2"])) {
    results = results2;
  }

  const lineGenerator = line()
    .x((x) => xScale(x.data[0]["x"]))
    .y((x) => yScale(results.predict(x.data[0]["x"])[1]));

  return (
    <path
      d={lineGenerator(data)}
      fill="none"
      stroke={"rgb(76, 175, 74)"}
      style={{ pointerEvents: "none" }}
    />
  );
};

class ScatterPlot extends React.Component {
  render() {
    const data = this.props.data;
    const axis = this.props.axis;

    return (
      <div className={styles.gray}>
        <ResponsiveScatterPlot
          data={data}
          margin={{ top: 60, right: 40, bottom: 70, left: 90 }}
          xScale={{ type: "linear", min: "auto", max: "auto" }}
          yScale={{ type: "linear", min: "auto", max: "auto" }}
          tooltip={({ node }) => (
            <div
              style={{
                backgroundColor: "rgb(255, 255, 255)",
                padding: "8px",
                borderRadius: "3px",
              }}
            >
              <strong style={{ color: "rgb(55,126,184)" }}>
                {parseInt(node["id"])}: (Rank: {node["data"]["x"]}, {axis}:{" "}
                {node["data"]["y"]})
              </strong>
            </div>
          )}
          colors="rgb(55,126,184)"
          blendMode="multiply"
          axisTop={null}
          axisRight={null}
          axisBottom={{
            orient: "bottom",
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Actual Rank",
            legendPosition: "middle",
            legendOffset: 46,
          }}
          axisLeft={{
            orient: "left",
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: `${axis}`,
            legendPosition: "middle",
            legendOffset: -60,
          }}
          useMesh={false}
          legends={[]}
          layers={[
            "grid",
            "axes",
            BestFitLine,
            "nodes",
            "markers",
            "mesh",
            "legends",
            "annotations",
          ]}
        />
      </div>
    );
  }
}

export default ScatterPlot;
