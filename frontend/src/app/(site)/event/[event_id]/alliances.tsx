import React, { useEffect, useMemo, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import { BarChartNoLegend } from "../../../../components/Figures/Bar";
import InsightsTable from "../../../../components/Table/InsightsTable";
import { TeamLink, formatCell, formatEPACell } from "../../../../components/Table/shared";
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

// Weird naming to use in the BarChart
export type AllianceInsights = {
  rank: number;
  team1: string;
  team2: string;
  team3: string;
  team4?: string;
  total_epa: number;
  "Captain EPA": number;
  "First Pick EPA": number;
  "Second Pick EPA": number;
  "Third Pick EPA": number;
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
      team: alliance.rank,
      rank: alliance.rank,
      team1: alliance.teams?.[0],
      team2: alliance.teams?.[1],
      team3: alliance.teams?.[2],
      team4: alliance.teams?.[3],
      total_epa: round(epa1 + epa2 + Math.max(epa3, epa4), 0),
      "Captain EPA": round(epa1, 1),
      "First Pick EPA": round(epa2, 1),
      "Second Pick EPA": round(epa3, 1),
      "Third Pick EPA": round(epa4, 1),
      record: alliance.record,
    };
  });

  const columns = useMemo<any>(
    () =>
      [
        columnHelper.accessor("rank", {
          cell: (info) => info.getValue(),
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
          cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight, 2.5),
          header: "Total EPA",
        }),
        columnHelper.accessor("Captain EPA", {
          cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight),
          header: "Captain EPA",
        }),
        columnHelper.accessor("First Pick EPA", {
          cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight),
          header: "Pick 1 EPA",
        }),
        columnHelper.accessor("Second Pick EPA", {
          cell: (info) => formatEPACell(data.year.total_stats, info, disableHighlight),
          header: "Pick 2 EPA",
        }),
        columnHelper.accessor("Third Pick EPA", {
          cell: (info) =>
            info.getValue() === 0
              ? formatCell(info)
              : formatEPACell(data.year.total_stats, info, disableHighlight),
          header: "Pick 3 EPA",
        }),
        year !== 2015 &&
          columnHelper.accessor("record", {
            cell: (info) => formatCell(info),
            header: "Record",
          }),
      ].filter(Boolean),
    [year, data.year, disableHighlight]
  );

  return (
    <div className="w-full h-auto flex flex-col justify-center items-center px-2">
      <div className="w-full text-2xl font-bold mb-4">Alliance Insights</div>
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
      <div className="w-full text-2xl font-bold pt-8 mb-4 border-t-2 border-gray-300">
        Alliance Bar Chart
      </div>
      {alliances && alliances.length > 0 && (
        <BarChartNoLegend
          data={allianceInsightsData}
          indexBy="rank"
          keys={["Captain EPA", "First Pick EPA", "Second Pick EPA"]}
        />
      )}
    </div>
  );
};

export default AlliancesSection;
