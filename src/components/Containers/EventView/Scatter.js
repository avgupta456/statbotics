import React from "react";

import regression from "regression";

import { ResponsiveScatterPlot } from "@nivo/scatterplot";
import { line } from "d3-shape";

import styles from "./EventView.module.css";

const BestFitLine = ({ data, xScale, yScale }) => {
  data.sort((a, b) => a.data[0]["x"] - b.data[0]["x"]);
  console.log(data);
  const points = data.map(function (x, i) {
    return [x.data[0]["x"], x.data[0]["y"]];
  });

  const results = regression.polynomial(points, { order: 2 });
  console.log(results.predict(1));

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
    var data = this.props.data;

    return (
      <div className={styles.gray}>
        <ResponsiveScatterPlot
          data={data}
          margin={{ top: 60, right: 140, bottom: 70, left: 90 }}
          xScale={{ type: "linear", min: "auto", max: "auto" }}
          yScale={{ type: "linear", min: "auto", max: "auto" }}
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
            legend: "Elo Rating",
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
