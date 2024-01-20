import { ReactNode } from "react";
import { IoMdEye } from "react-icons/io";

import { Tooltip } from "@mantine/core";

import { useLocation } from "../contexts/locationContext";
import { COUNTRIES, DISTRICT_FULL_NAMES, STATE_FULL_NAMES } from "../utils/geography";
import { Select } from "./select";

export function LocationFilter() {
  const { location, setLocation } = useLocation();

  return (
    <Select
      data={[
        {
          group: "Countries",
          items: COUNTRIES.map((c) => ({ value: `country_${c}`, label: c })),
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

export default function FilterBar({
  onClearFilters = () => {},
  showLocationFilter,
  className = "flex items-center gap-4",
  children,
}: {
  onClearFilters?: () => void;
  showLocationFilter: boolean;
  className?: string;
  children: ReactNode;
}) {
  const { setLocation } = useLocation();

  return (
    <div className={className}>
      <Tooltip label="Clear filters">
        <div className="cursor-pointer">
          <IoMdEye
            className="my-1.5 h-6 w-6 text-gray-600"
            onClick={() => {
              if (showLocationFilter) {
                setLocation(null);
              }
              onClearFilters();
            }}
          />
        </div>
      </Tooltip>
      {showLocationFilter && <LocationFilter />}
      {children}
    </div>
  );
}
