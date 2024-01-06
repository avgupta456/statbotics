import { useEffect, useMemo, useState } from "react";
import { MdBubbleChart, MdInsights, MdOutlineTableChart } from "react-icons/md";

// import { useRouter } from "next/router";
import { Select, Tabs, Textarea, Tooltip, useMantineColorScheme } from "@mantine/core";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridReact } from "ag-grid-react";

import getTeamYearData from "../../api/teams";
import { useApp } from "../../contexts/appContext";
import TabPanel from "../../layout/tabs";
import { EPAPercentiles, TeamYearData, YearData } from "../../types";
import { CURR_YEAR, YEAR_OPTIONS } from "../../utils/constants";
import {
  COUNTRIES,
  COUNTRY_FLAGS,
  DISTRICT_FULL_NAMES,
  STATE_PROV_FULL_NAMES,
} from "../../utils/geography";
import { classnames, round } from "../../utils/utils";
import BubbleChart from "./bubble";

// TODO: Enable query params for year, country, state, district
// TODO: Add query param for active tab

function EPACellRenderer({ value, percentileKey }: { value: number; percentileKey: string }) {
  const { colorScheme } = useMantineColorScheme();
  const { yearDataDict, year } = useApp();
  const percentiles: EPAPercentiles = yearDataDict[year]?.percentiles?.[percentileKey] ?? {};

  // if value is undefined, return a dash, careful not to turn 0 into a dash
  if (value === undefined || value === null) {
    return <div className="flex h-full w-full items-center justify-center">-</div>;
  }

  let color = "text-gray-800";
  if (colorScheme === "light") {
    if (value > percentiles?.p99 ?? 1000) {
      color = "text-blue-800 bg-blue-200";
    } else if (value > percentiles?.p90 ?? 1000) {
      color = "text-green-800 bg-green-100";
    } else if (value > percentiles?.p75 ?? 1000) {
      color = "text-green-800 bg-green-50";
    } else if (value < percentiles?.p25 ?? -1000) {
      color = "text-red-700 bg-red-100";
    }
  } else {
    color = "text-gray-200";
    if (value > percentiles?.p99 ?? 1000) {
      color = "text-blue-200 bg-blue-800";
    } else if (value > percentiles?.p90 ?? 1000) {
      color = "text-green-100 bg-green-800";
    } else if (value > percentiles?.p75 ?? 1000) {
      color = "text-green-100 bg-green-600";
    } else if (value < percentiles?.p25 ?? -1000) {
      color = "text-red-100 bg-red-700";
    }
  }

  const lowerBound = round(value * 0.9, 1);
  const upperBound = round(value * 1.1, 1);

  return (
    <div className="flex h-full w-full items-center justify-center">
      <Tooltip
        label={`${round(lowerBound, 0)} - ${round(upperBound, 0)}`}
        classNames={{
          tooltip: "text-xs",
        }}
      >
        <div className={classnames(color, "flex h-7 w-12 items-center justify-center rounded-lg")}>
          {round(value, 0)}
          <p className="ml-1 text-xs">±{round(value * 0.1, 0)}</p>
        </div>
      </Tooltip>
    </div>
  );

  /*
  return (
    <div className="flex h-full w-full items-center justify-center">
      <Tooltip.Floating label={`${lowerBound} - ${upperBound}`}>
        <div className={classnames(color, "flex h-7 w-12 items-center justify-center rounded-lg")}>
          {round(value, 1)}
        </div>
      </Tooltip.Floating>
    </div>
  );
  */
}

export default function TeamsPage() {
  const { colorScheme } = useMantineColorScheme();
  // const router = useRouter();

  const {
    teamYearMiniDataDict,
    setTeamYearMiniDataDict,
    teamYearDataDict,
    setTeamYearDataDict,
    setyearDataDict,
    year,
    setYear,
  } = useApp();

  const [error, setError] = useState(false);
  const [loadingMini, setLoadingMini] = useState(false);
  const [loadingFull, setLoadingFull] = useState(false);

  const [quickFilterText, setQuickFilterText] = useState("");

  useEffect(() => {
    const getMiniDataForYear = async (yearNum: number) => {
      setLoadingMini(true);
      const data: any = await getTeamYearData(yearNum, 50);
      const teamYearsData: TeamYearData[] = data?.team_years;
      const yearData: YearData = data?.year;
      if (teamYearsData && yearData) {
        setTeamYearMiniDataDict((prev: any) => ({ ...prev, [yearNum]: teamYearsData }));
        setyearDataDict((prev: any) => ({ ...prev, [yearNum]: yearData }));
      } else {
        setError(true);
      }
      setLoadingMini(false);
    };

    const getDataForYear = async (yearNum: number) => {
      setLoadingFull(true);
      const data: any = await getTeamYearData(yearNum);
      const teamYearsData: TeamYearData[] = data?.team_years;
      const yearData: YearData = data?.year;
      if (teamYearsData && yearData) {
        setTeamYearDataDict((prev: any) => ({ ...prev, [yearNum]: teamYearsData }));
        setyearDataDict((prev: any) => ({ ...prev, [yearNum]: yearData }));
      } else {
        setError(true);
      }
      setLoadingFull(false);
    };

    if (!error && !teamYearMiniDataDict[year] && !loadingMini) {
      getMiniDataForYear(year);
    } else if (!error && !teamYearDataDict[year] && !loadingFull) {
      getDataForYear(year);
    }
  }, [
    teamYearMiniDataDict,
    setTeamYearMiniDataDict,
    teamYearDataDict,
    setTeamYearDataDict,
    year,
    error,
  ]);

  const data: TeamYearData[] | undefined = teamYearDataDict[year] || teamYearMiniDataDict[year];
  const loading = data?.length === 0;

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

  const recordGetter = (params: any) => {
    const wins = params?.data?.wins || 0;
    const losses = params?.data?.losses || 0;
    const ties = params?.data?.ties || 0;
    return `${wins}-${losses}-${ties}`;
  };

  const winRateGetter = (params: any) => {
    const wins = params?.data?.wins || 0;
    const losses = params?.data?.losses || 0;
    const ties = params?.data?.ties || 0;
    const total = wins + losses + ties;
    if (total === 0) {
      return 0;
    }
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

  const [columnDefs, setColumnDefs] = useState<any>([
    {
      headerName: "Rank",
      colId: "rank",
      valueGetter: (params: any) => params.node.rowIndex + 1,
      minWidth: 80,
      maxWidth: 80,
      filter: false,
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
        { field: "epa.ranks.total.rank", headerName: "EPA Rank" },
        { field: "epa.unitless", headerName: "Unitless EPA" },
        {
          field: "epa.total.mean",
          headerName: "EPA",
          cellRenderer: EPACellRenderer,
          cellRendererParams: { percentileKey: "total_points" },
        },
      ],
    },
    {
      headerName: "EPA Breakdown",
      headerClass: "ag-text-center !border-r-2 !border-gray-200",
      children: [
        {
          field: "auto_epa",
          headerName: "Auto",
          headerTooltip: "Auto EPA",
          minWidth: 100,
          cellRenderer: EPACellRenderer,
          cellRendererParams: { percentileKey: "auto_stats" },
        },
        {
          field: "teleop_epa",
          headerName: "Teleop",
          headerTooltip: "Teleop EPA",
          minWidth: 100,
          cellRenderer: EPACellRenderer,
          cellRendererParams: { percentileKey: "teleop_stats" },
        },
        {
          field: "endgame_epa",
          headerName: "Endgame",
          headerTooltip: "Endgame EPA",
          minWidth: 100,
          cellRenderer: EPACellRenderer,
          cellRendererParams: { percentileKey: "endgame_stats" },
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
          comparator: (
            valueA: number,
            valueB: number,
            nodeA: any,
            nodeB: any,
            // eslint-disable-next-line @typescript-eslint/no-unused-vars, no-unused-vars
            isDescending: boolean,
          ) => {
            const winRateA = winRateGetter(nodeA);
            const winRateB = winRateGetter(nodeB);
            return winRateA - winRateB;
          },
        },
        { field: "count", headerName: "Matches", minWidth: 100, columnGroupShow: "open" },
        { field: "wins", headerName: "Wins", minWidth: 100, columnGroupShow: "open" },
        { field: "losses", headerName: "Losses", minWidth: 100, columnGroupShow: "open" },
        { field: "ties", headerName: "Ties", minWidth: 100, columnGroupShow: "open" },
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
    <div className="p-4">
      <div className="flex w-full items-center justify-center">
        <Select
          data={YEAR_OPTIONS}
          value={year.toString()}
          onChange={(newYear: string | null) => (newYear ? setYear(parseInt(newYear)) : CURR_YEAR)}
          // withCheckIcon={false}
          checkIconPosition="right"
          allowDeselect={false}
          className="mr-4 w-24"
        />
        <div className="text-center text-3xl">Teams</div>
      </div>
      <Tabs
        variant="pills"
        classNames={{ list: "border-b pb-px border-gray-200" }}
        defaultValue="insights"
        // value={router.query.activeTab as string}
        // onChange={(value) => router.push(`/teams/${value}`)}
      >
        <Tabs.List>
          <Tabs.Tab value="insights" leftSection={<MdOutlineTableChart />}>
            Insights
          </Tabs.Tab>
          <Tabs.Tab value="bubble" leftSection={<MdBubbleChart />}>
            Bubble Chart
          </Tabs.Tab>
          <Tabs.Tab value="figures" leftSection={<MdInsights />}>
            Figures
          </Tabs.Tab>
        </Tabs.List>
        <TabPanel value="insights" error={error}>
          <div className="mt-4 h-full w-full">
            <div className="flex flex-row items-center justify-between">
              <Textarea
                value={quickFilterText}
                onChange={(e) => setQuickFilterText(e.target.value)}
                placeholder="Search"
              />
            </div>
            <div className="border-box h-full w-full">
              <div
                className={classnames(
                  // "h-auto w-full",
                  "h-[568px] w-full",
                  colorScheme === "light" ? "ag-theme-quartz" : "ag-theme-quartz-dark",
                )}
              >
                <AgGridReact
                  rowData={data}
                  defaultColDef={defaultColDef}
                  columnDefs={columnDefs}
                  quickFilterText={quickFilterText}
                  // domLayout="autoHeight"
                  pagination
                  paginationPageSize={10}
                  paginationPageSizeSelector={[10, 50, 100]}
                />
              </div>
            </div>
          </div>
        </TabPanel>
        <TabPanel value="bubble" loading={loading} error={error}>
          <div className="block h-[400px] w-[400px]">
            <BubbleChart width={400} height={400} />
          </div>
        </TabPanel>
        <TabPanel value="figures" loading={loading} error={error}>
          Figures
        </TabPanel>
      </Tabs>
    </div>
  );
}
