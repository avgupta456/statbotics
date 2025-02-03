import { useEffect, useState } from "react";

import { APITeamYear } from "../../types/api";
import { CURR_YEAR } from "../../utils/constants";
import { getEPADef } from "./templates/epa";
import { rankDef, teamNameDef, teamNumDef } from "./templates/misc";
import Table from "./templates/table";

export default function TeamYearsBreakdownTable({
  year,
  data,
}: {
  year: number;
  data: APITeamYear[] | undefined;
}) {
  const [expanded, setExpanded] = useState(false);

  const getColumnDefs = (newYear: number, newExpanded: boolean) => {
    const sharedDefs = [rankDef, teamNumDef, teamNameDef];

    if (newYear === 2023) {
      return [
        ...sharedDefs,
        {
          headerName: "Total",
          headerClass: "ag-text-center",
          children: [
            getEPADef("total_points", "Total"),
            getEPADef("total_pieces", "Game Pieces"),
            getEPADef("links", "Links"),
            newExpanded && getEPADef("grid_points", "Grid Points"),
          ].filter(Boolean),
        },
        {
          headerName: "Scoring Period",
          headerClass: "ag-text-center",
          children: [
            getEPADef("auto_pieces", "Auto Pieces"),
            newExpanded && getEPADef("auto_grid_points", "Auto Points"),
            getEPADef("teleop_pieces", "Teleop Pieces"),
            newExpanded && getEPADef("teleop_grid_points", "Teleop Points"),
          ].filter(Boolean),
        },
        {
          headerName: "Scoring Location",
          headerClass: "ag-text-center",
          children: [
            getEPADef("bottom_pieces", "Bottom Pieces"),
            getEPADef("middle_pieces", "Middle Pieces"),
            getEPADef("top_pieces", "Top Pieces"),
          ].filter(Boolean),
        },
        {
          headerName: "Game Piece Type",
          headerClass: "ag-text-center",
          children: [
            getEPADef("cubes_scored", "Cubes Scored"),
            newExpanded && getEPADef("cube_points", "Cube Points"),
            getEPADef("cones_scored", "Cones Scored"),
            newExpanded && getEPADef("cone_points", "Cone Points"),
          ].filter(Boolean),
        },
        newExpanded && {
          headerName: "Charge Station",
          headerClass: "ag-text-center",
          children: [
            getEPADef("auto_charge_station_points", "Auto CS"),
            getEPADef("endgame_charge_station_points", "Endgame CS"),
          ].filter(Boolean),
        },
      ].filter(Boolean);
    }

    if (year === 2024) {
      return [
        ...sharedDefs,
        {
          headerName: "Total",
          headerClass: "ag-text-center",
          children: [
            getEPADef("total_points", "Total"),
            getEPADef("total_notes", "Notes"),
            getEPADef("total_note_points", "Note Points"),
          ],
        },
        {
          headerName: "Scoring Period",
          headerClass: "ag-text-center",
          children: [
            getEPADef("auto_notes", "Auto Notes"),
            newExpanded && getEPADef("auto_note_points", "Auto Points"),
            getEPADef("teleop_notes", "Teleop Notes"),
            newExpanded && getEPADef("teleop_note_points", "Teleop Points"),
          ].filter(Boolean),
        },
        {
          headerName: "Scoring Location",
          headerClass: "ag-text-center",
          children: [
            getEPADef("amp_notes", "Amp Notes"),
            getEPADef("speaker_notes", "All Speaker Notes"),
            getEPADef("amplified_notes", "Amplified Notes"),
          ].filter(Boolean),
        },
        {
          headerName: "Endgame",
          headerClass: "ag-text-center",
          children: [
            !newExpanded && getEPADef("endgame_points", "Endgame Points"),
            newExpanded && getEPADef("endgame_park_points", "Park Points"),
            newExpanded && getEPADef("endgame_on_stage_points", "On Stage Points"),
            newExpanded && getEPADef("endgame_harmony_points", "Harmony Points"),
            newExpanded && getEPADef("endgame_trap_points", "Trap Points"),
            newExpanded && getEPADef("endgame_spotlight_points", "Spotlight Points"),
          ].filter(Boolean),
        },
      ];
    }

    return [...sharedDefs, getEPADef("total_points", "Total")];
  };

  const [columnDefs, setColumnDefs] = useState<any>(getColumnDefs(year, expanded));

  useEffect(() => {
    setColumnDefs(getColumnDefs(year, expanded));
  }, [year, expanded]);

  return (
    <Table
      data={data || []}
      columnDefs={columnDefs}
      showLocationQuickFilter
      showProjectionsFilter={year === CURR_YEAR}
      showCompetingThisWeekFilter={year === CURR_YEAR}
      showDownloadCSV
      showExpand
      expanded={expanded}
      setExpanded={setExpanded}
    />
  );
}
