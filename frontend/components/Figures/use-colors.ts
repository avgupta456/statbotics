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

export function useColors(teams: number[]): Map<number, string | undefined> {
  /** Maps team num to hex color code */
  const [colors, setColors] = useState<Map<number, string | undefined>>(new Map());

  useEffect(() => {
    const fetchColors = async () => {
      const colorsUrl = new URL("https://frc-colors.com/api/v1/team");

      console.log(teams.map((num) => colors.has(num)));

      if (teams.length > 100) {
        setColors(new Map());
        return;
      }

      if (teams.every((num) => colors.has(num))) {
        return;
      }

      colorsUrl.search = new URLSearchParams(
        teams.map((num) => ["team", num.toString()])
      ).toString();

      let json: ColorData = { teams: {} };

      try {
        const response = await fetch(colorsUrl.toString());

        if (!response.ok) {
          throw new Error("Failed to fetch colors");
        }

        json = await response.json();
      } catch (error) {
        console.error("Error fetching colors:", error);
      }

      const newColors = new Map<number, string>();

      for (const teamColors of Object.values(json.teams)) {
        newColors.set(teamColors.teamNumber, teamColors.colors?.primaryHex ?? undefined);
      }

      setColors(newColors);
    };

    fetchColors();
  }, [teams]);

  return colors;
}
