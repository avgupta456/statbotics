import { useEffect } from "react";

import { useRouter } from "next/router";

import { CURR_YEAR } from "../utils/constants";
import {
  DISTRICT_FULL_NAMES,
  STATE_FULL_NAMES,
  parseCountry,
  parseDistrict,
  parseState,
} from "../utils/geography";

export default function QueryHandler({
  recordTab,
  tab = "",
  setTab = () => {},
  defaultTab = "",
  tabOptions = [],
  recordYear,
  year = CURR_YEAR,
  setYear = () => {},
  recordLocation,
  location = null,
  setLocation = () => {},
  recordWeek,
  week = null,
  setWeek = () => {},
}: {
  recordTab: boolean;
  tab?: string;
  // eslint-disable-next-line no-unused-vars
  setTab?: (newTab: string) => void;
  defaultTab?: string;
  tabOptions?: string[];
  recordYear: boolean;
  year?: number;
  // eslint-disable-next-line no-unused-vars
  setYear?: (newYear: number) => void;
  recordLocation: boolean;
  location?: string | null;
  // eslint-disable-next-line no-unused-vars
  setLocation?: (newLocation: string | null) => void;
  recordWeek: boolean;
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
      if (recordTab && typeof paramsTab === "string" && tabOptions?.includes(paramsTab)) {
        setTab(paramsTab as string);
      }

      if (recordYear && typeof paramsYear === "string") {
        const paramsYearInt = parseInt(paramsYear);
        if (paramsYearInt >= 2002 && paramsYearInt !== year) {
          setYear(paramsYearInt);
        }
      }

      if (recordLocation) {
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

      if (recordWeek && typeof paramsWeek === "string") {
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
    if (recordTab && tab && tab !== defaultTab) {
      query.tab = tab;
    } else {
      query.tab = undefined;
    }

    if (recordYear && year && year !== CURR_YEAR) {
      query.year = year;
    } else {
      query.year = undefined;
    }

    query.country = undefined;
    query.state = undefined;
    query.district = undefined;
    if (recordLocation && location) {
      const locationType = location.split("_")[0];
      let locationValue = location.split("_")[1];
      // check if in STATE_FULL_NAMES, DISTRICT_FULL_NAMES, if so, use abbreviation
      if (locationType === "state") {
        locationValue =
          Object.entries(STATE_FULL_NAMES).find(([, v]) => v === locationValue)?.[0] ??
          locationValue;
      } else if (locationType === "district") {
        locationValue =
          Object.entries(DISTRICT_FULL_NAMES).find(([, v]) => v === locationValue)?.[0] ??
          locationValue;
      }
      query[locationType] = locationValue;
    }

    if (recordWeek && week) {
      query.week = week;
    } else {
      query.week = undefined;
    }

    const cleanQuery: any = Object.fromEntries(
      Object.entries(query).filter(([, v]) => v !== undefined),
    );

    router.push({
      pathname: router.pathname,
      query: cleanQuery,
    });
  }, [year, tab, location, week]);

  return null;
}
