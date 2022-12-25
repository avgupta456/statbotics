"use client";

import React from "react";

import { LineData } from "../types/figures";
import LineChart from "./Line";

const EventLineChart = () => {
  const lineData: LineData[] = [
    {
      id: "Test",
      data: [
        {
          x: 1,
          y: 2,
        },
        {
          x: 2,
          y: 3,
        },
        {
          x: 3,
          y: 4,
        },
      ],
    },
  ];

  return <LineChart data={lineData} />;
};

export default EventLineChart;
