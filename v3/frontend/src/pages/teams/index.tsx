import { useEffect, useMemo, useState } from "react";
import { MdBubbleChart, MdInsights, MdOutlineTableChart } from "react-icons/md";

import { useRouter } from "next/router";

import { Tabs } from "@mantine/core";

import { getYearTeamYears } from "../../api/teams";
import { getAxisOptions } from "../../components/figures/axisOptions";
import Bubbles from "../../components/figures/bubbles";
import YearLineChart from "../../components/figures/yearLine";
import QueryHandler from "../../components/queryHandler";
import TeamYearsTable from "../../components/tables/teamYears";
import TeamYearsBreakdownTable from "../../components/tables/teamYearsBreakdown";
import { useData } from "../../contexts/dataContext";
import { LocationContext } from "../../contexts/locationContext";
import TabsLayout, { TabPanel } from "../../layout/tabs";
import { APITeamYear, APIYear } from "../../types/api";

export default function TeamsPage() {
  const { isReady } = useRouter();
  const {
    teamYearMiniDataDict,
    setTeamYearMiniDataDict,
    teamYearDataDict,
    setTeamYearDataDict,
    setYearDataDict,
    year,
    setYear,
  } = useData();

  const [location, setLocation] = useState<string | null>(null);
  const [_tab, setTab] = useState<string>("insights");

  let tab = _tab;
  if (tab === "breakdown" && ![2023].includes(year)) {
    tab = "insights";
  }

  const memoizedLocation = useMemo(() => ({ location, setLocation }), [location, setLocation]);

  const [error, setError] = useState(false);
  const [loadingMini, setLoadingMini] = useState(false);
  const [loadingFull, setLoadingFull] = useState(false);

  useEffect(() => {
    const getMiniDataForYear = async (yearNum: number) => {
      setLoadingMini(true);
      const {
        year: yearData,
        team_years: teamYearsData,
      }: {
        year: APIYear;
        team_years: APITeamYear[];
      } = await getYearTeamYears(yearNum, 50);
      if (teamYearsData && yearData) {
        setTeamYearMiniDataDict((prev: { [key: number]: APITeamYear[] }) => ({
          ...prev,
          [yearNum]: teamYearsData,
        }));
        setYearDataDict((prev: { [key: number]: APIYear }) => ({ ...prev, [yearNum]: yearData }));
      } else {
        setError(true);
      }
      setLoadingMini(false);
    };

    const getDataForYear = async (yearNum: number) => {
      setLoadingFull(true);
      const data = await getYearTeamYears(yearNum);
      const teamYearsData: APITeamYear[] = data?.team_years;
      const yearData: APIYear = data?.year;
      if (teamYearsData && yearData) {
        setTeamYearDataDict((prev: { [key: number]: APITeamYear[] }) => ({
          ...prev,
          [yearNum]: teamYearsData,
        }));
        setYearDataDict((prev: { [key: number]: APIYear }) => ({ ...prev, [yearNum]: yearData }));
      } else {
        setError(true);
      }
      setLoadingFull(false);
    };

    if (isReady && !error && !teamYearMiniDataDict[year] && !loadingMini) {
      getMiniDataForYear(year);
    } else if (isReady && !error && !teamYearDataDict[year] && !loadingFull) {
      getDataForYear(year);
    }
  }, [teamYearMiniDataDict, teamYearDataDict, year]);

  let data = teamYearDataDict[year] || teamYearMiniDataDict[year];
  if (data) {
    data = data.sort(
      (a, b) => (a?.epa?.ranks?.total?.rank ?? 0) - (b?.epa?.ranks?.total?.rank ?? 0),
    );
  }
  const loading = data?.length === 0;

  return (
    <LocationContext.Provider value={memoizedLocation}>
      <QueryHandler
        tab={tab}
        setTab={setTab}
        defaultTab="insights"
        tabOptions={["insights", "breakdown", "bubble", "figures"]}
        year={year}
        setYear={setYear}
        location={location}
        setLocation={setLocation}
      />
      <TabsLayout showYearSelector title="Teams" tab={tab} setTab={setTab} defaultTab="insights">
        <Tabs.List>
          <Tabs.Tab value="insights" leftSection={<MdOutlineTableChart />}>
            Insights
          </Tabs.Tab>
          {year >= 2016 && (
            <Tabs.Tab
              value="breakdown"
              leftSection={<MdOutlineTableChart />}
              disabled={![2023].includes(year)}
            >
              Breakdown
            </Tabs.Tab>
          )}
          <Tabs.Tab value="bubble" leftSection={<MdBubbleChart />}>
            Bubble Chart
          </Tabs.Tab>
          <Tabs.Tab value="figures" leftSection={<MdInsights />}>
            Figures
          </Tabs.Tab>
        </Tabs.List>
        <TabPanel value="insights" loading={loading} error={error}>
          <div className="h-full w-full">
            <TeamYearsTable data={data} />
          </div>
        </TabPanel>
        {year >= 2016 && (
          <TabPanel value="breakdown" loading={loading} error={error}>
            <div className="h-full w-full">
              <TeamYearsBreakdownTable data={data} />
            </div>
          </TabPanel>
        )}
        <TabPanel value="bubble" loading={loading} error={error}>
          <Bubbles
            data={data ?? []}
            axisOptions={getAxisOptions(year)}
            defaultAxes={{
              x: "teleop_points",
              y: "auto_points",
              z: "endgame_points",
            }}
          />
        </TabPanel>
        <TabPanel value="figures" loading={loading} error={error}>
          <div className="flex h-auto w-full flex-col items-center justify-center px-2">
            <YearLineChart year={year} teamYears={data} />
          </div>
        </TabPanel>
      </TabsLayout>
    </LocationContext.Provider>
  );
}
