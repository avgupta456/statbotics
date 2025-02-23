import React, { useMemo, useState } from "react";

import { createColumnHelper } from "@tanstack/react-table";

import { APITeamEvent, APITeamYear, APIYear } from "../../types/api";
import { round, truncate } from "../../utils";
import InsightsTable from "./InsightsTable";
import { TeamLink, formatEPACell } from "./shared";

const columnHelper = createColumnHelper<any>();

type Config = {
  keys: {
    [key: string]: {
      name: string;
      digits: number;
    };
  };
  layout: {
    [key: number]: {
      [key: string]: string[];
    };
  };
};

const configs: { [key: number]: Config } = {
  2025: {
    keys: {
      total_points: { name: "Total Points", digits: 1 },
      auto_points: { name: "Auto Points", digits: 1 },
      teleop_points: { name: "Teleop Points", digits: 1 },
      endgame_points: { name: "Endgame Points", digits: 1 },
      auto_coral: { name: "Auto Coral", digits: 1 },
      auto_coral_points: { name: "Auto Coral Points", digits: 1 },
      teleop_coral: { name: "Teleop Coral", digits: 1 },
      teleop_coral_points: { name: "Teleop Coral Points", digits: 1 },
      coral_l1: { name: "Coral L1", digits: 1 },
      coral_l2: { name: "Coral L2", digits: 1 },
      coral_l3: { name: "Coral L3", digits: 1 },
      coral_l4: { name: "Coral L4", digits: 1 },
      total_coral_points: { name: "Total Coral Points", digits: 1 },
      processor_algae: { name: "Processor Algae", digits: 1 },
      processor_algae_points: { name: "Processor Algae Points", digits: 1 },
      net_algae: { name: "Net Algae", digits: 1 },
      net_algae_points: { name: "Net Algae Points", digits: 1 },
      total_algae: { name: "Total Algae", digits: 1 },
      total_algae_points: { name: "Total Algae Points", digits: 1 },
      total_game_pieces: { name: "Total Game Pieces", digits: 1 },
    },
    layout: {
      0: {
        Overall: ["total_points", "total_game_pieces", "total_coral_points", "total_algae_points"],
        Coral: ["auto_coral", "teleop_coral", "coral_l1", "coral_l2", "coral_l3", "coral_l4"],
        Algae: ["processor_algae", "net_algae"],
        Endgame: ["endgame_points"],
      },
      1: {
        Overall: [
          "total_points",
          "auto_points",
          "teleop_points",
          "total_game_pieces",
          "total_coral_points",
          "total_algae_points",
        ],
        Coral: [
          "auto_coral",
          "auto_coral_points",
          "teleop_coral",
          "teleop_coral_points",
          "coral_l1",
          "coral_l2",
          "coral_l3",
          "coral_l4",
        ],
        Algae: ["processor_algae", "processor_algae_points", "net_algae", "net_algae_points"],
        Endgame: ["endgame_points"],
      },
    },
  },
  2024: {
    keys: {
      total_points: { name: "Total Points", digits: 1 },
      total_notes: { name: "Total Notes", digits: 1 },
      total_note_points: { name: "Total Note Points", digits: 1 },
      auto_notes: { name: "Auto Notes", digits: 1 },
      auto_points: { name: "Auto Points", digits: 1 },
      teleop_notes: { name: "Teleop Notes", digits: 1 },
      teleop_points: { name: "Teleop Points", digits: 1 },
      amp_notes: { name: "Amp Notes", digits: 1 },
      speaker_notes: { name: "Speaker Notes", digits: 1 },
      amplified_notes: { name: "Amplified Notes", digits: 1 },
      endgame_points: { name: "Endgame Points", digits: 1 },
      endgame_park_points: { name: "Park Points", digits: 2 },
      endgame_on_stage_points: { name: "On Stage Points", digits: 1 },
      endgame_harmony_points: { name: "Harmony Points", digits: 2 },
      endgame_trap_points: { name: "Trap Points", digits: 1 },
      endgame_spotlight_points: { name: "Spotlight Points", digits: 2 },
    },
    layout: {
      0: {
        Overall: ["total_points", "total_notes", "total_note_points"],
        "Scoring Period": ["auto_notes", "teleop_notes"],
        "Scoring Location": ["amp_notes", "speaker_notes", "amplified_notes"],
        Endgame: ["endgame_points"],
      },
      1: {
        Overall: ["total_points", "total_notes", "total_note_points"],
        "Scoring Period": ["auto_notes", "auto_points", "teleop_notes", "teleop_points"],
        "Scoring Location": ["amp_notes", "speaker_notes", "amplified_notes"],
        Endgame: [
          "endgame_points",
          "endgame_park_points",
          "endgame_on_stage_points",
          "endgame_harmony_points",
          "endgame_trap_points",
          "endgame_spotlight_points",
        ],
      },
    },
  },
};

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

  const config = configs[year];
  const allCols = Object.keys(config.keys);

  const yearInsightsData: any[] = data
    .sort((a, b) => b?.epa?.breakdown?.total_points - a?.epa?.breakdown?.total_points)
    .map((team) => {
      const teamEventToName = (team: APITeamYear | APITeamEvent) => {
        if ("name" in team) {
          return team.name;
        } else if ("team_name" in team) {
          return team.team_name;
        } else {
          return "N/A";
        }
      };

      return {
        ...{ num: team.team, team: truncate(teamEventToName(team), 30) },
        ...allCols.reduce((acc, col) => {
          const value = team?.epa?.breakdown?.[col];
          return { ...acc, [col]: round(value, config.keys[col].digits) };
        }, {}),
      };
    });

  const { columns, detailedColumns } = useMemo<any>(() => {
    const getColumns = (detailed: number) => [
      ...[
        {
          header: "Team",
          columns: [
            columnHelper.accessor("num", {
              cell: (info) => info.getValue(),
              header: "Number",
            }),
            columnHelper.accessor("team", {
              cell: (info) => TeamLink({ team: info.getValue(), num: info.row.original.num, year }),
              header: "Name",
            }),
          ],
        },
      ],
      ...Object.entries(config.layout[detailed]).reduce((acc, [header, cols]) => {
        return [
          ...acc,
          {
            header,
            columns: cols.map((col) =>
              columnHelper.accessor(col, {
                cell: (info) => formatEPACell(yearData?.percentiles[col], info, disableHighlight),
                header: config.keys[col]["name"],
              })
            ),
          },
        ];
      }, []),
    ];
    return { columns: getColumns(0), detailedColumns: getColumns(1) };
  }, [config, yearData, year, disableHighlight]);

  return (
    <>
      <InsightsTable
        title={"EPA Breakdown"}
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
