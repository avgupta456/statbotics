"use client";

import React from "react";

import { ResponsivePie } from "@nivo/pie";

type Datum = {
  title: string;
  label: string;
  value: number;
};

const PieChart = ({ data, colors }: { data: Datum[]; colors: string[] }) => {
  if (!(Array.isArray(data) && data.length > 0)) {
    return <div className="w-full h-full flex items-center justify-center">No data to show</div>;
  }

  return (
    <ResponsivePie
      data={data}
      id="title"
      margin={{ right: 40, left: 40 }}
      innerRadius={0.4}
      padAngle={0.7}
      cornerRadius={3}
      activeOuterRadiusOffset={8}
      borderWidth={1}
      borderColor={{ from: "color", modifiers: [["darker", 0.2]] }}
      // Arc Link Settings
      enableArcLinkLabels={false}
      // Arc Label Settings
      arcLabel={(e) => e.data.label}
      arcLabelsSkipAngle={45}
      arcLabelsTextColor="#fff"
      // Tooltip
      tooltip={({ datum }) => (
        <div
          style={{
            fontSize: "14px",
            padding: 6,
            color: datum.color,
            background: "#fff",
            boxShadow: "0px 0px 10px rgba(0, 0, 0, 0.1)",
          }}
        >
          <strong>{datum.data.title}</strong>
          {`: ${datum.data.label}`}
        </div>
      )}
      colors={colors}
    />
  );
};

export default PieChart;
