"use client";

import React, { useMemo } from "react";

import { createColumnHelper } from "@tanstack/table-core";

import LineChart from "../../../../components/Figures/Line";
import InsightsTable from "../../../../components/Table/InsightsTable";
import { formatCell } from "../../../../components/Table/shared";
import { CURR_YEAR } from "../../../../constants";
import { round } from "../../../../utils";
import { SummaryRow, TeamData, TeamYearsData } from "./types";

const columnHelper = createColumnHelper<SummaryRow>();

const SummaryOverviewSection = ({
  teamData,
  teamYearsData,
}: {
  teamData: TeamData | undefined;
  teamYearsData: TeamYearsData | undefined;
}) => {
  const includeDistrict = teamData?.district;
  const includeState = teamData?.state;

  const columns = useMemo<any>(
    () =>
      [
        columnHelper.accessor("year", {
          cell: (info) => formatCell(info),
          header: "Year",
        }),
        columnHelper.accessor("norm_epa", {
          cell: (info) => formatCell(info),
          header: "Normalized EPA",
        }),
        columnHelper.accessor("epa_rank", {
          cell: (info) => formatCell(info),
          header: "World EPA Rank",
        }),
        columnHelper.accessor("epa_percentile", {
          cell: (info) => formatCell(info),
          header: "World EPA Percentile",
        }),
        columnHelper.accessor("country_epa_rank", {
          cell: (info) => formatCell(info),
          header: "Country EPA Rank",
        }),
        columnHelper.accessor("country_epa_percentile", {
          cell: (info) => formatCell(info),
          header: "Country EPA Percentile",
        }),
        includeDistrict &&
          columnHelper.accessor("district_epa_rank", {
            cell: (info) => formatCell(info),
            header: "District EPA Rank",
          }),
        includeDistrict &&
          columnHelper.accessor("district_epa_percentile", {
            cell: (info) => formatCell(info),
            header: "District EPA Percentile",
          }),
        includeState &&
          columnHelper.accessor("state_epa_rank", {
            cell: (info) => formatCell(info),
            header: "State EPA Rank",
          }),
        includeState &&
          columnHelper.accessor("state_epa_percentile", {
            cell: (info) => formatCell(info),
            header: "State EPA Percentile",
          }),
      ].filter(Boolean),
    [includeDistrict, includeState]
  );

  if (!teamData || !teamYearsData) {
    return (
      <div className="w-full h-auto flex flex-col justify-center items-center px-2">Loading...</div>
    );
  }

  const filteredTeamYearsData = teamYearsData
    .filter((x) => x.year >= teamData.rookie_year && x.year < CURR_YEAR)
    .sort((a, b) => a.year - b.year);

  const tableData = filteredTeamYearsData
    .map((teamYear) => ({
      year: teamYear.year,
      norm_epa: round(teamYear.norm_epa, 0),
      epa_rank: teamYear.epa_rank || "N/A",
      epa_percentile: teamYear?.epa_percentile
        ? Math.min(99.9, 100 * (1 - teamYear.epa_percentile)).toFixed(1) + "%"
        : "N/A",
      country_epa_rank: teamYear.country_epa_rank || "N/A",
      country_epa_percentile: teamYear?.country_epa_percentile
        ? Math.min(99.9, 100 * (1 - teamYear.country_epa_percentile)).toFixed(1) + "%"
        : "N/A",
      district_epa_rank: teamYear.district_epa_rank || "N/A",
      district_epa_percentile: teamYear?.district_epa_percentile
        ? Math.min(99.9, 100 * (1 - teamYear.district_epa_percentile)).toFixed(1) + "%"
        : "N/A",
      state_epa_rank: teamYear.state_epa_rank || "N/A",
      state_epa_percentile: teamYear?.state_epa_percentile
        ? Math.min(99.9, 100 * (1 - teamYear.state_epa_percentile)).toFixed(1) + "%"
        : "N/A",
    }))
    .reverse();

  const xMin = Math.min(...filteredTeamYearsData.map((x) => x.year));
  const xMax = Math.max(...filteredTeamYearsData.map((x) => x.year));

  let roundedYMin = Math.floor(Math.min(...filteredTeamYearsData.map((x) => x.norm_epa)) / 50) * 50;
  roundedYMin = Math.min(1400, Math.max(roundedYMin - 50, 1200));

  let roundedYMax = Math.ceil(Math.max(...filteredTeamYearsData.map((x) => x.norm_epa)) / 50) * 50;
  roundedYMax = Math.min(roundedYMax + 50, 2200);

  let lineData = [
    {
      id: "Baseline",
      data: [
        {
          x: xMin,
          y: 1500,
          label: xMin.toString(),
        },
        {
          x: xMax,
          y: 1500,
          label: xMax.toString(),
        },
      ],
    },
    {
      id: teamData.num.toString(),
      data: filteredTeamYearsData.map((teamYear) => ({
        x: teamYear.year,
        y: round(teamYear.norm_epa, 0),
        label: teamYear.year.toString(),
      })),
    },
  ];

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold mb-4">Years Summary</div>
      <InsightsTable
        title={"Team Insights"}
        data={tableData}
        columns={columns}
        searchCols={["year"]}
        csvFilename={`${teamData.team}_summary.csv`}
        includeKey={false}
      />
      <div className="w-full text-2xl font-bold mb-4">Normalized EPA over Time</div>
      <LineChart
        data={lineData}
        xAxis="Year"
        yAxis="Norm EPA"
        enableArea
        xMin={xMin}
        xMax={xMax}
        yMin={roundedYMin}
        yMax={roundedYMax}
      />
    </div>
  );
};

export default SummaryOverviewSection;
