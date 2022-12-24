"use client";

import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_more from "highcharts/highcharts-more";

import React, { useState } from "react";

import { filterData } from "../filter";
import { YearStats } from "../types/api";

if (typeof Highcharts === "object") {
  HC_more(Highcharts);
}

type ScatterData = {
  x: number;
  y: number;
  z: number;
  num: number;
  auto: number;
  total: number;
  state: string;
  country: string;
  district: string;
};

const BubbleChart = ({ data, yearStats }: { data: ScatterData[]; yearStats: YearStats }) => {
  const filteredData = filterData(data, { state: "CA" });
  const filteredDataSubset = filteredData.map((datum) => ({
    x: datum.x,
    y: datum.y,
    z: datum.z,
    num: datum.num,
    auto: datum.auto,
    total: datum.total,
  }));

  const totals = filteredDataSubset.map((datum) => datum.total);
  const totalsCutoff = totals.sort((a, b) => b - a)[40];

  const options: Highcharts.Options = {
    title: {
      text: "",
    },
    legend: {
      enabled: false,
    },
    xAxis: {
      title: {
        text: "Teleop EPA",
      },
      min: 0,
    },
    yAxis: {
      title: {
        text: "Auto EPA + Endgame EPA",
      },
      min: 0,
    },
    tooltip: {
      useHTML: true,
      headerFormat: "<table>",
      pointFormat:
        '<tr><th colspan="2"><h3>{point.num}</h3></th></tr>' +
        "<tr><th>Auto EPA:    </th><td>{point.auto}</td></tr>" +
        "<tr><th>Teleop EPA:  </th><td>{point.x}</td></tr>" +
        "<tr><th>Endgame EPA: </th><td>{point.z}</td></tr>",
      footerFormat: "</table>",
      followPointer: true,
    },

    chart: {
      reflow: true,
      height: (9 / 16) * 100 + "%", // 16:9 ratio
      backgroundColor: "transparent",
      type: "bubble",
      plotBorderWidth: 1,
      zooming: {
        type: "xy",
        resetButton: {
          position: {
            align: "right",
            verticalAlign: "top",
            x: -10,
            y: 10,
          },
        },
      },
    },
    plotOptions: {
      series: {
        dataLabels: {
          enabled: true,
          format: "{point.num}",
          filter: {
            property: "total",
            operator: ">",
            value: Math.min(totalsCutoff, yearStats.total.p90),
          },
          y: -15,
          borderWidth: 1,
          style: {
            fontSize: "10px",
            color: "black",
            textOutline: "none",
          },
        },
      },
      bubble: {
        minSize: 2,
        maxSize: 20,
        color: "#3b82f6",
      },
    },
    series: [
      {
        type: "bubble",
        data: filteredDataSubset,
      },
    ],
    credits: {
      enabled: false,
    },
    caption: {
      text: "Size of Bubble is Endgame EPA",
      align: "right",
      verticalAlign: "bottom",
      y: -75,
      x: -10,
    },
  };

  // use bottom-padding to make the chart responsive
  return (
    <div className="w-full">
      <HighchartsReact highcharts={Highcharts} options={options} />
    </div>
  );
};

export default BubbleChart;
