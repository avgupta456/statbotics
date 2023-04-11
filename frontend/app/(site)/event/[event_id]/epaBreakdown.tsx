"use client";

import React, { useEffect, useState } from "react";

import EPABreakdownTable from "../../../../components/Table/EPABreakdownTable";
import { getEPABreakdown, getEPABreakdownPercentiles, log } from "../../../../utils";
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
  const [epaBreakdownPercentiles, setEPABreakdownPercentiles] = useState(null);
  const [epaBreakdown, setEPABreakdown] = useState(null);

  useEffect(() => {
    if (!epaBreakdownPercentiles && data.year) {
      getEPABreakdownPercentiles(setEPABreakdownPercentiles);
    }

    if (!epaBreakdown && data.year) {
      getEPABreakdown(setEPABreakdown);
    }
  }, [epaBreakdownPercentiles, epaBreakdown, data.year]);

  const epaBreakdownData = data.team_events.map((teamEvent) => {
    const teamYearEPABreakdown = epaBreakdown?.[teamEvent.num] ?? {};
    return { ...teamEvent, epa_breakdown: teamYearEPABreakdown };
  });

  const epaBreakdownYearData = { ...data.year, epa_breakdown_stats: epaBreakdownPercentiles ?? {} };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      {epaBreakdownPercentiles && epaBreakdown ? (
        <EPABreakdownTable
          year={year}
          yearData={epaBreakdownYearData}
          data={epaBreakdownData}
          csvFilename={`${year}_epa_breakdown.csv`}
        />
      ) : (
        <div className="w-full flex-grow flex flex-col items-center justify-center">
          <div className="text-gray-700 mt-4">Loading data, please wait...</div>
        </div>
      )}
    </div>
  );
};

export default EPABreakdownSection;
