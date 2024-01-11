import { useEffect, useState } from "react";

import { useData } from "../../contexts/dataContext";
import { CURR_YEAR } from "../../utils/constants";
import { EPATotalRankDef, UnitlessEPADef, getEPADef } from "./templates/epa";
import { getCountryDef, getDistrictDef, getStateDef } from "./templates/locations";
import { nameDef, nextEventDef, nextEventWeekDef, rankDef, teamDef } from "./templates/misc";
import { recordDef, winRateDef } from "./templates/record";
import Table from "./templates/table";

export default function TeamYearsTable({ data }: { data: any[] | undefined }) {
  const { year } = useData();
  const [expanded, setExpanded] = useState(false);

  const getColumnDefs = (newYear: number, newExpanded: boolean) =>
    [
      rankDef,
      teamDef,
      nameDef,
      getCountryDef(true),
      getStateDef(true),
      getDistrictDef(true),
      EPATotalRankDef,
      getEPADef("total_points", "Total", false),
      newYear >= 2016 && getEPADef("auto_points", "Auto"),
      newYear >= 2016 && getEPADef("teleop_points", "Teleop"),
      newYear >= 2016 && getEPADef("endgame_points", "Endgame"),
      newExpanded && UnitlessEPADef,
      recordDef,
      newExpanded && winRateDef,
      newYear === CURR_YEAR && nextEventDef,
      newExpanded && newYear === CURR_YEAR && nextEventWeekDef,
    ].filter(Boolean);

  // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
  const [columnDefs, setColumnDefs] = useState<any>(getColumnDefs(year, false));

  useEffect(() => {
    setColumnDefs(getColumnDefs(year, expanded));
  }, [year, expanded]);

  const EPAColumns = ["total_points", "auto_points", "teleop_points", "endgame_points"];

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
