import React from "react";

import { ResponsiveBar } from "@nivo/bar";

import styles from "./../EventView.module.css";

class BarChart extends React.Component {
  render() {
    let data = this.props.data;
    const minValue = 1500;

    data = data.map(function (x, i) {
      return {
        team: x["team"],
        Elo: x["Elo"] - minValue,
      };
    });

    return (
      <div className={styles.gray}>
        <ResponsiveBar
          data={data}
          keys={["Elo"]}
          indexBy="team"
          margin={{ top: 50, right: 30, bottom: 50, left: 60 }}
          padding={0.3}
          groupMode="stacked"
          colors="rgb(55,126,184)"
          tooltip={({ id, data, value, color }) => (
            <strong style={{ color }}>
              {data["team"]} {id}: {value + minValue}
            </strong>
          )}
          defs={[
            {
              id: "dots",
              type: "patternDots",
              background: "inherit",
              color: "#38bcb2",
              size: 4,
              padding: 1,
              stagger: true,
            },
            {
              id: "lines",
              type: "patternLines",
              background: "inherit",
              color: "#eed312",
              rotation: -45,
              lineWidth: 6,
              spacing: 10,
            },
          ]}
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
            legend: "Elo",
            legendPosition: "middle",
            legendOffset: -40,
            format: (v) => `${v + minValue}`,
          }}
          enableLabel={false}
          animate={false}
        />
      </div>
    );
  }
}

export default BarChart;
