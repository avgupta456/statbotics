import { PropsWithChildren, createContext, useContext, useEffect, useMemo, useState } from "react";

function colorLuminance(r: number, g: number, b: number) {
  return r * 0.299 + g * 0.587 + b * 0.114;
}

type TeamColors = Map<string, string | undefined>;

type IColorsContext = {
  isLoading: boolean;
  colors: TeamColors | undefined;
};

export const ColorsContext = createContext<IColorsContext>({
  isLoading: true,
  colors: undefined,
});

type Props = PropsWithChildren<{
  teams: string[];
}>;

type ColorData = {
  teams: Record<
    number,
    {
      teamNumber: string;
      colors: null | {
        primaryHex: string;
        secondaryHex: string;
        verified: boolean;
      };
    }
  >;
};

async function fetchColors(teams: string[]): Promise<TeamColors | undefined> {
  if (teams.length === 100) {
    return undefined;
  }

  const colorsUrl = new URL("https://frc-colors.com/api/v1/team");

  colorsUrl.search = new URLSearchParams(
    Array.from(teams).map((num) => ["team", num.toString()])
  ).toString();

  const request = fetch(colorsUrl.toString());

  let json: ColorData = { teams: {} };

  try {
    const response = await request;

    if (!response.ok) {
      throw new Error("Failed to fetch colors");
    }

    json = await response.json();
  } catch (error) {
    console.error("Error fetching colors:", error);
    return undefined;
  }

  return new Map(
    Object.values(json.teams).map(
      (teamColors) => [teamColors.teamNumber, teamColors.colors?.primaryHex ?? undefined] as const
    )
  );
}

export const ColorsProvider = ({ children, teams }: Props) => {
  const [colors, setColors] = useState<TeamColors | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (teams.length === 0) {
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    fetchColors(teams).then((newColors) => {
      const filteredColors: TeamColors = new Map();

      for (const [team, color] of Array.from(newColors)) {
        if (!color) {
          filteredColors.set(team, undefined);
          continue;
        }

        const r = parseInt(color.slice(1, 3), 16);
        const g = parseInt(color.slice(3, 5), 16);
        const b = parseInt(color.slice(5, 7), 16);

        const luminance = colorLuminance(r, g, b);

        if (luminance > 0.9 * 255) {
          continue;
        }

        filteredColors.set(team, color);
      }

      setColors(filteredColors);
      setIsLoading(false);
    });
  }, [teams]);

  const value = useMemo(() => ({ isLoading, colors }), [isLoading, colors]);

  return <ColorsContext.Provider value={value}>{children}</ColorsContext.Provider>;
};

type GetColor = (team: string) => string;

export function useColors(defaultColor: string, showColors = true): GetColor {
  const { colors } = useContext(ColorsContext);

  const getColor = useMemo(() => {
    if (showColors) {
      return (team: string) => colors?.get(team) ?? defaultColor;
    } else {
      return () => defaultColor;
    }
  }, [colors, defaultColor, showColors]);

  return getColor;
}
