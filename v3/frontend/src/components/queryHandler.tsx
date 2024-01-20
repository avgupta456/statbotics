import { useEffect } from "react";

import { useRouter } from "next/router";

import { CURR_YEAR } from "../utils/constants";
import { parseCountry, parseDistrict, parseState } from "../utils/geography";

export default function QueryHandler({
  tab = "",
  setTab = () => {},
  defaultTab = "",
  tabOptions = [],
  year = CURR_YEAR,
  setYear = () => {},
  location = null,
  setLocation = () => {},
  week = null,
  setWeek = () => {},
}: {
  tab?: string;
  // eslint-disable-next-line no-unused-vars
  setTab?: (newTab: string) => void;
  defaultTab?: string;
  tabOptions?: string[];
  year?: number;
  // eslint-disable-next-line no-unused-vars
  setYear?: (newYear: number) => void;
  location?: string | null;
  // eslint-disable-next-line no-unused-vars
  setLocation?: (newLocation: string | null) => void;
  week?: number | null;
  // eslint-disable-next-line no-unused-vars
  setWeek?: (newWeek: number | null) => void;
}) {
  const router = useRouter();

  const { isReady } = router;

  const {
    tab: paramsTab,
    country: paramsCountry,
    state: paramsState,
    district: paramsDistrict,
    year: paramsYear,
    week: paramsWeek,
  } = router.query;

  useEffect(() => {
    if (isReady) {
      if (typeof paramsTab === "string" && tabOptions?.includes(paramsTab)) {
        setTab(paramsTab as string);
      }

      if (typeof paramsYear === "string") {
        const paramsYearInt = parseInt(paramsYear);
        if (paramsYearInt >= 2002 && paramsYearInt !== year) {
          setYear(paramsYearInt);
        }
      }

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

      if (typeof paramsWeek === "string") {
        const paramsWeekInt = parseInt(paramsWeek);
        if (paramsWeekInt !== week) {
          setWeek(paramsWeekInt);
        }
      }
    }
  }, [isReady]);

  useEffect(() => {
    if (!isReady) return;

    const query: any = {};
    if (tab && tab !== defaultTab) {
      query.tab = tab;
    }
    if (year && year !== CURR_YEAR) {
      query.year = year;
    }
    if (location) {
      const [locationType, locationValue] = location.split("_");
      query[locationType] = locationValue;
    }
    if (week) {
      query.week = week;
    }

    router.push({
      pathname: router.pathname,
      query,
    });
  }, [year, tab, location]);

  return null;
}
