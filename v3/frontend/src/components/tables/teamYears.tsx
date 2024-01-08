import { useMemo, useState } from "react";

import { Select, Textarea } from "@mantine/core";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridReact } from "ag-grid-react";

import { usePreferences } from "../../contexts/preferencesContext";
import {
  COUNTRIES,
  COUNTRY_FLAGS,
  DISTRICT_FULL_NAMES,
  STATE_PROV_FULL_NAMES,
} from "../../utils/geography";
import { classnames, round } from "../../utils/utils";
import { EPACellRenderer } from "./template";

export default function TeamYearTable({ data }: { data: any }) {
  const { colorScheme, EPACellFormat, setEPACellFormat } = usePreferences();

  const [quickFilterText, setQuickFilterText] = useState("");

  const defaultColDef = useMemo(
    () => ({
      resizable: false,
      sortable: true,
      suppressMovable: true,
      suppressStickyLabel: true,
      suppressSpanHeaderHeight: true,
      filter: true,
      flex: 1,
      minWidth: 120,
      headerClass: "ag-text-center",
      cellStyle: {
        textAlign: "center",
      },
    }),
    [],
  );

  const countryFilter = COUNTRIES.map((country) => ({
    displayKey: country,
    displayName: country,
    predicate: (_: any, cellValue: string) => cellValue === country,
    numberOfInputs: 0,
  }));

  const districtFilter = Object.values(DISTRICT_FULL_NAMES).map((district) => ({
    displayKey: district,
    displayName: district,
    predicate: (_: any, cellValue: string) => cellValue === district,
    numberOfInputs: 0,
  }));

  const getWLT = (params: any) => {
    const record = params?.data?.record?.season;
    if (!record) {
      return { wins: 0, losses: 0, ties: 0 };
    }
    const wins = record?.wins || 0;
    const losses = record?.losses || 0;
    const ties = record?.ties || 0;
    return { wins, losses, ties };
  };

  const recordGetter = (params: any) => {
    const { wins, losses, ties } = getWLT(params);
    return `${wins}-${losses}-${ties}`;
  };

  const winRateGetter = (params: any) => {
    const { wins, losses, ties } = getWLT(params);
    const total = wins + losses + ties;
    if (total === 0) return 0;
    return (wins + ties / 2) / total;
  };

  const countryFormatter = (params: any) => {
    if (COUNTRY_FLAGS?.[params?.value]) {
      return COUNTRY_FLAGS[params?.value];
    }
    return params?.value;
  };

  const stateGetter = (params: any) => {
    const state = params?.data?.state;
    const fullState = STATE_PROV_FULL_NAMES?.[state];
    return fullState || state;
  };

  const districtGetter = (params: any) => {
    const district = params?.data?.district;
    const fullDistrict = DISTRICT_FULL_NAMES?.[district];
    return fullDistrict || district;
  };

  // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
  const [columnDefs, setColumnDefs] = useState<any>([
    {
      headerName: "Rank",
      colId: "rank",
      valueGetter: (params: any) => params.node.rowIndex + 1,
      minWidth: 80,
      maxWidth: 80,
      filter: false,
      sortable: false,
      pinned: "left",
    },
    {
      field: "team",
      headerName: "Number",
      maxWidth: 120,
      filterParams: {
        filterOptions: ["equals", "startsWith"],
        maxNumConditions: 1,
        debounceMs: 200,
      },
      pinned: "left",
    },
    {
      headerName: "Basic Info",
      headerClass: "ag-text-center !border-r-2 !border-gray-200",
      children: [
        {
          field: "name",
          headerName: "Name",
          minWidth: 200,
          filter: false,
          sortable: false,
        },
        {
          field: "country",
          headerName: "Country",
          minWidth: 150,
          valueFormatter: countryFormatter,
          columnGroupShow: "open",
          filterParams: {
            filterOptions: ["empty", ...countryFilter],
            maxNumConditions: 1,
          },
          sortable: false,
        },
        {
          field: "state",
          headerName: "State/Prov",
          minWidth: 150,
          valueGetter: stateGetter,
          columnGroupShow: "open",
          filterParams: {
            filterOptions: ["startsWith", "equals"],
            maxNumConditions: 1,
            debounceMs: 200,
          },
          sortable: false,
        },
        {
          field: "district",
          headerName: "District",
          minWidth: 150,
          valueGetter: districtGetter,
          columnGroupShow: "open",
          filterParams: {
            filterOptions: ["empty", ...districtFilter],
            maxNumConditions: 1,
          },
          sortable: false,
        },
      ],
    },
    {
      headerName: "Total EPA",
      headerClass: "ag-text-center !border-r-2 !border-gray-200",
      children: [
        { field: "epa.ranks.total.rank", headerName: "EPA Rank", sortingOrder: ["desc", null] },
        { field: "epa.unitless", headerName: "Unitless EPA", sortingOrder: ["desc", null] },
        {
          field: "epa.total_points.mean",
          headerName: "EPA",
          cellRenderer: EPACellRenderer,
          cellRendererParams: { epaKey: "total_points" },
          resizable: true,
          sortingOrder: ["desc", null],
          filterParams: {
            filterOptions: ["greaterThan", "lessThan", "inRange"],
            maxNumConditions: 1,
          },
          cellClass: "col-border",
        },
      ],
    },
    {
      headerName: "EPA Breakdown",
      headerClass: "ag-text-center !border-r-2 !border-gray-200",
      children: [
        {
          field: "epa.breakdown.auto_points.mean",
          headerName: "Auto",
          headerTooltip: "Auto EPA",
          minWidth: 100,
          cellRenderer: EPACellRenderer,
          cellRendererParams: { epaKey: "auto_points" },
          resizable: true,
          sortingOrder: ["desc", null],
          filterParams: {
            filterOptions: ["greaterThan", "lessThan", "inRange"],
            maxNumConditions: 1,
          },
        },
        {
          field: "epa.breakdown.teleop_points.mean",
          headerName: "Teleop",
          headerTooltip: "Teleop EPA",
          minWidth: 100,
          cellRenderer: EPACellRenderer,
          cellRendererParams: { epaKey: "teleop_points" },
          resizable: true,
          sortingOrder: ["desc", null],
          filterParams: {
            filterOptions: ["greaterThan", "lessThan", "inRange"],
            maxNumConditions: 1,
          },
        },
        {
          field: "epa.breakdown.endgame_points.mean",
          headerName: "Endgame",
          headerTooltip: "Endgame EPA",
          minWidth: 100,
          cellRenderer: EPACellRenderer,
          cellRendererParams: { epaKey: "endgame_points" },
          resizable: true,
          sortingOrder: ["desc", null],
          filterParams: {
            filterOptions: ["greaterThan", "lessThan", "inRange"],
            maxNumConditions: 1,
          },
        },
      ],
    },
    {
      headerName: "Match Stats",
      headerClass: "ag-text-center",
      children: [
        {
          colId: "record",
          headerName: "Record",
          minWidth: 100,
          valueGetter: recordGetter,
          // sort record by win rate column
          // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
          comparator: (_a: any, _b: any, nodeA: any, nodeB: any, _c: any) => {
            const winRateA = winRateGetter(nodeA);
            const winRateB = winRateGetter(nodeB);
            return winRateA - winRateB;
          },
        },
        {
          field: "record.season.count",
          headerName: "Matches",
          minWidth: 100,
          columnGroupShow: "open",
        },
        { field: "record.season.wins", headerName: "Wins", minWidth: 100, columnGroupShow: "open" },
        {
          field: "record.season.losses",
          headerName: "Losses",
          minWidth: 100,
          columnGroupShow: "open",
        },
        { field: "record.season.ties", headerName: "Ties", minWidth: 100, columnGroupShow: "open" },
        {
          colId: "win_rate",
          headerName: "Win Rate",
          filter: "agNumberColumnFilter",
          valueGetter: winRateGetter,
          valueFormatter: (params: any) => `${round((params?.value ?? 0) * 100, 1)}%`,
          columnGroupShow: "open",
        },
      ],
    },
  ]);

  return (
    <div className="mt-4 h-full w-full">
      <div className="flex flex-row items-center justify-between">
        <Textarea
          value={quickFilterText}
          onChange={(e) => setQuickFilterText(e.target.value)}
          placeholder="Search"
        />
        <Select
          data={[
            "Error Bars (shifted)",
            "Error Bars (centered)",
            "Highlight (with interval)",
            "Highlight (mean only)",
            "Plaintext",
          ]}
          value={EPACellFormat}
          onChange={setEPACellFormat}
          allowDeselect={false}
        />
      </div>
      <div
        className={classnames(
          "h-[568px] w-full",
          colorScheme === "light" ? "ag-theme-quartz" : "ag-theme-quartz-dark",
        )}
      >
        <AgGridReact
          rowData={data}
          defaultColDef={defaultColDef}
          columnDefs={columnDefs}
          quickFilterText={quickFilterText}
          pagination
          paginationPageSize={10}
          paginationPageSizeSelector={[10, 50, 100, 500, 1000, 5000]}
        />
      </div>
    </div>
  );
}
