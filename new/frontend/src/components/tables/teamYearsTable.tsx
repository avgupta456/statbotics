import { useEffect, useState } from "react";

import { APITeamYear } from "../../types/api";
import { CURR_YEAR, RP_NAMES } from "../../utils/constants";
import { EPATotalRankDef, UnitlessEPADef, getEPADef } from "./templates/epa";
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
      EPATotalRankDef,
      getEPADef("total_points", "Total"),
      newYear >= 2016 && getEPADef("auto_points", "Auto"),
      newYear >= 2016 && getEPADef("teleop_points", "Teleop"),
      newYear >= 2016 && getEPADef("endgame_points", "Endgame"),
      newYear >= 2016 && newExpanded && getEPADef("rp_1", RP_NAMES[newYear][0]),
      newYear >= 2016 && newExpanded && getEPADef("rp_2", RP_NAMES[newYear][1]),
      newYear >= 2025 && newExpanded && getEPADef("rp_3", RP_NAMES[newYear][2]),
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
