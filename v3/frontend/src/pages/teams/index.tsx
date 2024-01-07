import { useEffect, useMemo, useState } from "react";
import { MdBubbleChart, MdInsights, MdOutlineTableChart } from "react-icons/md";

// import { useRouter } from "next/router";
import { Select, Tabs, Textarea, Tooltip, useMantineColorScheme } from "@mantine/core";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridReact } from "ag-grid-react";

import getTeamYearData from "../../api/teams";
import { useData } from "../../contexts/dataContext";
import { usePreferences } from "../../contexts/preferencesContext";
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

function getColorSubTemplate(percentiles: EPAPercentiles, colorOptions: string[], value: number) {
  if (percentiles?.p99 && value > percentiles?.p99) {
    return colorOptions?.[0];
  }
  if (percentiles?.p90 && value > percentiles?.p90) {
    return colorOptions?.[1];
  }
  if (percentiles?.p75 && value > percentiles?.p75) {
    return colorOptions?.[2];
  }
  if (percentiles?.p25 && value < percentiles?.p25) {
    return colorOptions?.[4];
  }
  return colorOptions?.[3];
}

function getColorTemplate(
  colorScheme: string,
  percentiles: EPAPercentiles,
  colorOptions: string[],
  value: number,
) {
  if (colorScheme === "light") {
    return getColorSubTemplate(percentiles, colorOptions, value);
  }
  return getColorSubTemplate(percentiles, colorOptions.slice(5), value);
}

function EPACellRenderer({ data, epaKey, value }: { data: any; epaKey: string; value: number }) {
  if (value === undefined || value === null) {
    return <div className="flex h-full w-full items-center justify-center">-</div>;
  }

  const { colorScheme } = useMantineColorScheme();
  const { EPACellFormat } = usePreferences();
  const { yearDataDict, year } = useData();

  const mean = value;
  const sd = data?.epa?.breakdown?.[epaKey]?.sd || data?.epa?.[epaKey]?.sd || 0;
  const [rawLower, rawUpper] = data?.epa?.conf ?? [0, 0];
  const lower = mean + rawLower * sd;
  const upper = mean + rawUpper * sd;
  const adjSd = (upper - lower) / 2;

  const percentiles: EPAPercentiles = yearDataDict[year]?.percentiles?.[epaKey] ?? {};

  if (EPACellFormat === "Plaintext") {
    return <div>{round(value, 1)}</div>;
  }

  const color = getColorTemplate(
    colorScheme,
    percentiles,
    [
      "bg-blue-200 text-blue-800", // light p99
      "bg-green-200 text-green-800", // light p90
      "bg-green-100 text-green-800", // light p75
      "", // light middle
      "bg-red-200 text-red-700", // light p25
      "bg-blue-500 text-white", // dark p99
      "bg-green-600 text-white", // dark p90
      "bg-green-300 text-green-800", // dark p75
      "", // dark middle
      "bg-red-400 text-white", // dark p25
    ],
    value,
  );

  if (EPACellFormat === "Highlight (mean only)") {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <div className={classnames(color, "flex h-7 w-12 items-center justify-center rounded-lg")}>
          {round(value, 1)}
        </div>
      </div>
    );
  }

  if (EPACellFormat === "Highlight (with interval)") {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <Tooltip
          label={`${round(lower, 1)} - ${round(upper, 1)}`}
          classNames={{
            tooltip: "text-xs",
          }}
        >
          <div
            className={classnames(color, "flex h-7 w-12 items-center justify-center rounded-lg")}
          >
            {round(value, 0)}
            <p className="ml-1 text-xs">±{round(adjSd, 0)}</p>
          </div>
        </Tooltip>
      </div>
    );
  }

  const borderColor = getColorTemplate(
    colorScheme,
    percentiles,
    [
      "border border-blue-500",
      "border border-green-500",
      "border border-green-500",
      "border border-gray-500",
      "border border-red-500",
      "border border-blue-500",
      "border border-green-800",
      "border border-green-800",
      "border border-gray-500",
      "border border-red-500",
    ],
    value,
  );

  const shifted = EPACellFormat === "Error Bars (shifted)";

  const minValue = 0;
  const maxValue = 1.5 * (percentiles?.p99 ?? 100);
  const valueRange = maxValue - minValue;
  const midValue = minValue + valueRange / 2;

  // TODO: Fix size math (percents messed up right now)
  return (
    <div
      className="relative flex h-full w-full items-center justify-center"
      style={{
        marginLeft: shifted ? `${(100 * (value - midValue)) / valueRange}%` : "",
      }}
    >
      <div
        className={classnames(
          "absolute right-1/2 top-1/2 mr-[12px] h-[1.5px] transform",
          borderColor,
        )}
        style={{
          width: `calc(${(100 * (value - lower)) / valueRange}% - 6px)`,
        }}
      />
      <Tooltip
        label={`${round(lower, 1)} - ${round(upper, 1)}`}
        classNames={{
          tooltip: "text-xs",
        }}
      >
        <div
          className={classnames(
            "flex h-6 w-6 items-center justify-center rounded-full",
            color,
            borderColor,
          )}
        >
          {round(value, 0)}
        </div>
      </Tooltip>
      <div
        className={classnames(
          "absolute left-1/2 top-1/2 ml-[12px] h-[1.5px] transform",
          borderColor,
        )}
        style={{
          width: `calc(${(100 * (upper - value)) / valueRange}% - 6px)`,
        }}
      />
    </div>
  );
}

export default function TeamsPage() {
  const { colorScheme } = useMantineColorScheme();
  const { EPACellFormat, setEPACellFormat } = usePreferences();
  // const router = useRouter();

  const {
    teamYearMiniDataDict,
    setTeamYearMiniDataDict,
    teamYearDataDict,
    setTeamYearDataDict,
    setyearDataDict,
    year,
    setYear,
  } = useData();

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

  let data: TeamYearData[] | undefined = teamYearDataDict[year] || teamYearMiniDataDict[year];
  if (data) {
    data = data.sort(
      (a, b) => (a?.epa?.ranks?.total?.rank ?? 0) - (b?.epa?.ranks?.total?.rank ?? 0),
    );
  }
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
        classNames={{
          list: classnames(
            "border-b pb-px",
            colorScheme === "light" ? "border-gray-200" : "border-gray-600",
          ),
        }}
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
                  paginationPageSizeSelector={[10, 50, 100, 500, 1000, 5000]}
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
