import { useEffect, useState } from "react";

import { useData } from "../../contexts/dataContext";
import { getEPADef } from "./templates/epa";
import { getCountryDef, getDistrictDef, getStateDef } from "./templates/locations";
import { nameDef, rankDef, teamDef } from "./templates/misc";
import Table from "./templates/table";

export default function TeamYearsBreakdownTable({ data }: { data: any[] | undefined }) {
  const { year } = useData();
  const [expanded, setExpanded] = useState(false);

  const getColumnDefs = (newYear: number, newExpanded: boolean) => {
    if (newYear === 2023) {
      return [
        rankDef,
        teamDef,
        nameDef,
        getCountryDef(true),
        getStateDef(true),
        getDistrictDef(true),
        {
          headerName: "Total",
          headerClass: "ag-text-center",
          children: [
            getEPADef("total_points", "Total", false),
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

    return [
      rankDef,
      teamDef,
      nameDef,
      getCountryDef(true),
      getStateDef(true),
      getDistrictDef(true),
      getEPADef("total_points", "Total", false),
    ];
  };

  // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
  const [columnDefs, setColumnDefs] = useState<any>(getColumnDefs(year, false));

  useEffect(() => {
    setColumnDefs(getColumnDefs(year, expanded));
  }, [year, expanded]);

  const EPAColumns = [
    "total_points",
    "auto_points",
    "teleop_points",
    "endgame_points",
    "total_pieces",
    "links",
    "grid_points",
    "auto_pieces",
    "auto_grid_points",
    "teleop_pieces",
    "teleop_grid_points",
    "bottom_pieces",
    "middle_pieces",
    "top_pieces",
    "cubes_scored",
    "cube_points",
    "cones_scored",
    "cone_points",
    "auto_charge_station_points",
    "endgame_charge_station_points",
  ];

  return (
    <Table
      data={data || []}
      columnDefs={columnDefs}
      EPAColumns={EPAColumns}
      showLocationQuickFilter
      showProjectionsFilter
      showCompetingThisWeekFilter
      showDownloadCSV
      showExpand
      expanded={expanded}
      setExpanded={setExpanded}
    />
  );
}
