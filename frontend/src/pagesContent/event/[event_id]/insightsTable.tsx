"use client";

import React, { useMemo, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../components/Table/InsightsTable";
import { TeamLink, formatCell, formatEPACell } from "../../../components/Table/shared";
import { CURR_YEAR, RP_NAMES } from "../../../constants";
import { APITeamEvent } from "../../../types/api";
import { EventData } from "../../../types/data";
import { round, truncate } from "../../../utils";

export type TeamEventInsights = {
  num: number;
  team: string;
  first_event: boolean;
  rank: number;
  unitless_epa: number | string;
  norm_epa: number | string;
  total_epa: number;
  auto_epa: number | string;
  teleop_epa: number | string;
  endgame_epa: number | string;
  rp_1_epa: number | string;
  rp_2_epa: number | string;
  rp_3_epa: number | string;
};

export type DetailedTeamEventInsights = {
  num: number;
  team: string;
  first_event: boolean;
  rank: number;
  rps: number;
  rps_per_match: string;
  record: string;
  unitless_epa: number | string;
  norm_epa: number | string;
  total_epa: number;
  auto_epa: number | string;
  teleop_epa: number | string;
  endgame_epa: number | string;
  rp_1_epa: number | string;
  rp_2_epa: number | string;
  rp_3_epa: number | string;
};

const columnHelper = createColumnHelper<TeamEventInsights>();
const detailedColumnHelper = createColumnHelper<DetailedTeamEventInsights>();

const PageEventInsightsTable = ({ eventId, data }: { eventId: string; data: EventData }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);

  const sortFunc = (a: TeamEventInsights, b: TeamEventInsights) => {
    if (a.rank === -1 && b.rank === -1) {
      return b.total_epa - a.total_epa;
    } else if (a.rank === -1) {
      return 1;
    } else if (b.rank === -1) {
      return -1;
    } else {
      return a.rank - b.rank || b.total_epa - a.total_epa;
    }
  };

  const eventInsightsData: TeamEventInsights[] = data.team_events
    .map((teamEvent) => {
      return {
        num: teamEvent?.team ?? -1,
        team: teamEvent?.team_name ? truncate(teamEvent?.team_name, 30) : "N/A",
        first_event: teamEvent?.first_event ?? false,
        unitless_epa: round(teamEvent?.epa?.unitless, 0) ?? "N/A",
        norm_epa: round(teamEvent?.epa?.norm, 0) ?? "N/A",
        total_epa: round(teamEvent?.epa?.breakdown?.total_points, 1) ?? 0,
        auto_epa: round(teamEvent?.epa?.breakdown?.auto_points, 1) ?? "N/A",
        teleop_epa: round(teamEvent?.epa?.breakdown?.teleop_points, 1) ?? "N/A",
        endgame_epa: round(teamEvent?.epa?.breakdown?.endgame_points, 1) ?? "N/A",
        rp_1_epa: round(teamEvent?.epa?.breakdown?.rp_1, 2) ?? "N/A",
        rp_2_epa: round(teamEvent?.epa?.breakdown?.rp_2, 2) ?? "N/A",
        rp_3_epa: round(teamEvent?.epa?.breakdown?.rp_3, 1) ?? "N/A",
        rank: teamEvent?.record?.qual?.rank ?? -1,
      };
    })
    .sort(sortFunc);

  const detailedEventInsightsData: DetailedTeamEventInsights[] = data.team_events
    .map((teamEvent) => ({
      num: teamEvent?.team ?? null,
      team: teamEvent?.team_name ? truncate(teamEvent?.team_name, 30) : "N/A",
      first_event: teamEvent?.first_event ?? false,
      unitless_epa: round(teamEvent?.epa?.unitless, 0) ?? "N/A",
      norm_epa: round(teamEvent?.epa?.norm, 0) ?? "N/A",
      total_epa: round(teamEvent?.epa?.breakdown?.total_points, 1) ?? 0,
      auto_epa: round(teamEvent?.epa?.breakdown?.auto_points, 1) ?? "N/A",
      teleop_epa: round(teamEvent?.epa?.breakdown?.teleop_points, 1) ?? "N/A",
      endgame_epa: round(teamEvent?.epa?.breakdown?.endgame_points, 1) ?? "N/A",
      rp_1_epa: round(teamEvent?.epa?.breakdown?.rp_1, 2) ?? "N/A",
      rp_2_epa: round(teamEvent?.epa?.breakdown?.rp_2, 2) ?? "N/A",
      rp_3_epa: round(teamEvent?.epa?.breakdown?.rp_3, 2) ?? "N/A",
      rank: teamEvent?.record?.qual?.rank ?? -1,
      rps: teamEvent?.record?.qual?.rps ?? 0,
      rps_per_match: teamEvent?.record?.qual?.rps_per_match.toFixed(2),
      record: `${teamEvent?.record?.qual.wins}-${teamEvent?.record?.qual?.losses}-${teamEvent?.record?.qual?.ties}`,
    }))
    .sort(sortFunc);

  const maxRank = Math.max(...eventInsightsData.map((team) => team.rank));

  const year = data.year.year;
  const columns = useMemo<any>(
    () =>
      [
        columnHelper.accessor("num", {
          cell: (info) => info.getValue(),
          header: "Number",
        }),
        columnHelper.accessor("team", {
          cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
          header: "Name",
        }),
        maxRank > 0 &&
          columnHelper.accessor("rank", {
            cell: (info) => formatCell(info),
            header: "Rank",
          }),
        year >= CURR_YEAR &&
          columnHelper.accessor("unitless_epa", {
            cell: (info) => formatCell(info),
            header: "Unitless EPA",
          }),
        year < CURR_YEAR &&
          columnHelper.accessor("norm_epa", {
            cell: (info) => formatCell(info),
            header: "Norm EPA",
          }),
        columnHelper.accessor("total_epa", {
          cell: (info) => formatEPACell(data.year.percentiles.total_points, info, disableHighlight),
          header: "EPA",
        }),
        year >= 2016 &&
          columnHelper.accessor("auto_epa", {
            cell: (info) =>
              formatEPACell(data.year.percentiles.auto_points, info, disableHighlight),
            header: "Auto EPA",
          }),
        year >= 2016 &&
          columnHelper.accessor("teleop_epa", {
            cell: (info) =>
              formatEPACell(data.year.percentiles.teleop_points, info, disableHighlight),
            header: "Teleop EPA",
          }),
        year >= 2016 &&
          columnHelper.accessor("endgame_epa", {
            cell: (info) =>
              formatEPACell(data.year.percentiles.endgame_points, info, disableHighlight),
            header: "Endgame EPA",
          }),
        year >= 2016 &&
          columnHelper.accessor("rp_1_epa", {
            cell: (info) => formatEPACell(data.year.percentiles.rp_1, info, disableHighlight),
            header: `${RP_NAMES?.[data.year.year]?.[0]} EPA`,
          }),
        year >= 2016 &&
          columnHelper.accessor("rp_2_epa", {
            cell: (info) => formatEPACell(data.year.percentiles.rp_2, info, disableHighlight),
            header: `${RP_NAMES?.[data.year.year]?.[1]} EPA`,
          }),
        year >= 2025 &&
          columnHelper.accessor("rp_3_epa", {
            cell: (info) => formatEPACell(data.year.percentiles.rp_3, info, disableHighlight),
            header: `${RP_NAMES?.[data.year.year]?.[2]} EPA`,
          }),
      ].filter(Boolean),
    [year, data, maxRank, disableHighlight]
  );

  const detailedColumns = useMemo<any>(
    () =>
      [
        detailedColumnHelper.accessor("num", {
          cell: (info) => info.getValue(),
          header: "Number",
        }),
        detailedColumnHelper.accessor("team", {
          cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
          header: "Name",
        }),
        maxRank > 0 &&
          detailedColumnHelper.accessor("rank", {
            cell: (info) => formatCell(info),
            header: "Rank",
          }),
        maxRank > 0 &&
          detailedColumnHelper.accessor("rps_per_match", {
            cell: (info) => formatCell(info),
            header: "Ranking Score",
          }),
        year >= CURR_YEAR &&
          detailedColumnHelper.accessor("unitless_epa", {
            cell: (info) => formatCell(info),
            header: "Unitless EPA",
          }),
        year < CURR_YEAR &&
          detailedColumnHelper.accessor("norm_epa", {
            cell: (info) => formatCell(info),
            header: "Norm EPA",
          }),
        detailedColumnHelper.accessor("total_epa", {
          cell: (info) => formatEPACell(data.year.percentiles.total_points, info, disableHighlight),
          header: "EPA",
        }),
        year >= 2016 &&
          detailedColumnHelper.accessor("auto_epa", {
            cell: (info) =>
              formatEPACell(data.year.percentiles.auto_points, info, disableHighlight),
            header: "Auto EPA",
          }),
        year >= 2016 &&
          detailedColumnHelper.accessor("teleop_epa", {
            cell: (info) =>
              formatEPACell(data.year.percentiles.teleop_points, info, disableHighlight),
            header: "Teleop EPA",
          }),
        year >= 2016 &&
          detailedColumnHelper.accessor("endgame_epa", {
            cell: (info) =>
              formatEPACell(data.year.percentiles.endgame_points, info, disableHighlight),
            header: "Endgame EPA",
          }),
        year >= 2016 &&
          detailedColumnHelper.accessor("rp_1_epa", {
            cell: (info) => formatEPACell(data.year.percentiles.rp_1, info, disableHighlight),
            header: `${RP_NAMES?.[data.year.year]?.[0]} EPA`,
          }),
        year >= 2016 &&
          detailedColumnHelper.accessor("rp_2_epa", {
            cell: (info) => formatEPACell(data.year.percentiles.rp_2, info, disableHighlight),
            header: `${RP_NAMES?.[data.year.year]?.[1]} EPA`,
          }),
        year >= 2025 &&
          detailedColumnHelper.accessor("rp_3_epa", {
            cell: (info) => formatEPACell(data.year.percentiles.rp_3, info, disableHighlight),
            header: `${RP_NAMES?.[data.year.year]?.[2]} EPA`,
          }),
        maxRank > 0 &&
          detailedColumnHelper.accessor("record", {
            cell: (info) => formatCell(info),
            header: "Record",
          }),
        maxRank > 0 &&
          detailedColumnHelper.accessor("rps", {
            cell: (info) => formatCell(info),
            header: "RPs",
          }),
      ].filter(Boolean),
    [year, data, maxRank, disableHighlight]
  );

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <InsightsTable
        title={"Team Insights"}
        data={eventInsightsData}
        columns={columns}
        detailedData={detailedEventInsightsData}
        detailedColumns={detailedColumns}
        searchCols={["num", "team"]}
        csvFilename={`${eventId}_team_insights.csv`}
        toggleDisableHighlight={() => setDisableHighlight(!disableHighlight)}
      />
    </div>
  );
};

export default PageEventInsightsTable;
