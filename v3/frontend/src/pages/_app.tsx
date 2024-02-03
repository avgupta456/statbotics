import { useEffect, useMemo, useState } from "react";

import type { AppProps } from "next/app";
import Head from "next/head";

import { AppShell, MantineProvider, createTheme, useMantineColorScheme } from "@mantine/core";
import "@mantine/core/styles.css";
import "@mantine/spotlight/styles.css";

import { get, set } from "idb-keyval";

import { DataContext } from "../contexts/dataContext";
import { PreferencesContext } from "../contexts/preferencesContext";
import Header from "../layout/header";
import "../styles/globals.css";
import { APIEvent, APITeamYear, APIYear } from "../types/api";
import { CURR_YEAR } from "../utils/constants";
import NoSSR from "../utils/no-ssr";

const theme = createTheme({
  fontFamily: "Roboto, sans-serif",
  cursorType: "pointer",
});

function App({ Component, pageProps }: AppProps) {
  const [teamYearMiniDataDict, setTeamYearMiniDataDict] = useState<{
    [key: number]: APITeamYear[];
  }>({});
  const [teamYearDataDict, setTeamYearDataDict] = useState<{ [key: number]: APITeamYear[] }>({});
  const [eventDataDict, setEventDataDict] = useState<{ [key: number]: APIEvent[] }>({});
  const [yearDataDict, setYearDataDict] = useState<{ [key: number]: APIYear }>({});
  const [year, setYear] = useState(CURR_YEAR);

  const memoizedDataValue = useMemo(
    () => ({
      teamYearMiniDataDict,
      setTeamYearMiniDataDict,
      teamYearDataDict,
      setTeamYearDataDict,
      eventDataDict,
      setEventDataDict,
      yearDataDict,
      setYearDataDict,
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
      setYearDataDict,
      year,
      setYear,
    ],
  );

  const { colorScheme, setColorScheme: _setColorScheme } = useMantineColorScheme();
  const [EPACellFormat, _setEPACellFormat] = useState("Highlight (with interval)");
  // Error Bars (shifted) --> mean-shifted with skew adjusted sd error bars
  // Error Bars (centered) --> skew adjusted sd error bars but no mean-shift
  // Highlight (with interval) --> percentile highlighted with p/m sd
  // Highlight (mean only) --> percentile highlighted without p/m sd
  // Plaintext --> just mean with no special formatting

  useEffect(() => {
    const loadPreferences = async () => {
      const preferences = await get("preferences");
      if (preferences?.colorScheme) {
        _setColorScheme(preferences?.colorScheme);
      }
      if (preferences?.EPACellFormat) {
        _setEPACellFormat(preferences?.EPACellFormat);
      }
    };

    loadPreferences();
  }, []);

  const setColorScheme = (newColorScheme: "light" | "dark") => {
    const newPreferences = { colorScheme: newColorScheme, EPACellFormat };
    set("preferences", newPreferences);
    _setColorScheme(newColorScheme);
  };

  const setEPACellFormat = (newEPACellFormat: string) => {
    const newPreferences = { colorScheme, EPACellFormat: newEPACellFormat };
    set("preferences", newPreferences);
    _setEPACellFormat(newEPACellFormat);
  };

  useEffect(() => {
    if (colorScheme === "dark") {
      document.body.classList.add("dark");
    } else {
      document.body.classList.remove("dark");
    }
  }, [colorScheme]);

  const memoizedPreferencesValue = useMemo(
    () => ({
      colorScheme,
      setColorScheme,
      EPACellFormat,
      setEPACellFormat,
    }),
    [colorScheme, setColorScheme, EPACellFormat, setEPACellFormat],
  );

  return (
    <PreferencesContext.Provider value={memoizedPreferencesValue}>
      <AppShell header={{ height: 60 }} padding={0} transitionDuration={0}>
        <DataContext.Provider value={memoizedDataValue}>
          <Header />
          <AppShell.Main>
            <Component {...pageProps} />
          </AppShell.Main>
        </DataContext.Provider>
      </AppShell>
    </PreferencesContext.Provider>
  );
}

export default function AppWrapper({ ...props }: AppProps) {
  return (
    <div>
      <Head>
        <title>Statbotics</title>
      </Head>
      <MantineProvider theme={theme}>
        <NoSSR>
          <App {...props} />
        </NoSSR>
      </MantineProvider>
    </div>
  );
}
