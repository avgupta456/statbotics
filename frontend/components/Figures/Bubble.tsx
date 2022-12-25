"use client";

import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_more from "highcharts/highcharts-more";

import React, { useState } from "react";

import { ColumnBar, columnOptionsDict } from "../columns";
import { FilterBar, filterData } from "../filter";
import { TeamYear, YearStats } from "../types/api";

if (typeof Highcharts === "object") {
  HC_more(Highcharts);
}

type ScatterData = {
  x: number;
  y: number;
  z: number;
  num: number;
  labelInt: number;
};

const BubbleChart = ({ data, yearStats }: { data: TeamYear[]; yearStats: YearStats }) => {
  const [filters, setFilters] = useState({ state: "", country: "", district: "" });
  const [columns, setColumns] = useState({
    x: "Teleop EPA",
    y: "Auto + Endgame EPA",
    z: "Endgame EPA",
  });

  const filteredData: TeamYear[] = filterData(data, filters);

  const xAxis = columnOptionsDict[columns.x];
  const yAxis = columnOptionsDict[columns.y];
  const zAxis = columnOptionsDict[columns.z];

  const scatterData: ScatterData[] = filteredData.map((datum) => ({
    x: xAxis.accessor(datum),
    y: yAxis.accessor(datum),
    z: zAxis.accessor(datum),
    num: datum.num,
    labelInt: 0,
  }));

  const xs = scatterData.map((datum) => datum.x);
  const ys = scatterData.map((datum) => datum.y);
  const zs = scatterData.map((datum) => datum.z);
  const len = Math.min(50, xs.length - 1);
  const xCutoff = xs.sort((a, b) => b - a)[len];
  const yCutoff = ys.sort((a, b) => b - a)[len];
  const zCutoff = zs.sort((a, b) => b - a)[len];

  const filteredDataSubset: ScatterData[] = scatterData.map((datum) => ({
    x: datum.x,
    y: datum.y,
    z: datum.z,
    num: datum.num,
    labelInt: datum.x > xCutoff || datum.y > yCutoff || datum.z > zCutoff ? 1 : 0,
  }));

  const options: Highcharts.Options = {
    title: {
      text: "",
    },
    legend: {
      enabled: false,
    },
    xAxis: {
      title: {
        text: xAxis["label"],
      },
      min: 0,
    },
    yAxis: {
      title: {
        text: yAxis["label"],
      },
      min: 0,
    },
    tooltip: {
      useHTML: true,
      headerFormat: "<table>",
      pointFormat:
        '<tr><th colspan="2"><h3>{point.num}</h3></th></tr>' +
        (xAxis.label !== "Constant" ? `<tr><th>${xAxis.label}: </th><td>{point.x}</td></tr>` : "") +
        (yAxis.label !== "Constant" ? `<tr><th>${yAxis.label}: </th><td>{point.y}</td></tr>` : "") +
        (zAxis.label !== "Constant" ? `<tr><th>${zAxis.label}: </th><td>{point.z}</td></tr>` : ""),
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
            property: "labelInt",
            operator: ">",
            value: 0,
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
        minSize: zAxis.label === "Constant" ? 6 : 2,
        maxSize: zAxis.label === "Constant" ? 6 : 12,
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
  };

  // use bottom-padding to make the chart responsive
  return (
    <div className="w-full">
      <div className="flex items-end justify-center mb-2">
        <ColumnBar columns={columns} setColumns={setColumns} />
        <div className="w-0.5 h-10 ml-2 mr-4 bg-gray-500 rounded" />
        <FilterBar filters={filters} setFilters={setFilters} />
      </div>
      <div className="w-4/5 mx-auto">
        <HighchartsReact highcharts={Highcharts} options={options} />
      </div>
    </div>
  );
};

export default BubbleChart;
