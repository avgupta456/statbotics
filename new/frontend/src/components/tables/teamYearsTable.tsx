import { useEffect, useState } from "react";

import { APITeamYear } from "../../types/api";
import { CURR_YEAR } from "../../utils/constants";
import { EPATotalRankDef, UnitlessEPADef, getEPADef } from "./templates/epa";
import { getCountryDef, getDistrictDef, getStateDef } from "./templates/locations";
import { nextEventDef, nextEventWeekDef, rankDef, teamNameDef, teamNumDef } from "./templates/misc";
import { recordDef, winRateDef } from "./templates/record";
import Table from "./templates/table";

export default function TeamYearsTable({
  year,
  data,
}: {
  year: number;
  data: APITeamYear[] | undefined;
}) {
  const [expanded, setExpanded] = useState(false);

  const getColumnDefs = (newYear: number, newExpanded: boolean) =>
    [
      rankDef,
      teamNumDef,
      teamNameDef,
      getCountryDef(!newExpanded),
      getStateDef(!newExpanded),
      getDistrictDef(!newExpanded),
      EPATotalRankDef,
      getEPADef("total_points", "Total"),
      newYear >= 2016 && getEPADef("auto_points", "Auto"),
      newYear >= 2016 && getEPADef("teleop_points", "Teleop"),
      newYear >= 2016 && getEPADef("endgame_points", "Endgame"),
      newExpanded && UnitlessEPADef,
      recordDef,
      newExpanded && winRateDef,
      newYear === CURR_YEAR && nextEventDef,
      newExpanded && newYear === CURR_YEAR && nextEventWeekDef,
    ].filter(Boolean);

  const [columnDefs, setColumnDefs] = useState<any>(getColumnDefs(year, expanded));

  useEffect(() => {
    setColumnDefs(getColumnDefs(year, expanded));
  }, [year, expanded]);

  const EPAColumns = ["total_points", "auto_points", "teleop_points", "endgame_points"];

  return (
    <Table
      year={year}
      data={data || []}
      dataType="TeamYear"
      columnDefs={columnDefs}
      EPAColumns={EPAColumns}
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
