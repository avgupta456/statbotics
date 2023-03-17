import React, { useEffect, useMemo, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import InsightsTable from "../../../../components/Table/InsightsTable";
import { TeamLink, formatCell, formatPercentileCell } from "../../../../components/Table/shared";
import { formatNumber } from "../../../../components/utils";
import { readTBA, round } from "../../../../utils";
import { Data } from "./types";

const getAlliances = async (eventId: string) => {
  const rawAlliances = await readTBA(`/event/${eventId}/alliances`);
  const alliances = rawAlliances?.map((alliance, i) => ({
    rank: i + 1,
    teams: alliance?.picks?.map((pick) => parseInt(pick?.slice(3))),
    record: `${alliance?.status?.record?.wins}-${alliance?.status?.record?.losses}-${alliance?.status?.record?.ties}`,
    status: alliance?.status?.status,
  }));

  return alliances;
};

export type AllianceInsights = {
  rank: number;
  team1: number;
  team2: number;
  team3: number;
  team4?: number;
  total_epa: number;
  epa1: number;
  epa2: number;
  epa3: number;
  epa4?: number;
  record: string;
};

const columnHelper = createColumnHelper<AllianceInsights>();

const AlliancesSection = ({
  year,
  eventId,
  data,
}: {
  year: number;
  eventId: string;
  data: Data;
}) => {
  const [alliances, setAlliances] = useState(null);
  const [disableHighlight, setDisableHighlight] = useState(false);

  useEffect(() => {
    getAlliances(eventId).then((alliances) => setAlliances(alliances));
  }, [eventId]);

  const teamToEPA = {};
  data?.team_events?.forEach((teamEvent) => {
    teamToEPA[teamEvent?.num] = teamEvent?.total_epa;
  });

  const allianceInsightsData: AllianceInsights[] = alliances?.map((alliance) => {
    const epa1 = teamToEPA[alliance?.teams?.[0]] ?? 0;
    const epa2 = teamToEPA[alliance?.teams?.[1]] ?? 0;
    const epa3 = teamToEPA[alliance?.teams?.[2]] ?? 0;
    const epa4 = teamToEPA[alliance?.teams?.[3]] ?? 0;

    return {
      rank: alliance.rank,
      team1: alliance.teams?.[0],
      team2: alliance.teams?.[1],
      team3: alliance.teams?.[2],
      team4: alliance.teams?.[3],
      total_epa: round(epa1 + epa2 + Math.max(epa3, epa4), 0),
      epa1: round(epa1, 1),
      epa2: round(epa2, 1),
      epa3: round(epa3, 1),
      epa4: round(epa4, 1),
      record: alliance.record,
    };
  });

  const columns = useMemo<any>(
    () => [
      columnHelper.accessor("rank", {
        cell: (info) => formatNumber(info.getValue()),
        header: "Rank",
      }),
      columnHelper.accessor("team1", {
        cell: (info) =>
          info.getValue()
            ? TeamLink({ team: info.getValue(), num: info.getValue(), year, small: true })
            : "",
        header: "Captain",
      }),
      columnHelper.accessor("team2", {
        cell: (info) =>
          info.getValue()
            ? TeamLink({ team: info.getValue(), num: info.getValue(), year, small: true })
            : "",
        header: "Pick 1",
      }),
      columnHelper.accessor("team3", {
        cell: (info) =>
          info.getValue()
            ? TeamLink({ team: info.getValue(), num: info.getValue(), year, small: true })
            : "",
        header: "Pick 2",
      }),
      columnHelper.accessor("team4", {
        cell: (info) =>
          info.getValue()
            ? TeamLink({ team: info.getValue(), num: info.getValue(), year, small: true })
            : "",
        header: "Pick 3",
      }),
      columnHelper.accessor("total_epa", {
        cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight, 2.5),
        header: "Total EPA",
      }),
      columnHelper.accessor("epa1", {
        cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight),
        header: "Captain EPA",
      }),
      columnHelper.accessor("epa2", {
        cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight),
        header: "Pick 1 EPA",
      }),
      columnHelper.accessor("epa3", {
        cell: (info) => formatPercentileCell(data.year.total_stats, info, disableHighlight),
        header: "Pick 2 EPA",
      }),
      columnHelper.accessor("epa4", {
        cell: (info) =>
          info.getValue() === 0
            ? formatCell(info)
            : formatPercentileCell(data.year.total_stats, info, disableHighlight),
        header: "Pick 3 EPA",
      }),
      columnHelper.accessor("record", {
        cell: (info) => formatCell(info),
        header: "Record",
      }),
    ],
    [year, data.year, disableHighlight]
  );

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      {alliances && alliances.length > 0 && (
        <InsightsTable
          title={"Alliance Insights"}
          data={allianceInsightsData}
          columns={columns}
          searchCols={["team1", "team2", "team3", "team4"]}
          csvFilename={`${eventId}_alliance_insights.csv`}
          toggleDisableHighlight={() => setDisableHighlight(!disableHighlight)}
        />
      )}
      <div className="h-4" />
    </div>
  );
};

export default AlliancesSection;
