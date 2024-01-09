import { createRef, useEffect, useMemo, useState } from "react";
import { BiShow } from "react-icons/bi";
import { MdCloudDownload } from "react-icons/md";

import { Select, Tooltip } from "@mantine/core";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridReact } from "ag-grid-react";

import { usePreferences } from "../../contexts/preferencesContext";
import { TeamYearData } from "../../types";
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

  const [quickFilterText, setQuickFilterText] = useState<string | null>(null);

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
          getQuickFilterText: (params: any) => `country_${params?.value}`,
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
          getQuickFilterText: (params: any) => `state_${params?.value}`,
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
          getQuickFilterText: (params: any) => `district_${params?.value}`,
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

  const EPAColumns = ["total_points", "auto_points", "teleop_points", "endgame_points"];
  const [EPAContext, setEPAContext] = useState({});

  const updateContext = (newData: TeamYearData[]) => {
    const newContext: any = {};
    EPAColumns.forEach((k) => {
      const means = newData.map((d) => d?.epa?.breakdown?.[k]?.mean || d?.epa?.[k]?.mean);
      const sds = newData.map((d) => d?.epa?.breakdown?.[k]?.sd || d?.epa?.[k]?.sd);
      const lowBounds = newData.map((d) => d?.epa?.conf?.[0]);
      const highBounds = newData.map((d) => d?.epa?.conf?.[1]);
      const maxValues = means.map((m, i) => m + highBounds[i] * sds[i]);
      const maxErrors = sds.map((s, i) => s * Math.max(highBounds[i], -lowBounds[i]));
      newContext[k] = {
        minValue: 0,
        maxValue: Math.max(...maxValues),
        maxError: Math.max(...maxErrors),
      };
    });
    setEPAContext(newContext);
  };

  useEffect(() => {
    if (data && data.length > 0) {
      updateContext(data);
    }
  }, [data]);

  const gridRef = createRef<any>();

  const exportCSV = () => {
    gridRef.current.api.exportDataAsCsv({ skipColumnGroupHeaders: true, allColumns: true });
  };

  return (
    <div className="mt-4 h-full w-full">
      <div className="mb-2 flex flex-row items-center justify-center gap-4">
        <Tooltip label="Clear filters">
          <div className="cursor-pointer">
            <BiShow
              className="h-6 w-6 text-gray-600"
              onClick={() => {
                setQuickFilterText(null);
                gridRef?.current?.api?.setFilterModel(null);
              }}
            />
          </div>
        </Tooltip>
        <Tooltip label="Download CSV">
          <div className="cursor-pointer">
            <MdCloudDownload className="h-6 w-6 text-gray-600" onClick={exportCSV} />
          </div>
        </Tooltip>
        <Select
          data={[
            {
              group: "Countries",
              items: COUNTRIES.map((c) => ({ value: `country_${c}`, label: c })),
            },
            {
              group: "Districts",
              items: Object.values(DISTRICT_FULL_NAMES).map((d) => ({
                value: `district_${d}`,
                label: d,
              })),
            },
            {
              group: "States/Provinces",
              items: Object.values(STATE_PROV_FULL_NAMES).map((s) => ({
                value: `state_${s}`,
                label: s,
              })),
            },
          ]}
          value={quickFilterText}
          onChange={setQuickFilterText}
          placeholder="Search locations"
          clearable
          searchable
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
          ref={gridRef}
          rowData={data}
          defaultColDef={defaultColDef}
          columnDefs={columnDefs}
          quickFilterText={quickFilterText ?? undefined}
          pagination
          paginationPageSize={10}
          paginationPageSizeSelector={[10, 50, 100, 500, 1000, 5000]}
          context={EPAContext}
        />
      </div>
    </div>
  );
}
