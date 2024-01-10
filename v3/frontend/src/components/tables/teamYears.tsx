import { useEffect, useState } from "react";

import { EPATotalRankDef, UnitlessEPADef, getEPADef } from "./templates/epa";
import { countryDef, districtDef, stateDef } from "./templates/locations";
import { nameDef, nextEventDef, nextEventWeekDef, rankDef, teamDef } from "./templates/misc";
import { recordDef, winRateDef } from "./templates/record";
import Table from "./templates/table";

export default function TeamYearTable({ data }: { data: any }) {
  const [expanded, setExpanded] = useState(false);

  const unexpandedColumnDefs = [
    rankDef,
    teamDef,
    nameDef,
    EPATotalRankDef,
    getEPADef("total_points", "Total", "Total EPA", false),
    recordDef,
    nextEventDef,
  ];

  const expandedColumnDefs = [
    rankDef,
    teamDef,
    nameDef,
    countryDef,
    stateDef,
    districtDef,
    EPATotalRankDef,
    UnitlessEPADef,
    getEPADef("total_points", "Total", "Total EPA", false),
    getEPADef("auto_points", "Auto", "Auto EPA"),
    getEPADef("teleop_points", "Teleop", "Teleop EPA"),
    getEPADef("endgame_points", "Endgame", "Endgame EPA"),
    recordDef,
    winRateDef,
    nextEventDef,
    nextEventWeekDef,
  ];

  // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
  const [columnDefs, setColumnDefs] = useState<any>(unexpandedColumnDefs);

  useEffect(() => {
    setColumnDefs(expanded ? expandedColumnDefs : unexpandedColumnDefs);
  }, [expanded]);

  const EPAColumns = ["total_points", "auto_points", "teleop_points", "endgame_points"];

  return (
    <Table
      data={data}
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
