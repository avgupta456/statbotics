"use client";

import React, { useMemo, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../../components/Table/InsightsTable";
import { TeamLink, formatCell, formatEPACell } from "../../../../components/Table/shared";
import { formatNumber } from "../../../../components/utils";
import { CURR_YEAR, RPMapping } from "../../../../constants";
import { round, truncate } from "../../../../utils";
import { Data } from "./types";

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
};

const columnHelper = createColumnHelper<TeamEventInsights>();
const detailedColumnHelper = createColumnHelper<DetailedTeamEventInsights>();

const PageEventInsightsTable = ({ eventId, data }: { eventId: string; data: Data }) => {
  const [disableHighlight, setDisableHighlight] = useState(false);

  const sortFunc = (a, b) => {
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
        num: teamEvent.num ?? -1,
        team: teamEvent.team ? truncate(teamEvent.team, 30) : "N/A",
        first_event: teamEvent.first_event ?? false,
        unitless_epa: round(teamEvent.unitless_epa, 0) ?? "N/A",
        norm_epa: round(teamEvent.norm_epa, 0) ?? "N/A",
        total_epa: round(teamEvent.total_epa, 1) ?? 0,
        auto_epa: round(teamEvent.auto_epa, 1) ?? "N/A",
        teleop_epa: round(teamEvent.teleop_epa, 1) ?? "N/A",
        endgame_epa: round(teamEvent.endgame_epa, 1) ?? "N/A",
        rank: teamEvent.rank ?? -1,
      };
    })
    .sort(sortFunc);

  const detailedEventInsightsData: DetailedTeamEventInsights[] = data.team_events
    .map((teamEvent) => {
      return {
        num: teamEvent.num ?? -1,
        team: teamEvent.team ? truncate(teamEvent.team, 30) : "N/A",
        first_event: teamEvent.first_event ?? false,
        unitless_epa: round(teamEvent.unitless_epa, 0) ?? "N/A",
        norm_epa: round(teamEvent.norm_epa, 0) ?? "N/A",
        total_epa: round(teamEvent.total_epa, 1) ?? 0,
        auto_epa: round(teamEvent.auto_epa, 1) ?? "N/A",
        teleop_epa: round(teamEvent.teleop_epa, 1) ?? "N/A",
        endgame_epa: round(teamEvent.endgame_epa, 1) ?? "N/A",
        rank: teamEvent.rank ?? -1,
        rps: teamEvent.rps ?? 0,
        rps_per_match: teamEvent.rps_per_match.toFixed(2),
        record: `${teamEvent.qual_wins}-${teamEvent.qual_losses}-${teamEvent.qual_ties}`,
      };
    })
    .sort(sortFunc);

  const maxRank = Math.max(...eventInsightsData.map((team) => team.rank));

  const year = data.year.year;
  const columns = useMemo<any>(
    () =>
      [
        columnHelper.accessor("num", {
          cell: (info) => formatNumber(info.getValue()),
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
      ].filter(Boolean),
    [year, data, maxRank, disableHighlight]
  );

  const detailedColumns = useMemo<any>(
    () =>
      [
        detailedColumnHelper.accessor("num", {
          cell: (info) => formatNumber(info.getValue()),
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

  const numProjections = eventInsightsData.filter(
    (row) => row.rank === -1 && row.first_event
  ).length;

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
      <div className="w-full px-4 border-t-[1px] border-gray-200 mb-4">
        {numProjections > 0 && (
          <div className="w-full text-xs mt-4">
            <strong>1.</strong> Yellow highlighted teams have not played yet. Their EPA rating is
            only a projection.
          </div>
        )}
      </div>
    </div>
  );
};

export default PageEventInsightsTable;
