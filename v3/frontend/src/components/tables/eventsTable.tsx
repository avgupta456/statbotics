import { useEffect, useState } from "react";

import Link from "next/link";

import { APIEvent } from "../../types/api";
import { getCountryDef, getDistrictDef, getStateDef } from "./templates/locations";
import Table from "./templates/table";

function EventNameCellRenderer({ value, data }: { value: string; data: APIEvent }) {
  const { key } = data;
  const link = `/events/${key}`;

  return (
    <Link href={link} className="text-blue-500 underline">
      {value}
    </Link>
  );
}

function EventEPAFormatter({ value }: { value: number }) {
  return value ? value.toFixed(1) : "N/A";
}

const eventNameDef = {
  field: "name",
  headerName: "Event Name",
  minWidth: 300,
  sortable: false,
  // display link to Event page
  cellRenderer: EventNameCellRenderer,
};

const weekDef = {
  field: "week",
  headerName: "Week",
  minWidth: 80,
  sortable: true,
};

const eventStatusDef = {
  field: "status",
  headerName: "Status",
  minWidth: 120,
  sortable: false,
};

const eventNumTeamsDef = {
  field: "num_teams",
  headerName: "# Teams",
  minWidth: 120,
  sortable: true,
};

const maxEPADef = {
  field: "epa.max",
  headerName: "Max EPA",
  minWidth: 120,
  sortable: true,
  valueFormatter: EventEPAFormatter,
  sortingOrder: ["desc", null],
};

const top8EPADef = {
  field: "epa.top_8",
  headerName: "Top 8 EPA",
  minWidth: 120,
  sortable: true,
  valueFormatter: EventEPAFormatter,
  sortingOrder: ["desc", null],
};

const top24EPADef = {
  field: "epa.top_24",
  headerName: "Top 24 EPA",
  minWidth: 120,
  sortable: true,
  valueFormatter: EventEPAFormatter,
  sortingOrder: ["desc", null],
};

const meanEPADef = {
  field: "epa.mean",
  headerName: "Mean EPA",
  minWidth: 120,
  sortable: true,
  valueFormatter: EventEPAFormatter,
  sortingOrder: ["desc", null],
};

export default function EventsTable({ data }: { data: APIEvent[] }) {
  const [expanded, setExpanded] = useState(false);

  // eslint-disable-next-line @typescript-eslint/no-unused-vars, no-unused-vars
  const getColumnDefs = (newExpanded: boolean) => [
    eventNameDef,
    weekDef,
    eventStatusDef,
    eventNumTeamsDef,
    getCountryDef(!newExpanded),
    getStateDef(!newExpanded),
    getDistrictDef(!newExpanded),
    maxEPADef,
    top8EPADef,
    top24EPADef,
    meanEPADef,
  ];

  const [columnDefs, setColumnDefs] = useState<any>(getColumnDefs(expanded));

  useEffect(() => {
    setColumnDefs(getColumnDefs(expanded));
  }, [expanded]);

  return (
    <Table
      data={data || []}
      dataType="Event"
      columnDefs={columnDefs}
      offset={262}
      showLocationQuickFilter={false}
      showProjectionsFilter={false}
      showCompetingThisWeekFilter={false}
      showDownloadCSV
      showExpand
      expanded={expanded}
      setExpanded={setExpanded}
    />
  );
}
