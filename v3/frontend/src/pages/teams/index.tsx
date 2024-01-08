import { useEffect, useState } from "react";
import { MdBubbleChart, MdInsights, MdOutlineTableChart } from "react-icons/md";

// import { useRouter } from "next/router";
import { Select, Tabs } from "@mantine/core";

import getTeamYearData from "../../api/teams";
import TeamYearTable from "../../components/tables/teamYears";
import { useData } from "../../contexts/dataContext";
import { usePreferences } from "../../contexts/preferencesContext";
import TabPanel from "../../layout/tabs";
import { TeamYearData, YearData } from "../../types";
import { CURR_YEAR, YEAR_OPTIONS } from "../../utils/constants";
import { classnames } from "../../utils/utils";

// TODO: Enable query params for year, country, state, district
// TODO: Add query param for active tab

export default function TeamsPage() {
  const { colorScheme } = usePreferences();
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
          <Tabs.Tab value="breakdown" leftSection={<MdOutlineTableChart />}>
            Breakdown
          </Tabs.Tab>
          <Tabs.Tab value="bubble" leftSection={<MdBubbleChart />}>
            Bubble Chart
          </Tabs.Tab>
          <Tabs.Tab value="figures" leftSection={<MdInsights />}>
            Figures
          </Tabs.Tab>
        </Tabs.List>
        <TabPanel value="insights" error={error}>
          <TeamYearTable data={data} />
        </TabPanel>
        <TabPanel value="breakdown" loading={loading} error={error}>
          Breakdown
        </TabPanel>
        <TabPanel value="bubble" loading={loading} error={error}>
          Bubble
        </TabPanel>
        <TabPanel value="figures" loading={loading} error={error}>
          Figures
        </TabPanel>
      </Tabs>
    </div>
  );
}
