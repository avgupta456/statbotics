import { useMemo, useState } from "react";

import type { AppProps } from "next/app";

import { AppShell, MantineProvider, createTheme } from "@mantine/core";
import "@mantine/core/styles.css";
import "@mantine/spotlight/styles.css";

import { AppContext } from "../contexts/appContext";
import Header from "../layout/header";
import "../styles/globals.css";
import { EventData, TeamYearData } from "../types";
import { CURR_YEAR } from "../utils/constants";

const theme = createTheme({
  fontFamily: "Roboto, sans-serif",
  cursorType: "pointer",
});

export default function App({ Component, pageProps }: AppProps) {
  const [teamYearMiniDataDict, setTeamYearMiniDataDict] = useState<{ [key: number]: TeamYearData }>(
    {},
  );
  const [teamYearDataDict, setTeamYearDataDict] = useState<{ [key: number]: TeamYearData }>({});
  const [eventDataDict, setEventDataDict] = useState<{ [key: number]: EventData }>({});
  const [yearDataDict, setyearDataDict] = useState<{ [key: number]: EventData }>({});
  const [year, setYear] = useState(CURR_YEAR);

  const memoizedValue = useMemo(
    () => ({
      teamYearMiniDataDict,
      setTeamYearMiniDataDict,
      teamYearDataDict,
      setTeamYearDataDict,
      eventDataDict,
      setEventDataDict,
      yearDataDict,
      setyearDataDict,
      year,
      setYear,
    }),
    [
      teamYearMiniDataDict,
      setTeamYearMiniDataDict,
      teamYearDataDict,
      setTeamYearDataDict,
      eventDataDict,
      setEventDataDict,
      yearDataDict,
      setyearDataDict,
      year,
      setYear,
    ],
  );

  return (
    <MantineProvider theme={theme} defaultColorScheme="light">
      <AppShell header={{ height: 60 }} padding={0} transitionDuration={0}>
        <AppContext.Provider value={memoizedValue}>
          <Header />
          <AppShell.Main>
            <Component {...pageProps} />
          </AppShell.Main>
        </AppContext.Provider>
      </AppShell>
    </MantineProvider>
  );
}
