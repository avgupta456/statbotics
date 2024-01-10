import { useEffect, useState } from "react";

import { useData } from "../../contexts/dataContext";
import { EPATotalRankDef, getEPADef } from "./templates/epa";
import { getCountryDef, getDistrictDef, getStateDef } from "./templates/locations";
import { nameDef, rankDef, teamDef } from "./templates/misc";
import { recordDef } from "./templates/record";
import Table from "./templates/table";

export default function TeamYearsBreakdownTable({ data }: { data: any[] | undefined }) {
  const { year } = useData();
  const [expanded, setExpanded] = useState(false);

  // TODO: Debug game pieces, links columns
  // TODO: Add more columns
  // TODO: Disable 2016-2024 except 2023
  // TODO: Remove 2002-2015 from options
  const getUnexpandedColumnDefs = (newYear: number) => {
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
            getEPADef("total_points", "Total", "Total EPA", false),
            getEPADef("total_pieces", "Game Pieces", "Total Pieces"),
            getEPADef("links", "Links", "Links"),
          ],
        },
        newYear >= 2016 && getEPADef("auto_points", "Auto", "Auto EPA"),
        newYear >= 2016 && getEPADef("teleop_points", "Teleop", "Teleop EPA"),
        newYear >= 2016 && getEPADef("endgame_points", "Endgame", "Endgame EPA"),
        recordDef,
      ].filter(Boolean);
    }

    return [
      rankDef,
      teamDef,
      nameDef,
      getCountryDef(true),
      getStateDef(true),
      getDistrictDef(true),
      getEPADef("total_points", "Total", "Total EPA", false),
    ];
  };

  const getExpandedColumnDefs = (newYear: number) => {
    if (newYear === 2023) {
      [
        rankDef,
        teamDef,
        nameDef,
        getCountryDef(true),
        getStateDef(true),
        getDistrictDef(true),
        EPATotalRankDef,
        getEPADef("total_points", "Total", "Total EPA", false),
        newYear >= 2016 && getEPADef("auto_points", "Auto", "Auto EPA"),
        newYear >= 2016 && getEPADef("teleop_points", "Teleop", "Teleop EPA"),
        newYear >= 2016 && getEPADef("endgame_points", "Endgame", "Endgame EPA"),
      ].filter(Boolean);
    }

    return [
      rankDef,
      teamDef,
      nameDef,
      getCountryDef(true),
      getStateDef(true),
      getDistrictDef(true),
      getEPADef("total_points", "Total", "Total EPA", false),
    ];
  };

  // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
  const [columnDefs, setColumnDefs] = useState<any>(getUnexpandedColumnDefs(year));

  useEffect(() => {
    setColumnDefs(expanded ? getExpandedColumnDefs(year) : getUnexpandedColumnDefs(year));
  }, [year, expanded]);

  const EPAColumns = [
    "total_points",
    "total_pieces",
    "links",
    "auto_points",
    "teleop_points",
    "endgame_points",
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
