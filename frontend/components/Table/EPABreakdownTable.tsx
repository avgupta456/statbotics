import React, { useMemo, useState } from "react";

import Link from "next/link";

import { createColumnHelper } from "@tanstack/react-table";

import { round, truncate } from "../../utils";
import { APITeamEvent, APITeamYear, APIYear } from "../types/api";
import { formatNumber } from "../utils";
import InsightsTable from "./InsightsTable";
import { TeamLink, formatEPACell } from "./shared";

export type EPABreakdown = {
  num: number;
  team: string;
  total_epa: number; // used for sorting
  auto_cycles: number | string;
  teleop_cycles: number | string;
  total_cycles: number | string;
  links: number | string;
  cube_cycles: number | string;
  cone_cycles: number | string;
  bot_cycles: number | string;
  mid_cycles: number | string;
  top_cycles: number | string;
};

const columnHelper = createColumnHelper<EPABreakdown>();

const detailedColumnHelper = createColumnHelper<any>();

const EPABreakdownTable = ({
  year,
  yearData,
  data,
  csvFilename,
}: {
  year: number;
  yearData: APIYear;
  data: (APITeamYear | APITeamEvent)[];
  csvFilename: string;
}) => {
  const [disableHighlight, setDisableHighlight] = useState(false);

  const yearInsightsData: EPABreakdown[] = data
    .sort((a, b) => b.total_epa - a.total_epa)
    .map((team: APITeamYear | APITeamEvent) => {
      return {
        num: team.num ?? -1,
        team: team.team ? truncate(team.team, 30) : "N/A",
        total_epa: round(team?.total_epa, 1) ?? -1,
        auto_cycles: round(team?.epa_breakdown?.auto_cycles, 1) ?? "N/A",
        auto_points: round(team?.epa_breakdown?.auto_points, 1) ?? "N/A",
        teleop_cycles: round(team?.epa_breakdown?.teleop_cycles, 1) ?? "N/A",
        teleop_points: round(team?.epa_breakdown?.teleop_points, 1) ?? "N/A",
        total_cycles: round(team?.epa_breakdown?.total_cycles, 1) ?? "N/A",
        total_points: round(team?.epa_breakdown?.total_points, 1) ?? "N/A",
        links: round(team?.epa_breakdown?.links, 1) ?? "N/A",
        cube_cycles: round(team?.epa_breakdown?.cube_cycles, 1) ?? "N/A",
        cube_points: round(team?.epa_breakdown?.cube_points, 1) ?? "N/A",
        cone_cycles: round(team?.epa_breakdown?.cone_cycles, 1) ?? "N/A",
        cone_points: round(team?.epa_breakdown?.cone_points, 1) ?? "N/A",
        bot_cycles: round(team?.epa_breakdown?.bot_cycles, 1) ?? "N/A",
        mid_cycles: round(team?.epa_breakdown?.mid_cycles, 1) ?? "N/A",
        top_cycles: round(team?.epa_breakdown?.top_cycles, 1) ?? "N/A",
      };
    });

  const columns = useMemo<any>(() => {
    const showColumns = [
      {
        header: "Team",
        columns: [
          columnHelper.accessor("num", {
            cell: (info) => formatNumber(info.getValue()),
            header: "Number",
          }),
          columnHelper.accessor("team", {
            cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
            header: "Name",
          }),
        ],
      },
      {
        header: "Overall",
        columns: [
          columnHelper.accessor("total_epa", {
            cell: (info) => formatEPACell(yearData.total_stats, info, disableHighlight),
            header: "EPA",
          }),
          columnHelper.accessor("total_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.total_cycles, info, disableHighlight),
            header: "Total Cycles",
          }),
          columnHelper.accessor("links", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.links, info, disableHighlight),
            header: "Links",
          }),
        ],
      },
      {
        header: "Cycle Time",
        columns: [
          columnHelper.accessor("auto_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.auto_cycles, info, disableHighlight),
            header: "Auto Cycles",
          }),
          columnHelper.accessor("teleop_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.teleop_cycles, info, disableHighlight),
            header: "Teleop Cycles",
          }),
        ],
      },
      {
        header: "Cycle Location",
        columns: [
          columnHelper.accessor("bot_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.bot_cycles, info, disableHighlight),
            header: "Bot Cycles",
          }),
          columnHelper.accessor("mid_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.mid_cycles, info, disableHighlight),
            header: "Mid Cycles",
          }),
          columnHelper.accessor("top_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.top_cycles, info, disableHighlight),
            header: "Top Cycles",
          }),
        ],
      },
      {
        header: "Cycle Type",
        columns: [
          columnHelper.accessor("cube_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.cube_cycles, info, disableHighlight),
            header: "Cube Cycles",
          }),
          columnHelper.accessor("cone_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.cone_cycles, info, disableHighlight),
            header: "Cone Cycles",
          }),
        ],
      },
    ].filter((x) => x);
    return showColumns;
  }, [year, yearData, disableHighlight]);

  const detailedColumns = useMemo<any>(() => {
    const showColumns = [
      {
        header: "Team",
        columns: [
          detailedColumnHelper.accessor("num", {
            cell: (info) => formatNumber(info.getValue()),
            header: "Number",
          }),
          detailedColumnHelper.accessor("team", {
            cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
            header: "Name",
          }),
        ],
      },
      {
        header: "Overall",
        columns: [
          detailedColumnHelper.accessor("total_epa", {
            cell: (info) => formatEPACell(yearData.total_stats, info, disableHighlight),
            header: "EPA",
          }),
          detailedColumnHelper.accessor("total_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.total_cycles, info, disableHighlight),
            header: "Total Cycles",
          }),
          detailedColumnHelper.accessor("links", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.links, info, disableHighlight),
            header: "Links",
          }),
          detailedColumnHelper.accessor("total_points", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.total_points, info, disableHighlight),
            header: "Grid Points",
          }),
        ],
      },
      {
        header: "Cycle Time",
        columns: [
          detailedColumnHelper.accessor("auto_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.auto_cycles, info, disableHighlight),
            header: "Auto Cycles",
          }),
          detailedColumnHelper.accessor("auto_points", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.auto_points, info, disableHighlight),
            header: "Auto Grid Points",
          }),
          detailedColumnHelper.accessor("teleop_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.teleop_cycles, info, disableHighlight),
            header: "Teleop Cycles",
          }),
          detailedColumnHelper.accessor("teleop_points", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.teleop_points, info, disableHighlight),
            header: "Teleop Grid Points",
          }),
        ],
      },
      {
        header: "Cycle Location",
        columns: [
          detailedColumnHelper.accessor("bot_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.bot_cycles, info, disableHighlight),
            header: "Bot Cycles",
          }),
          detailedColumnHelper.accessor("mid_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.mid_cycles, info, disableHighlight),
            header: "Mid Cycles",
          }),
          detailedColumnHelper.accessor("top_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.top_cycles, info, disableHighlight),
            header: "Top Cycles",
          }),
        ],
      },
      {
        header: "Cycle Type",
        columns: [
          detailedColumnHelper.accessor("cube_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.cube_cycles, info, disableHighlight),
            header: "Cube Cycles",
          }),
          detailedColumnHelper.accessor("cube_points", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.cube_points, info, disableHighlight),
            header: "Cube Points",
          }),
          detailedColumnHelper.accessor("cone_cycles", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.cone_cycles, info, disableHighlight),
            header: "Cone Cycles",
          }),
          detailedColumnHelper.accessor("cone_points", {
            cell: (info) =>
              formatEPACell(yearData.epa_breakdown_stats.cone_points, info, disableHighlight),
            header: "Cone Points",
          }),
        ],
      },
    ].filter((x) => x);
    return showColumns;
  }, [year, yearData, disableHighlight]);

  return (
    <>
      <div className="w-full my-4 px-16">
        EPA Breakdowns apply the same EPA formula used to predict match outcomes to more granular
        data. <strong>EPA Breakdowns are currently in BETA</strong>, and I cannot guarantee their
        accuracy or completeness. They are only available on the website and update at a much slower
        pace than the rest of the site. If you have any questions or bug reports, please reach out
        on{" "}
        <Link
          href="https://www.chiefdelphi.com/t/statbotics-2023-season/423703"
          rel="noopener noreferrer"
          target="_blank"
          className="text_link"
        >
          Chief Delphi
        </Link>
        . <strong>Last Updated:</strong> 5:00 AM ET, 4/1/2023
      </div>
      <InsightsTable
        title={"EPA Breakdown (BETA)"}
        data={yearInsightsData}
        columns={columns}
        detailedData={yearInsightsData}
        detailedColumns={detailedColumns}
        searchCols={["num", "team"]}
        csvFilename={csvFilename}
        toggleDisableHighlight={() => setDisableHighlight(!disableHighlight)}
      />
    </>
  );
};

export default EPABreakdownTable;
