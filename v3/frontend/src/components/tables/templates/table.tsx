import { createRef, useEffect, useMemo, useState } from "react";
import { IoMdEye } from "react-icons/io";
import { MdAdd, MdCloudDownload, MdRemove } from "react-icons/md";

import { MultiSelect, Select, Tooltip } from "@mantine/core";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridReact } from "ag-grid-react";

import { usePreferences } from "../../../contexts/preferencesContext";
import { TeamYearData } from "../../../types";
import { classnames } from "../../../utils/utils";
import { LocationFilter } from "./locations";

export default function Table({
  data,
  columnDefs,
  EPAColumns,
  showLocationQuickFilter,
  showProjectionsFilter,
  showCompetingThisWeekFilter,
  showDownloadCSV,
  showExpand,
  expanded = false,
  setExpanded = () => {},
}: {
  data: any[];
  columnDefs: any[];
  EPAColumns: string[];
  showLocationQuickFilter: boolean;
  showProjectionsFilter: boolean;
  showCompetingThisWeekFilter: boolean;
  showDownloadCSV: boolean;
  showExpand: boolean;
  expanded?: boolean;
  // eslint-disable-next-line no-unused-vars
  setExpanded?: (value: boolean) => void;
}) {
  const gridRef = createRef<any>();
  let cleanData = data;

  const { colorScheme, EPACellFormat, setEPACellFormat } = usePreferences();

  // Location Quick Filter

  const [quickFilterText, setQuickFilterText] = useState<string | null>(null);

  // Projection Filter, Competing This Week Filter

  const [multiSelectValue, setMultiSelectValue] = useState<string[]>([]);

  const hideProjections = multiSelectValue.includes("Played this season");

  if (hideProjections) {
    cleanData = cleanData.filter((d) => d?.record?.season?.count > 0);
  }

  const showCompetingThisWeek = multiSelectValue.includes("Competing this week");

  if (showCompetingThisWeek) {
    cleanData = cleanData.filter((d) => d?.competing?.this_week);
  }

  // Show Download CSV

  const exportCSV = () => {
    gridRef.current.api.exportDataAsCsv({ skipColumnGroupHeaders: true, allColumns: true });
  };

  // Show Expand

  // EPA Context

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

  const otherFilterOptions = [];
  if (showCompetingThisWeekFilter) {
    otherFilterOptions.push("Competing this week");
  }
  if (showProjectionsFilter) {
    otherFilterOptions.push("Played this season");
  }

  return (
    <div>
      <div className="mx-2 mb-2 flex flex-row">
        <div className="flex items-center gap-4">
          <Tooltip label="Clear filters">
            <div className="cursor-pointer">
              <IoMdEye
                className="h-6 w-6 text-gray-600"
                onClick={() => {
                  setQuickFilterText(null);
                  gridRef?.current?.api?.setFilterModel(null);
                }}
              />
            </div>
          </Tooltip>
          {showLocationQuickFilter && (
            <LocationFilter
              quickFilterText={quickFilterText}
              setQuickFilterText={setQuickFilterText}
            />
          )}
          {(showProjectionsFilter || showCompetingThisWeekFilter) && (
            <MultiSelect
              placeholder={multiSelectValue.length === 0 ? "Other filters" : ""}
              data={otherFilterOptions}
              value={multiSelectValue}
              onChange={setMultiSelectValue}
              classNames={{ root: "min-w-48 max-w-96" }}
            />
          )}
        </div>
        <div className="flex-grow" />
        <div className="flex items-center gap-4">
          {EPAColumns.length > 0 && (
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
          )}
          {showDownloadCSV && (
            <Tooltip label="Download CSV">
              <div className="cursor-pointer">
                <MdCloudDownload className="h-6 w-6 text-gray-600" onClick={exportCSV} />
              </div>
            </Tooltip>
          )}

          {showExpand && (
            <Tooltip label={expanded ? "Collapse" : "Expand"}>
              <div className="cursor-pointer">
                {expanded ? (
                  <MdRemove className="h-6 w-6 text-gray-600" onClick={() => setExpanded(false)} />
                ) : (
                  <MdAdd className="h-6 w-6 text-gray-600" onClick={() => setExpanded(true)} />
                )}
              </div>
            </Tooltip>
          )}
        </div>
      </div>
      <div
        className={classnames(
          "h-[516px] w-full",
          colorScheme === "light" ? "ag-theme-quartz" : "ag-theme-quartz-dark",
        )}
      >
        <AgGridReact
          ref={gridRef}
          rowData={cleanData}
          defaultColDef={defaultColDef}
          columnDefs={columnDefs}
          quickFilterText={quickFilterText ?? undefined}
          includeHiddenColumnsInQuickFilter
          pagination
          paginationPageSize={10}
          paginationPageSizeSelector={[10, 50, 100, 500, 1000, 5000]}
          context={EPAContext}
        />
      </div>
    </div>
  );
}
