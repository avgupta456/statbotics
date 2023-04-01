"use client";

import React from "react";

import EPABreakdownTable from "../../../../components/Table/EPABreakdownTable";
import { Data } from "./types";

const EPABreakdownSection = ({
  year,
  eventId,
  data,
}: {
  year: number;
  eventId: string;
  data: Data;
}) => {
  return (
    <div className="w-full flex flex-col justify-center items-center">
      <EPABreakdownTable year={year} yearData={data.year} data={data.team_events} />
    </div>
  );
};

export default EPABreakdownSection;
