import { createRef, useEffect, useMemo, useState } from "react";
import { MdAdd, MdCloudDownload, MdRemove, MdSettings } from "react-icons/md";

import { MultiSelect, Popover, Tooltip } from "@mantine/core";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridReact } from "ag-grid-react";

import { useLocation } from "../../../contexts/locationContext";
import { usePreferences } from "../../../contexts/preferencesContext";
import { APITeamYear } from "../../../types/api";
import { classnames } from "../../../utils/utils";
import FilterBar, { LocationFilter } from "../../filterBar";
import { Select } from "../../select";

export default function Table({
  data,
  dataType,
  columnDefs,
  offset,
  EPAColumns = [],
  showLocationQuickFilter = false,
  showProjectionsFilter = false,
  showCompetingThisWeekFilter = false,
  showDownloadCSV = true,
  showExpand = false,
  expanded = false,
  setExpanded = () => {},
}: {
  data: any[];
  dataType: "TeamYear" | "Event";
  columnDefs: any[];
  offset: number;
  EPAColumns?: string[];
  showLocationQuickFilter?: boolean;
  showProjectionsFilter?: boolean;
  showCompetingThisWeekFilter?: boolean;
  showDownloadCSV?: boolean;
  showExpand?: boolean;
  expanded?: boolean;
  // eslint-disable-next-line no-unused-vars
  setExpanded?: (value: boolean) => void;
}) {
  const gridRef = createRef<any>();
  let cleanData = data;

  const { colorScheme, EPACellFormat, setEPACellFormat } = usePreferences();

  // Location Quick Filter

  const { location, setLocation } = useLocation();

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

  const updateTeamYearContext = (newData: APITeamYear[]) => {
    const newContext: any = {};
    EPAColumns.forEach((k) => {
      const means = newData.map((d) => d?.epa?.breakdown?.[k]?.mean);
      const sds = newData.map((d) => d?.epa?.breakdown?.[k]?.sd);
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
    if (data && data.length > 0 && dataType === "TeamYear") {
      updateTeamYearContext(data);
    }
  }, [data]);

  const defaultColDef = useMemo(
    () => ({
      resizable: false,
      sortable: true,
      suppressMovable: true,
      suppressStickyLabel: true,
      suppressSpanHeaderHeight: true,
      filter: false,
      flex: 1,
      minWidth: 120,
      headerClass: "ag-text-center",
      cellStyle: {
        textAlign: "center",
      },
      cellClass: EPACellFormat === "Error Bars (shifted)" ? "ag-col-border" : "",
    }),
    [EPACellFormat],
  );

  const otherFilterOptions = [];
  if (showCompetingThisWeekFilter) {
    otherFilterOptions.push("Competing this week");
  }
  if (showProjectionsFilter) {
    otherFilterOptions.push("Played this season");
  }

  const EPACellFormatOptions = [
    "Error Bars (shifted)",
    "Error Bars (centered)",
    "Highlight (with interval)",
    "Highlight (mean only)",
    "Plaintext",
  ];

  const mobile = window.innerWidth < 640;

  const [finalColumnDefs, setFinalColumnDefs] = useState<any[]>(columnDefs);

  useEffect(() => {
    const getMobileWidth = (headerName: string) => {
      if (headerName === "Name" || headerName === "Event Name") {
        return 200;
      }
      if (headerName === "Record") {
        return 100;
      }
      return 80;
    };

    setFinalColumnDefs(
      mobile
        ? columnDefs.map((c) => ({
            ...c,
            pinned: false,
            minWidth: getMobileWidth(c.headerName),
          }))
        : columnDefs,
    );
  }, [mobile, columnDefs]);

  const showMultiSelect = showProjectionsFilter || showCompetingThisWeekFilter;

  return (
    <div>
      <div className="mx-2 mb-2 flex flex-row">
        {(showLocationQuickFilter || showMultiSelect) && (
          <FilterBar
            onClearFilters={() => {
              if (location) {
                setLocation(null);
              }
              gridRef?.current?.api?.setFilterModel(null);
            }}
          >
            {showLocationQuickFilter && <LocationFilter />}
            {showMultiSelect && (
              <MultiSelect
                placeholder={multiSelectValue.length === 0 ? "Other filters" : ""}
                data={otherFilterOptions}
                value={multiSelectValue}
                onChange={setMultiSelectValue}
                classNames={{ root: "min-w-48 max-w-96 hidden lg:block" }}
              />
            )}
          </FilterBar>
        )}
        <div className="flex-grow" />
        <div className="flex items-center gap-4">
          {EPAColumns.length > 0 && (
            <>
              <div className="lg:hidden">
                <Popover width={220} position="bottom" shadow="md">
                  <Popover.Target>
                    <Tooltip label="Options">
                      <div className="cursor-pointer">
                        <MdSettings className="h-6 w-6 cursor-pointer text-zinc-600" />
                      </div>
                    </Tooltip>
                  </Popover.Target>
                  <Popover.Dropdown>
                    <Select
                      data={EPACellFormatOptions}
                      value={EPACellFormat}
                      onChange={setEPACellFormat}
                      allowDeselect={false}
                    />
                  </Popover.Dropdown>
                </Popover>
              </div>
              <Select
                data={EPACellFormatOptions}
                value={EPACellFormat}
                onChange={setEPACellFormat}
                allowDeselect={false}
                className="hidden lg:block"
              />
            </>
          )}
          {showDownloadCSV && (
            <div className="hidden xs:block">
              <Tooltip label="Download CSV">
                <div className="cursor-pointer">
                  <MdCloudDownload className="h-6 w-6 text-zinc-600" onClick={exportCSV} />
                </div>
              </Tooltip>
            </div>
          )}
          {showExpand && (
            <Tooltip label={expanded ? "Collapse" : "Expand"}>
              <div className="cursor-pointer">
                {expanded ? (
                  <MdRemove className="h-6 w-6 text-zinc-600" onClick={() => setExpanded(false)} />
                ) : (
                  <MdAdd className="h-6 w-6 text-zinc-600" onClick={() => setExpanded(true)} />
                )}
              </div>
            </Tooltip>
          )}
        </div>
      </div>
      <div
        className={classnames(
          "w-full",
          colorScheme === "light" ? "ag-theme-quartz" : "ag-theme-quartz-dark",
        )}
        style={{
          height: mobile ? `calc(100vh - ${offset}px)` : "519px",
        }}
      >
        <AgGridReact
          ref={gridRef}
          rowData={cleanData}
          defaultColDef={defaultColDef}
          columnDefs={finalColumnDefs}
          quickFilterText={location ?? undefined}
          includeHiddenColumnsInQuickFilter
          pagination={!mobile}
          paginationPageSize={10}
          paginationPageSizeSelector={[10, 50, 100, 500, 1000, 5000]}
          context={EPAContext}
        />
      </div>
    </div>
  );
}
