import { RP_KEYS, RP_NAMES } from "../../constants";
import { APITeamMatch, APITeamYear } from "../../types/api";

export type LineData = {
  id: string | number;
  data: { x: number; label: string; y: number }[];
};

export const getYAxisOptions = (year: number) => [
  {
    yearAccessor: (teamYear: APITeamYear) => teamYear?.epa?.breakdown?.total_points?.mean ?? 0,
    matchAccessor: (teamMatch: APITeamMatch) => teamMatch?.epa?.breakdown?.total_points ?? 0,
    value: "total_epa",
    label: "Total EPA",
  },
  ...(year >= 2016
    ? [
        {
          yearAccessor: (teamYear: APITeamYear) => teamYear?.epa?.breakdown?.auto_points?.mean ?? 0,
          matchAccessor: (teamMatch: APITeamMatch) => teamMatch?.epa?.breakdown?.auto_points ?? 0,
          value: "auto_epa",
          label: "Auto EPA",
        },
        {
          yearAccessor: (teamYear: APITeamYear) =>
            teamYear?.epa?.breakdown?.teleop_points?.mean ?? 0,
          matchAccessor: (teamMatch: APITeamMatch) => teamMatch?.epa?.breakdown?.teleop_points ?? 0,
          value: "teleop_epa",
          label: "Teleop EPA",
        },
        {
          yearAccessor: (teamYear: APITeamYear) =>
            teamYear?.epa?.breakdown?.endgame_points?.mean ?? 0,
          matchAccessor: (teamMatch: APITeamMatch) =>
            teamMatch?.epa?.breakdown?.endgame_points ?? 0,
          value: "endgame_epa",
          label: "Endgame EPA",
        },
        {
          yearAccessor: (teamYear: APITeamYear) =>
            teamYear?.epa?.breakdown?.[RP_KEYS[year][0]]?.mean ?? 0,
          matchAccessor: (teamMatch: APITeamMatch) =>
            teamMatch?.epa?.breakdown?.[RP_KEYS[year][0]] ?? 0,
          value: "rp_1_epa",
          label: `${RP_NAMES[year][0]} EPA`,
        },
        {
          yearAccessor: (teamYear: APITeamYear) =>
            teamYear?.epa?.breakdown?.[RP_KEYS[year][1]]?.mean ?? 0,
          matchAccessor: (teamMatch: APITeamMatch) =>
            teamMatch?.epa?.breakdown?.[RP_KEYS[year][1]] ?? 0,
          value: "rp_2_epa",
          label: `${RP_NAMES[year][1]} EPA`,
        },
      ]
    : []),
];
