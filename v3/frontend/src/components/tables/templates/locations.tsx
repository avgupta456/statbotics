import { Select } from "@mantine/core";

import {
  COUNTRIES,
  COUNTRY_FLAGS,
  DISTRICT_FULL_NAMES,
  STATE_PROV_FULL_NAMES,
} from "../../../utils/geography";

const countryFilter = COUNTRIES.map((country) => ({
  displayKey: country,
  displayName: country,
  predicate: (_: any, cellValue: string) => cellValue === country,
  numberOfInputs: 0,
}));

const districtFilter = Object.values(DISTRICT_FULL_NAMES).map((district) => ({
  displayKey: district,
  displayName: district,
  predicate: (_: any, cellValue: string) => cellValue === district,
  numberOfInputs: 0,
}));

export const countryFormatter = (params: any) => {
  if (COUNTRY_FLAGS?.[params?.value]) {
    return COUNTRY_FLAGS[params?.value];
  }
  return params?.value;
};

export const stateGetter = (params: any) => {
  const state = params?.data?.state;
  const fullState = STATE_PROV_FULL_NAMES?.[state];
  return fullState || state;
};

export const districtGetter = (params: any) => {
  const district = params?.data?.district;
  const fullDistrict = DISTRICT_FULL_NAMES?.[district];
  return fullDistrict || district;
};

export function LocationFilter({
  quickFilterText,
  setQuickFilterText,
}: {
  quickFilterText: string | null;
  // eslint-disable-next-line no-unused-vars
  setQuickFilterText: (value: string | null) => void;
}) {
  return (
    <Select
      data={[
        {
          group: "Countries",
          items: COUNTRIES.map((c) => ({ value: `country_${c}`, label: c })),
        },
        {
          group: "Districts",
          items: Object.values(DISTRICT_FULL_NAMES).map((d) => ({
            value: `district_${d}`,
            label: d,
          })),
        },
        {
          group: "States/Provinces",
          items: Object.values(STATE_PROV_FULL_NAMES).map((s) => ({
            value: `state_${s}`,
            label: s,
          })),
        },
      ]}
      value={quickFilterText}
      onChange={setQuickFilterText}
      placeholder="Search locations"
      clearable
      searchable
    />
  );
}

// COLUMN DEFS

export const countryDef = {
  field: "country",
  headerName: "Country",
  minWidth: 150,
  valueFormatter: countryFormatter,
  filterParams: {
    filterOptions: ["empty", ...countryFilter],
    maxNumConditions: 1,
  },
  sortable: false,
  getQuickFilterText: (params: any) => `country_${params?.value}`,
};

export const stateDef = {
  field: "state",
  headerName: "State/Prov",
  minWidth: 150,
  valueGetter: stateGetter,
  filterParams: {
    filterOptions: ["startsWith", "equals"],
    maxNumConditions: 1,
    debounceMs: 200,
  },
  sortable: false,
  getQuickFilterText: (params: any) => `state_${params?.value}`,
};

export const districtDef = {
  field: "district",
  headerName: "District",
  minWidth: 150,
  valueGetter: districtGetter,
  filterParams: {
    filterOptions: ["empty", ...districtFilter],
    maxNumConditions: 1,
  },
  sortable: false,
  getQuickFilterText: (params: any) => `district_${params?.value}`,
};
