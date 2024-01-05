import { useMemo, useState } from "react";
import { MdBubbleChart, MdInsights, MdOutlineTableChart } from "react-icons/md";

import { useRouter } from "next/router";

import { Select, Tabs, useMantineColorScheme } from "@mantine/core";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { AgGridReact } from "ag-grid-react";

import { BACKEND_URL, CURR_YEAR } from "../../utils/constants";
import { getWithExpiry, setWithExpiry } from "../../utils/localStorage";
import { classnames, log, round } from "../../utils/utils";

const START_YEAR = 2002;
const END_YEAR = 2024;

// eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
async function getTeamYearData(year: number, limit?: number | null) {
  let urlSuffix = `/team_years/${year}`;
  let storageKey = `team_years_${year}`;
  if (limit) {
    urlSuffix += `?limit=${limit}&metric=epa_end`;
    storageKey += `_${limit}`;
  }

  const cacheData = getWithExpiry(storageKey);
  if (cacheData && cacheData?.team_years?.length > 0) {
    log(`Used Local Storage: ${storageKey}`);
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}${urlSuffix}`, { next: { revalidate: 60 } });
  log(`${urlSuffix} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = (await res.json())?.data;
  const expiry = year === CURR_YEAR ? 60 : 60 * 60; // 1 minute / 1 hour
  setWithExpiry(storageKey, data, expiry);
  return data;
}

export default function TeamsPage() {
  const { colorScheme } = useMantineColorScheme();
  const router = useRouter();

  // TODO: Enable query params for year, country, state, district

  const [year, setYear] = useState<number>(CURR_YEAR);

  const years = Array.from({ length: END_YEAR - START_YEAR + 1 }, (_, i) =>
    (END_YEAR - i).toString(),
  );

  const containerStyle = useMemo(() => ({ width: "100%", height: "100%" }), []);
  const gridStyle = useMemo(() => ({ height: "100%", width: "100%" }), []);

  const [rowData, setRowData] = useState([
    {
      athlete: "Michael Phelps",
      medals: {
        gold: 8,
        silver: 1,
        bronze: 0,
      },
    },
  ]);
  const [columnDefs, setColumnDefs] = useState([
    { field: "athlete" },
    // Using dot notation to access nested property
    { field: "medals.gold", headerName: "Gold" },
  ]);

  return (
    <div className="p-4">
      <div className="flex w-full items-center justify-center">
        <Select
          data={years}
          value={year.toString()}
          onChange={(newYear: string | null) => (newYear ? setYear(parseInt(newYear)) : END_YEAR)}
          // withCheckIcon={false}
          checkIconPosition="right"
          allowDeselect={false}
          className="mr-4 w-24"
        />
        <div className="text-center text-3xl">Teams</div>
      </div>
      <Tabs
        defaultValue="insights"
        value={router.query.activeTab as string}
        onChange={(value) => router.push(`/teams/${value}`)}
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
        <Tabs.Panel value="insights">
          <div className="mt-4 h-96 w-full">
            <div className="border-box h-full w-full">
              <div
                className={classnames(
                  "h-full w-full",
                  colorScheme === "light" ? "ag-theme-quartz" : "ag-theme-quartz-dark",
                )}
              >
                <AgGridReact rowData={rowData} columnDefs={columnDefs} />
              </div>
            </div>
          </div>
        </Tabs.Panel>
        <Tabs.Panel value="bubble">Bubble Chart</Tabs.Panel>
        <Tabs.Panel value="figures">Figures</Tabs.Panel>
      </Tabs>
    </div>
  );
}
