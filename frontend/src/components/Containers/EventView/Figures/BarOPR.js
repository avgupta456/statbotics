import React from "react";

import { ResponsiveBar } from "@nivo/bar";

import styles from "./../EventView.module.css";

class BarChart extends React.Component {
  render() {
    const data = this.props.data;
    const keys = this.props.keys;

    return (
      <div className={styles.gray}>
        <ResponsiveBar
          data={data}
          keys={keys}
          indexBy="team"
          margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
          padding={0.3}
          groupMode="stacked"
          colors={{ scheme: "set1" }}
          tooltip={({ id, data, value, color }) => (
            <strong style={{ color }}>
              {data["team"]} ({id}): {value}
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
            legend: "OPR",
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
          animate={false}
        />
      </div>
    );
  }
}

export default BarChart;
