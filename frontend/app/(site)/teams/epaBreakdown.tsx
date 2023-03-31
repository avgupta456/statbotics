"use client";

import React, { useMemo, useState } from "react";

import Link from "next/link";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../components/Table/InsightsTable";
import { TeamLink, formatCell, formatEPACell } from "../../../components/Table/shared";
import { filterData } from "../../../components/filter";
import { FilterBar } from "../../../components/filterBar";
import { APITeamYear } from "../../../components/types/api";
import { formatNumber } from "../../../components/utils";
import { CURR_YEAR } from "../../../constants";
import { round, truncate } from "../../../utils";
import { TeamYearData } from "../types";

export type EPABreakdown = {
  num: number;
  team: string;
  total_epa: number; // used for sorting
  auto_cycles: number | string;
  teleop_cycles: number | string;
  total_cycles: number | string;
};

const columnHelper = createColumnHelper<EPABreakdown>();

const detailedColumnHelper = createColumnHelper<any>();

const PageTeamInsightsTable = ({
  year,
  data,
  filters,
  setFilters,
}: {
  year: number;
  data: TeamYearData;
  filters: { [key: string]: any };
  setFilters: (filters: { [key: string]: any }) => void;
}) => {
  const [disableHighlight, setDisableHighlight] = useState(false);
  const [showProjections, setShowProjections] = useState(true);

  let defaultFilters = {
    country: "",
    state: "",
    district: "",
  };

  if (year === CURR_YEAR) {
    defaultFilters["is_competing"] = "";
  }

  const actualFilters = Object.keys(defaultFilters).reduce(
    (acc, key) => ({ ...acc, [key]: filters[key] || defaultFilters[key] }),
    {}
  );

  const allTeamYears = data.team_years.sort((a, b) => b.total_epa - a.total_epa);

  const yearInsightsData: EPABreakdown[] = filterData(allTeamYears, actualFilters)
    .filter((teamYear: APITeamYear) => showProjections || teamYear.count > 0)
    .map((teamYear: APITeamYear) => {
      return {
        num: teamYear.num ?? -1,
        team: teamYear.team ? truncate(teamYear.team, 30) : "N/A",
        total_epa: round(teamYear?.total_epa, 1) ?? -1,
        auto_cycles: round(teamYear?.epa_breakdown?.auto_cycles, 1) ?? "N/A",
        teleop_cycles: round(teamYear?.epa_breakdown?.teleop_cycles, 1) ?? "N/A",
        total_cycles: round(teamYear?.epa_breakdown?.total_cycles, 1) ?? "N/A",
      };
    });

  const columns = useMemo<any>(() => {
    const showColumns = [
      columnHelper.accessor("num", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Number",
      }),
      columnHelper.accessor("team", {
        cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
        header: "Name",
      }),
      columnHelper.accessor("total_epa", {
        cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight),
        header: "EPA",
      }),
      detailedColumnHelper.accessor("auto_cycles", {
        cell: (info) => formatCell(info),
        header: "Auto Cycles",
      }),
      detailedColumnHelper.accessor("teleop_cycles", {
        cell: (info) => formatCell(info),
        header: "Teleop Cycles",
      }),
      detailedColumnHelper.accessor("total_cycles", {
        cell: (info) => formatCell(info),
        header: "Total Cycles",
      }),
    ].filter((x) => x);
    return showColumns;
  }, [year, data.year, disableHighlight]);

  const detailedColumns = useMemo<any>(() => {
    const showColumns = [
      detailedColumnHelper.accessor("num", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Number",
      }),
      detailedColumnHelper.accessor("team", {
        cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
        header: "Name",
      }),
      detailedColumnHelper.accessor("total_epa", {
        cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight),
        header: "EPA",
      }),
    ].filter((x) => x);
    return showColumns;
  }, [year, data.year, disableHighlight]);

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <div className="flex items-center justify-center">
        <FilterBar
          defaultFilters={defaultFilters}
          filters={actualFilters}
          setFilters={setFilters}
          includeProjections={year === CURR_YEAR}
          showProjections={showProjections}
          setShowProjections={setShowProjections}
        />
      </div>
      <InsightsTable
        title={"EPA Breakdown (BETA)"}
        data={yearInsightsData}
        columns={columns}
        detailedData={yearInsightsData}
        detailedColumns={detailedColumns}
        searchCols={["num", "team"]}
        csvFilename={`${year}_epa_breakdown.csv`}
        toggleDisableHighlight={() => setDisableHighlight(!disableHighlight)}
      />
      <div className="w-full px-4 border-t-[1px] border-gray-200">
        {year >= CURR_YEAR && (
          <>
            <div className="w-full text-xs mt-4">
              <strong>1.</strong> Yellow highlighted teams have not played yet. Their EPA rating is
              only a projection.
            </div>
            <div className="w-full text-xs mb-4">
              <strong>2.</strong> Unitless EPA is a linear function mapping EPA into Elo units. This
              is not the same as Year Normalized EPA for past seasons. See{" "}
              <Link href="/blog/epa" className="text_link">
                blog
              </Link>{" "}
              for more details.
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default PageTeamInsightsTable;
