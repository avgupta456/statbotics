import { PropsWithChildren, createContext, useContext, useEffect, useMemo, useState } from "react";

import { usePreferences } from "./preferencesContext";

type TeamColors = Map<number, string | undefined>;

type ColorData = {
  teams: Record<
    number,
    {
      teamNumber: number;
      colors: null | {
        primaryHex: string;
        secondaryHex: string;
        verified: boolean;
      };
    }
  >;
};

async function fetchColors(teams: number[]): Promise<TeamColors | undefined> {
  if (teams.length === 0) {
    return undefined;
  }

  const uniqueTeams = new Set(
    // Convert offseason robots represented with really large numbers to their main team number
    // ex. team 1234B as 123400001
    teams.map((num) => num.toString().replace(/(\d+)0000\d+$/, "$1")),
  );

  const colorsUrl = new URL("https://api.frc-colors.com/v1/team");

  if (uniqueTeams.size > 500) {
    // Request all colors if above maximum allowed for one request
    colorsUrl.search = "?all";
  } else {
    colorsUrl.search = new URLSearchParams(
      Array.from(uniqueTeams).map((num) => ["team", num.toString()]),
    ).toString();
  }
  const request = fetch(colorsUrl.toString());

  let json: ColorData = { teams: {} };

  try {
    const response = await request;

    if (!response.ok) {
      throw new Error("Failed to fetch colors");
    }

    json = await response.json();
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error("Error fetching colors:", error);
    return undefined;
  }

  return new Map(
    Object.values(json.teams).map(
      (teamColors) => [teamColors.teamNumber, teamColors.colors?.primaryHex ?? undefined] as const,
    ),
  );
}

function relativeLuminance(hex: string): number {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);

  const sR = r / 255;
  const sG = g / 255;
  const sB = b / 255;

  const rL = sR <= 0.03928 ? sR / 12.92 : ((sR + 0.055) / 1.055) ** 2.4;
  const gL = sG <= 0.03928 ? sG / 12.92 : ((sG + 0.055) / 1.055) ** 2.4;
  const bL = sB <= 0.03928 ? sB / 12.92 : ((sB + 0.055) / 1.055) ** 2.4;

  return 0.2126 * rL + 0.7152 * gL + 0.0722 * bL;
}

function filterColors(colorScheme: string, colors?: TeamColors): TeamColors | undefined {
  if (!colors) {
    return undefined;
  }

  return new Map(
    Array.from(colors).filter(([, color]) => {
      if (!color) {
        return false;
      }

      const backgroundColor = colorScheme === "light" ? "#ffffff" : "#2e414d";
      const pointLuminance = relativeLuminance(color);
      const backgroundLuminance = relativeLuminance(backgroundColor);

      const l1 = Math.max(pointLuminance, backgroundLuminance);
      const l2 = Math.min(pointLuminance, backgroundLuminance);

      // Ranges from 1 to 21, higher is better
      const contrast = (l1 + 0.05) / (l2 + 0.05);

      return contrast > 1.3;
    }),
  );
}

type ContextValue = {
  // eslint-disable-next-line no-unused-vars
  setTeams: (teams: number[]) => void;
  colors: TeamColors | undefined;
};

export const ColorsContext = createContext<ContextValue>({
  colors: undefined,
  setTeams: () => {},
});

export function ColorsProvider({ children }: PropsWithChildren) {
  const [teams, setTeams] = useState<number[]>([]);
  const [colors, setColors] = useState<TeamColors | undefined>();
  const { colorScheme } = usePreferences();

  useEffect(() => {
    let canceled = false;

    fetchColors(teams).then((newColors) => {
      if (!canceled) {
        setColors(filterColors(colorScheme, newColors));
      }
    });

    return () => {
      canceled = true;
    };
  }, [useMemo(() => teams.join(","), [teams]), colorScheme]);

  const value = useMemo(
    () => ({
      colors,
      setTeams,
    }),
    [colors, setTeams],
  );

  return <ColorsContext.Provider value={value}>{children}</ColorsContext.Provider>;
}

// eslint-disable-next-line no-unused-vars
type GetColor = (team: number) => string;

export function useColors(teams: number[], enabled: boolean, defaultColor: string): GetColor {
  const context = useContext(ColorsContext);

  context.setTeams(teams);

  const getColor = (team: number): string =>
    enabled ? context.colors?.get(team) ?? defaultColor : defaultColor;

  return getColor;
}
