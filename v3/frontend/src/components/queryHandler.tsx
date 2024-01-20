import { useEffect } from "react";

import { useRouter } from "next/router";

import { useData } from "../contexts/dataContext";
import { useLocation } from "../contexts/locationContext";
import { CURR_YEAR } from "../utils/constants";
import { parseCountry, parseDistrict, parseState } from "../utils/geography";

export default function QueryHandler({
  tab,
  setTab,
  defaultTab,
  tabOptions,
}: {
  tab: string;
  // eslint-disable-next-line no-unused-vars
  setTab: (newTab: string) => void;
  defaultTab: string;
  tabOptions: string[];
}) {
  const router = useRouter();

  const { isReady } = router;

  const {
    year: paramsYear,
    tab: paramsTab,
    country: paramsCountry,
    state: paramsState,
    district: paramsDistrict,
  } = router.query;

  const { year, setYear } = useData();
  const { location, setLocation } = useLocation();

  useEffect(() => {
    if (isReady) {
      const paramsYearInt = parseInt(paramsYear as string);
      if (paramsYearInt >= 2002 && paramsYearInt !== year) {
        setYear(paramsYearInt);
      }

      if (paramsTab && typeof paramsTab === "string" && tabOptions.includes(paramsTab)) {
        setTab(paramsTab as string);
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
    }
  }, [isReady]);

  useEffect(() => {
    if (!isReady) return;

    const query: any = {};
    if (year !== CURR_YEAR) {
      query.year = year;
    }
    if (tab !== defaultTab) {
      query.tab = tab;
    }
    if (location) {
      const [locationType, locationValue] = location.split("_");
      query[locationType] = locationValue;
    }

    router.push({
      pathname: router.pathname,
      query,
    });
  }, [year, tab, location]);

  return null;
}
