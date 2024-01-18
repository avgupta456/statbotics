import { useEffect, useMemo, useState } from "react";
import { MdBubbleChart, MdInsights, MdOutlineTableChart } from "react-icons/md";

import { useRouter } from "next/router";

import { Tabs } from "@mantine/core";

import { getTeamYearData } from "../../api/teams";
import { getAxisOptions } from "../../components/figures/axisOptions";
import Bubbles from "../../components/figures/bubbles";
import YearLineChart from "../../components/figures/yearLine";
import { Select } from "../../components/select";
import TeamYearsTable from "../../components/tables/teamYears";
import TeamYearsBreakdownTable from "../../components/tables/teamYearsBreakdown";
import { useData } from "../../contexts/dataContext";
import { LocationContext } from "../../contexts/locationContext";
import { usePreferences } from "../../contexts/preferencesContext";
import TabPanel from "../../layout/tabs";
import { TeamYearData } from "../../types";
import { APITeamYear, APIYear } from "../../types/api";
import { CURR_YEAR, YEAR_OPTIONS } from "../../utils/constants";
import { parseCountry, parseDistrict, parseState } from "../../utils/geography";
import { classnames } from "../../utils/utils";

export default function TeamsPage() {
  const { colorScheme } = usePreferences();
  const router = useRouter();

  const { isReady } = router;
  const {
    year: paramsYear,
    tab: paramsTab,
    country: paramsCountry,
    state: paramsState,
    district: paramsDistrict,
  } = router.query;

  const {
    teamYearMiniDataDict,
    setTeamYearMiniDataDict,
    teamYearDataDict,
    setTeamYearDataDict,
    setyearDataDict,
    year,
    setYear,
  } = useData();

  const [location, setLocation] = useState<string | null>(null);
  const [_tab, setTab] = useState<string>("insights");

  let tab = _tab;
  if (tab === "breakdown" && ![2023].includes(year)) {
    tab = "insights";
  }

  useEffect(() => {
    if (isReady) {
      const paramsYearInt = parseInt(paramsYear as string);
      if (paramsYearInt >= 2002 && paramsYearInt !== year) {
        setYear(paramsYearInt);
      }

      if (
        paramsTab &&
        typeof paramsTab === "string" &&
        ["insights", "breakdown", "bubble", "figures"].includes(paramsTab)
      ) {
        setTab(paramsTab as string);
      }

      // check if paramsCountry in COUNTRIES (case insensitive)
      const parsedCountry = parseCountry(paramsCountry);
      const parsedState = parseState(paramsState);
      const parsedDistrict = parseDistrict(paramsDistrict);
      if (parsedCountry) {
        setLocation(`country_${parsedCountry}`);
      } else if (parsedState) {
        setLocation(`state_${parsedState}`);
      } else if (parsedDistrict) {
        setLocation(`district_${parsedDistrict}`);
      }
    }
  }, [isReady]);

  useEffect(() => {
    if (!isReady) return;
    // set query params
    const query: any = {};
    if (year !== CURR_YEAR) {
      query.year = year;
    }
    if (tab !== "insights") {
      query.tab = tab;
    }
    if (location) {
      const [locationType, locationName] = location.split("_");
      if (locationType === "country") {
        query.country = locationName;
      } else if (locationType === "state") {
        query.state = locationName;
      } else if (locationType === "district") {
        query.district = locationName;
      }
    }
    router.push({ pathname: "/teams", query }, undefined, { shallow: true });
  }, [year, tab, location]);

  const memoizedLocation = useMemo(() => ({ location, setLocation }), [location, setLocation]);

  const [error, setError] = useState(false);
  const [loadingMini, setLoadingMini] = useState(false);
  const [loadingFull, setLoadingFull] = useState(false);

  useEffect(() => {
    const getMiniDataForYear = async (yearNum: number) => {
      setLoadingMini(true);
      const data: TeamYearData = await getTeamYearData(yearNum, 50);
      const teamYearsData: APITeamYear[] = data?.team_years;
      const yearData: APIYear = data?.year;
      if (teamYearsData && yearData) {
        setTeamYearMiniDataDict((prev: { [key: number]: APITeamYear[] }) => ({
          ...prev,
          [yearNum]: teamYearsData,
        }));
        setyearDataDict((prev: { [key: number]: APIYear }) => ({ ...prev, [yearNum]: yearData }));
      } else {
        setError(true);
      }
      setLoadingMini(false);
    };

    const getDataForYear = async (yearNum: number) => {
      setLoadingFull(true);
      const data: TeamYearData = await getTeamYearData(yearNum);
      const teamYearsData: APITeamYear[] = data?.team_years;
      const yearData: APIYear = data?.year;
      if (teamYearsData && yearData) {
        setTeamYearDataDict((prev: { [key: number]: APITeamYear[] }) => ({
          ...prev,
          [yearNum]: teamYearsData,
        }));
        setyearDataDict((prev: { [key: number]: APIYear }) => ({ ...prev, [yearNum]: yearData }));
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
  }, [
    teamYearMiniDataDict,
    setTeamYearMiniDataDict,
    teamYearDataDict,
    setTeamYearDataDict,
    year,
    error,
  ]);

  let data = teamYearDataDict[year] || teamYearMiniDataDict[year];
  if (data) {
    data = data.sort(
      (a, b) => (a?.epa?.ranks?.total?.rank ?? 0) - (b?.epa?.ranks?.total?.rank ?? 0),
    );
  }
  const loading = data?.length === 0;

  return (
    <div className="pt-4 md:p-2 lg:p-4">
      <div className="mb-2 flex w-full items-center justify-center">
        <Select
          data={YEAR_OPTIONS}
          value={year.toString()}
          onChange={(newYear: string | null) => (newYear ? setYear(parseInt(newYear)) : CURR_YEAR)}
          checkIconPosition="right"
          allowDeselect={false}
          className="mr-4 w-24"
        />
        <div className="text-center text-3xl">Teams</div>
      </div>
      <LocationContext.Provider value={memoizedLocation}>
        <Tabs
          variant="pills"
          classNames={{
            list: classnames(
              "border-b pb-px flex-nowrap overflow-x-scroll whitespace-nowrap",
              colorScheme === "light" ? "border-gray-200" : "border-gray-600",
            ),
          }}
          defaultValue="insights"
          value={tab}
          onChange={(newValue) => setTab(newValue ?? "insights")}
        >
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
          <TabPanel value="insights" error={error}>
            <div className="mt-4 h-full w-full">
              <TeamYearsTable data={data} />
            </div>
          </TabPanel>
          {year >= 2016 && (
            <TabPanel value="breakdown" loading={loading} error={error}>
              <div className="mt-4 h-full w-full">
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
            <div className="mt-4 flex h-auto w-full flex-col items-center justify-center px-2">
              <YearLineChart year={year} teamYears={data} />
            </div>
          </TabPanel>
        </Tabs>
      </LocationContext.Provider>
    </div>
  );
}
