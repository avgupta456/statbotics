import Link from "next/link";

export function TeamNameCellRenderer({ value, data }: { value: string; data: any }) {
  const { team, year } = data;
  const link = year ? `/teams/${team}/${year}` : `/teams/${team}`;

  return (
    <Link href={link} className="text-blue-500 underline">
      {value}
    </Link>
  );
}

export function NextEventCellRenderer({ value, data }: { value: string; data: any }) {
  const nextEventKey = data?.competing?.next_event_key;

  if (nextEventKey === null) {
    return <p>None</p>;
  }
  return (
    <Link href={`/event/${nextEventKey}`} className="text-blue-500 underline">
      {value}
    </Link>
  );
}

// COLUMN DEFS

export const rankDef = {
  headerName: "Rank",
  colId: "rank",
  valueGetter: (params: any) => params.node.rowIndex + 1,
  minWidth: 70,
  maxWidth: 70,
  sortable: false,
  pinned: "left",
};

export const teamDef = {
  field: "team",
  headerName: "Number",
  maxWidth: 115,
  // filterParams: {
  //   filterOptions: ["equals", "startsWith"],
  //   maxNumConditions: 1,
  //   debounceMs: 200,
  // },
  pinned: "left",
};

export const nameDef = {
  field: "name",
  headerName: "Name",
  minWidth: 200,
  sortable: false,
  // display link to Team page
  cellRenderer: TeamNameCellRenderer,
};

export const nextEventDef = {
  field: "competing.next_event_name",
  headerName: "Next Event",
  minWidth: 200,
  sortable: true,
  // display link to Event page
  cellRenderer: NextEventCellRenderer,
};

export const nextEventWeekDef = {
  field: "competing.next_event_week",
  headerName: "Next Week",
  minWidth: 120,
  maxWidth: 120,
  sortable: true,
};
