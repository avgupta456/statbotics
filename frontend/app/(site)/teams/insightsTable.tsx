"use client";

import React, { useMemo, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../components/Table/InsightsTable";
import { EventLink, TeamLink, formatCell, formatEPACell } from "../../../components/Table/shared";
import { filterData } from "../../../components/filter";
import { FilterBar } from "../../../components/filterBar";
import { APITeamYear } from "../../../components/types/api";
import { formatNumber } from "../../../components/utils";
import { CURR_YEAR, RPMapping } from "../../../constants";
import { round, truncate } from "../../../utils";
import { TeamYearData } from "../types";

export type TeamYearInsights = {
  num: number;
  team: string;
  epa_rank: number;
  total_epa: number; // used for sorting
  norm_epa: number; // used for historical years
  unitless_epa: number; // used for current year
  auto_epa: number | string;
  teleop_epa: number | string;
  endgame_epa: number | string;
  rp_1_epa: number | string;
  rp_2_epa: number | string;
  next_event_key?: string;
  next_event_name?: string;
  next_event_week?: number | string;
  record: string;
};

const columnHelper = createColumnHelper<TeamYearInsights>();

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

  const allTeamYears = data.team_years
    .sort((a, b) => b.total_epa - a.total_epa)
    .map((teamYear: APITeamYear, i) => ({
      ...teamYear,
      // overwrite epa_rank with index (since we lazy update epa_rank)
      epa_rank: i + 1,
    }));

  const yearInsightsData: TeamYearInsights[] = filterData(allTeamYears, actualFilters)
    .filter((teamYear: APITeamYear) => showProjections || teamYear.count > 0)
    .map((teamYear: APITeamYear) => {
      const wins = teamYear.wins ?? 0;
      const losses = teamYear.losses ?? 0;
      const ties = teamYear.ties ?? 0;
      return {
        num: teamYear.num ?? -1,
        team: teamYear.team ? truncate(teamYear.team, 30) : "N/A",
        epa_rank: teamYear.epa_rank ?? -1,
        total_epa: round(teamYear.total_epa, 1) ?? 0,
        norm_epa: round(teamYear.norm_epa, 0) ?? 0,
        unitless_epa: round(teamYear.unitless_epa, 0) ?? 0,
        auto_epa: round(teamYear.auto_epa, 1) ?? "N/A",
        teleop_epa: round(teamYear.teleop_epa, 1) ?? "N/A",
        endgame_epa: round(teamYear.endgame_epa, 1) ?? "N/A",
        rp_1_epa: round(teamYear.rp_1_epa, 2) ?? "N/A",
        rp_2_epa: round(teamYear.rp_2_epa, 2) ?? "N/A",
        next_event_key: teamYear.next_event_key ?? "N/A",
        next_event_name: teamYear.next_event_name ?? "N/A",
        next_event_week: teamYear.next_event_week ?? "N/A",
        record: `${wins}-${losses}-${ties}`,
        winrate: ((wins + ties / 2) / Math.max(wins + losses + ties, 1)).toFixed(3),
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
      columnHelper.accessor("epa_rank", {
        cell: (info) => formatCell(info),
        header: "EPA Rank",
      }),
      year < CURR_YEAR &&
        columnHelper.accessor("norm_epa", {
          cell: (info) => formatCell(info),
          header: "Normalized EPA",
        }),
      year >= CURR_YEAR &&
        columnHelper.accessor("unitless_epa", {
          cell: (info) => formatCell(info),
          header: "Unitless EPA",
        }),
      columnHelper.accessor("total_epa", {
        cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight),
        header: "EPA",
      }),
      year >= 2016 &&
        columnHelper.accessor("auto_epa", {
          cell: (info) => formatEPACell(data.year.auto_stats, info, disableHighlight),
          header: "Auto EPA",
        }),
      year >= 2016 &&
        columnHelper.accessor("teleop_epa", {
          cell: (info) => formatEPACell(data.year.teleop_stats, info, disableHighlight),
          header: "Teleop EPA",
        }),
      year >= 2016 &&
        columnHelper.accessor("endgame_epa", {
          cell: (info) => formatEPACell(data.year.endgame_stats, info, disableHighlight),
          header: "Endgame EPA",
        }),
      year == CURR_YEAR &&
        columnHelper.accessor("next_event_name", {
          cell: (info) =>
            EventLink({ key: info.row.original.next_event_key, event: info.getValue() }),
          header: "Next Event",
        }),
      columnHelper.accessor("record", {
        cell: (info) => formatCell(info),
        header: "Record",
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
      detailedColumnHelper.accessor("epa_rank", {
        cell: (info) => formatCell(info),
        header: "EPA Rank",
      }),
      year < CURR_YEAR &&
        detailedColumnHelper.accessor("norm_epa", {
          cell: (info) => formatCell(info),
          header: "Normalized EPA",
        }),
      year >= CURR_YEAR &&
        detailedColumnHelper.accessor("unitless_epa", {
          cell: (info) => formatCell(info),
          header: "Unitless EPA",
        }),
      detailedColumnHelper.accessor("total_epa", {
        cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight),
        header: "EPA",
      }),
      year >= 2016 &&
        detailedColumnHelper.accessor("auto_epa", {
          cell: (info) => formatEPACell(data.year.auto_stats, info, disableHighlight),
          header: "Auto EPA",
        }),
      year >= 2016 &&
        detailedColumnHelper.accessor("teleop_epa", {
          cell: (info) => formatEPACell(data.year.teleop_stats, info, disableHighlight),
          header: "Teleop EPA",
        }),
      year >= 2016 &&
        detailedColumnHelper.accessor("endgame_epa", {
          cell: (info) => formatEPACell(data.year.endgame_stats, info, disableHighlight),
          header: "Endgame EPA",
        }),
      year >= 2016 &&
        detailedColumnHelper.accessor("rp_1_epa", {
          cell: (info) => formatEPACell(data.year.rp_1_stats, info, disableHighlight),
          header: RPMapping[year][0],
        }),
      year >= 2016 &&
        detailedColumnHelper.accessor("rp_2_epa", {
          cell: (info) => formatEPACell(data.year.rp_2_stats, info, disableHighlight),
          header: RPMapping[year][1],
        }),
      year == CURR_YEAR &&
        detailedColumnHelper.accessor("next_event_name", {
          cell: (info) =>
            EventLink({ key: info.row.original.next_event_key, event: info.getValue() }),
          header: "Next Event",
        }),
      detailedColumnHelper.accessor("record", {
        cell: (info) => formatCell(info),
        header: "Record",
      }),
      detailedColumnHelper.accessor("winrate", {
        cell: (info) => formatCell(info),
        header: "Winrate",
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
        title={"Team Insights"}
        data={yearInsightsData}
        columns={columns}
        detailedData={yearInsightsData}
        detailedColumns={detailedColumns}
        searchCols={["num", "team"]}
        csvFilename={`${year}_insights.csv`}
        toggleDisableHighlight={() => setDisableHighlight(!disableHighlight)}
      />
    </div>
  );
};

export default PageTeamInsightsTable;
