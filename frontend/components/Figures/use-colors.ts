import { useEffect, useState } from "react";

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

const requestCache = new Map<string, Promise<Response>>();

async function fetchColors(
  teams: number[],
  colors: Map<number, string | undefined> = new Map()
): Promise<Map<number, string | undefined>> {
  if (teams.length > 100) {
    // Too many teams to fetch in a single request
    return new Map();
  }

  const colorsUrl = new URL("https://frc-colors.com/api/v1/team");

  if (teams.every((num) => colors.has(num))) {
    return colors;
  }

  colorsUrl.search = new URLSearchParams(teams.map((num) => ["team", num.toString()])).toString();

  let json: ColorData = { teams: {} };

  const cacheKey = teams.join(",");
  const request = requestCache.get(cacheKey) ?? fetch(colorsUrl.toString());
  requestCache.set(cacheKey, request);

  try {
    const response = await request;

    if (!response.ok) {
      throw new Error("Failed to fetch colors");
    }

    json = await response.json();
  } catch (error) {
    console.error("Error fetching colors:", error);
    return colors;
  }

  return new Map(
    Object.values(json.teams).map(
      (teamColors) => [teamColors.teamNumber, teamColors.colors?.primaryHex ?? undefined] as const
    )
  );
}

export function useColors(teams: number[]): Map<number, string | undefined> {
  /** Maps team num to hex color code */
  const [colors, setColors] = useState<Map<number, string | undefined>>(new Map());

  useEffect(() => {
    const teamsInColors = Array.from(colors.keys());
    // check if we already have all the colors (or if we have too many teams to fetch)
    if (teams.length > 100 || teams.every((num) => teamsInColors.includes(num))) {
      return;
    }

    fetchColors(teams, colors).then((newColors) => {
      setColors(newColors);
    });
  }, [colors, teams]);

  return colors;
}
