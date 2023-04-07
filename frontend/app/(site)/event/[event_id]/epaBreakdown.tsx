"use client";

import React, { useEffect, useState } from "react";

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
  const [epaBreakdownPercentiles, setEPABreakdownPercentiles] = useState(null);
  const [epaBreakdown, setEPABreakdown] = useState(null);
  const [eventEpaBreakdown, setEventEpaBreakdown] = useState(null);

  useEffect(() => {
    if (!epaBreakdownPercentiles && data.year) {
      // read json from public folder
      fetch("/data/epa_breakdown_percentiles.json").then((response) => {
        response.json().then((data) => {
          setEPABreakdownPercentiles(data);
        });
      });
    }

    if (!epaBreakdown && data.year) {
      // read json from public folder
      fetch("/data/epa_breakdown.json").then((response) => {
        response.json().then((data) => {
          setEPABreakdown(data);
        });
      });
    }

    if (!eventEpaBreakdown && data.year) {
      // read json from public folder
      fetch(`/data/event_epa_breakdown.json`).then((response) => {
        response.json().then((data) => {
          setEventEpaBreakdown(data);
        });
      });
    }
  }, [epaBreakdownPercentiles, epaBreakdown, eventEpaBreakdown, data.year]);

  const epaBreakdownData = data.team_events.map((teamEvent) => {
    const teamEventEPABreakdown = eventEpaBreakdown?.[`${teamEvent.num}_${eventId}`];
    const teamYearEPABreakdown = epaBreakdown?.[teamEvent.num] ?? {};
    return { ...teamEvent, epa_breakdown: teamEventEPABreakdown ?? teamYearEPABreakdown };
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
