import { useEffect } from "react";

import { useRouter } from "next/router";

import { CURR_YEAR } from "../utils/constants";
import { parseCountry, parseDistrict, parseState } from "../utils/geography";

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
  query = {},
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
  query?: any;
}) {
  const router = useRouter();

  const { isReady } = router;

  const {
    country: paramsCountry,
    state: paramsState,
    district: paramsDistrict,
    year: paramsYear,
    week: paramsWeek,
  } = router.query;

  const paramsTab = window.location.hash.substring(1);

  useEffect(() => {
    if (isReady) {
      if (recordTab && tabOptions?.includes(paramsTab)) {
        setTab(paramsTab);
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

    const newHash = recordTab && tab !== defaultTab ? tab : undefined;

    const newQuery: any = { ...query };
    if (recordYear && year && year !== CURR_YEAR) {
      newQuery.year = year;
    }

    if (recordLocation && location) {
      const locationType = location.split("_")[0];
      const locationValue = location.split("_")[1];
      newQuery[locationType] = locationValue;
    }

    if (recordWeek && week) {
      newQuery.week = week;
    }

    const cleanQuery: any = Object.fromEntries(
      Object.entries(newQuery).filter(([, v]) => v !== undefined),
    );

    router.replace(
      {
        pathname: router.pathname,
        hash: newHash || "",
        query: cleanQuery,
      },
      undefined,
      { shallow: true },
    );
  }, [year, tab, location, week]);

  return null;
}