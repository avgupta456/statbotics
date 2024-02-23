import { ReactNode } from "react";
import { IoMdEye } from "react-icons/io";

import { Tooltip } from "@mantine/core";

import { useLocation } from "../contexts/locationContext";
import { APIEvent, APITeamEvent, APITeamYear } from "../types/api";
import { COUNTRY_FULL_NAMES, DISTRICT_FULL_NAMES, STATE_FULL_NAMES } from "../utils/geography";
import { Select } from "./select";

export function LocationFilter() {
  const { location, setLocation } = useLocation();

  return (
    <Select
      data={[
        {
          group: "Countries",
          items: Object.values(COUNTRY_FULL_NAMES).map((c) => ({
            value: `country_${c}`,
            label: c,
          })),
        },
        {
          group: "States/Provinces",
          items: Object.values(STATE_FULL_NAMES).map((s) => ({
            value: `state_${s}`,
            label: s,
          })),
        },
        {
          group: "Districts",
          items: Object.values(DISTRICT_FULL_NAMES).map((d) => ({
            value: `district_${d}`,
            label: d,
          })),
        },
      ]}
      value={location}
      onChange={setLocation}
      placeholder="Search locations"
      classNames={{ root: "w-40 md:w-48" }}
      clearable
      searchable
    />
  );
}

export const filterLocation = (
  location: string | null,
  item: APITeamYear | APITeamEvent | APIEvent,
) => {
  if (!location) return true;
  const [type, value] = location.split("_");
  if (type === "country" && item.country) {
    // unlike state and district, full name stored in DB
    return item.country === value;
  }
  if (type === "state" && item.state) {
    return STATE_FULL_NAMES[item.state] === value;
  }
  if (type === "district" && item.district) {
    return DISTRICT_FULL_NAMES[item.district] === value;
  }
  return false;
};

export default function FilterBar({
  onClearFilters = () => {},
  className = "flex items-center gap-3",
  children,
}: {
  onClearFilters?: () => void;
  className?: string;
  children: ReactNode;
}) {
  return (
    <div className={className}>
      <Tooltip label="Clear filters">
        <div className="cursor-pointer">
          <IoMdEye
            className="my-1.5 h-6 w-6 text-zinc-600"
            onClick={() => {
              onClearFilters();
            }}
          />
        </div>
      </Tooltip>
      {children}
    </div>
  );
}
