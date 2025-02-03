import { createRef, useEffect, useState } from "react";
import { MdAdd, MdCloudDownload, MdRemove } from "react-icons/md";

import { MultiSelect, Tooltip } from "@mantine/core";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridReact } from "ag-grid-react";

import { useLocation } from "../../../contexts/locationContext";
import { usePreferences } from "../../../contexts/preferencesContext";
import { classnames } from "../../../utils/utils";
import FilterBar, { LocationFilter } from "../../filterBar";

export default function Table({
  data,
  columnDefs,
  showLocationQuickFilter = false,
  showProjectionsFilter = false,
  showCompetingThisWeekFilter = false,
  showDownloadCSV = true,
  showExpand = false,
  expanded = false,
  setExpanded = () => {},
}: {
  data: any[];
  columnDefs: any[];
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

  const { colorScheme } = usePreferences();

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

  const defaultColDef = {
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
    cellClass: "",
  };

  const otherFilterOptions = [];
  if (showCompetingThisWeekFilter) {
    otherFilterOptions.push("Competing this week");
  }
  if (showProjectionsFilter) {
    otherFilterOptions.push("Played this season");
  }

  const mobile = window.innerWidth < 640;

  const [finalColumnDefs, setFinalColumnDefs] = useState<any[]>(columnDefs);

  useEffect(() => {
    const getMobileWidth = (headerName: string) => {
      if (headerName === "Name" || headerName === "Event Name") {
        return 200;
      }
      return 100;
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

  const hasHeaderGroup = finalColumnDefs.some((c) => c.children);

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
        <div className="flex items-center gap-3">
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
          hasHeaderGroup ? "h-[566px]" : "h-[519px]",
        )}
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
        />
      </div>
    </div>
  );
}
