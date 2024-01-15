import { useLocation } from "../contexts/locationContext";
import { COUNTRIES, DISTRICT_FULL_NAMES, STATE_FULL_NAMES } from "../utils/geography";
import Select from "./select";

export default function LocationFilter() {
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
