"use client";

import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import HC_more from "highcharts/highcharts-more";

import React, { useState } from "react";

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
};

const BubbleChart = ({ data }: { data: ScatterData[] }) => {
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
            value: 40,
          },
          y: -15,
          borderWidth: 1,
          style: {
            fontSize: "10px",
            color: "gray",
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
        data: data,
      },
    ],
  };

  // use bottom-padding to make the chart responsive
  return (
    <div className="w-full">
      <HighchartsReact highcharts={Highcharts} options={options} />
    </div>
  );
};

export default BubbleChart;
