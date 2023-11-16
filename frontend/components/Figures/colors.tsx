import { PropsWithChildren, createContext, useContext, useEffect, useMemo, useState } from "react";

type TeamColors = Map<number, string | undefined>;

type IColorsContext = {
  isLoading: boolean;
  colors: TeamColors | undefined;
};

export const ColorsContext = createContext<IColorsContext>({
  isLoading: true,
  colors: undefined,
});

type Props = PropsWithChildren<{
  teams: number[];
}>;

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
  const uniqueTeams = new Set(
    // Convert offseason robots represented with really large numbers to their main team number
    // ex. team 1234B as 123400001
    teams.map((num) => num.toString().replace(/(\d+)0000\d+$/, "$1"))
  );

  if (uniqueTeams.size > 100) {
    return undefined;
  }

  const colorsUrl = new URL("https://frc-colors.com/api/v1/team");

  colorsUrl.search = new URLSearchParams(
    Array.from(uniqueTeams).map((num) => ["team", num.toString()])
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
    setIsLoading(true);
    fetchColors(teams).then((newColors) => {
      setColors(newColors);
      setIsLoading(false);
    });
  }, [teams]);

  const value = useMemo(() => ({ isLoading, colors }), [isLoading, colors]);

  return <ColorsContext.Provider value={value}>{children}</ColorsContext.Provider>;
};

type GetColor = (team: number) => string;

export function useColors(defaultColor: string, showColors = true): GetColor {
  const { colors } = useContext(ColorsContext);

  const getColor = useMemo(() => {
    if (showColors) {
      return (team: number) => colors?.get(team) ?? defaultColor;
    } else {
      return () => defaultColor;
    }
  }, [colors, defaultColor, showColors]);

  return getColor;
}
