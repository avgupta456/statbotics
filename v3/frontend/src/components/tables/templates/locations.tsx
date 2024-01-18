import { COUNTRY_FLAGS, DISTRICT_FULL_NAMES, STATE_FULL_NAMES } from "../../../utils/geography";

export const countryFormatter = (params: any) => {
  if (COUNTRY_FLAGS?.[params?.value]) {
    return COUNTRY_FLAGS[params?.value];
  }
  return params?.value;
};

export const stateGetter = (params: any) => {
  const state = params?.data?.state;
  const fullState = STATE_FULL_NAMES?.[state];
  return fullState || state;
};

export const districtGetter = (params: any) => {
  const district = params?.data?.district;
  const fullDistrict = DISTRICT_FULL_NAMES?.[district];
  return fullDistrict || district;
};

// COLUMN DEFS

export const getCountryDef = (hidden: boolean) => ({
  field: "country",
  headerName: "Country",
  minWidth: 150,
  valueFormatter: countryFormatter,
  // filterParams: {
  //   filterOptions: ["empty", ...countryFilter],
  //   maxNumConditions: 1,
  // },
  sortable: false,
  getQuickFilterText: (params: any) => `country_${params?.value}`,
  hide: hidden,
});

export const getStateDef = (hidden: boolean) => ({
  field: "state",
  headerName: "State/Prov",
  minWidth: 150,
  valueGetter: stateGetter,
  // filterParams: {
  //   filterOptions: ["startsWith", "equals"],
  //   maxNumConditions: 1,
  //   debounceMs: 200,
  // },
  sortable: false,
  getQuickFilterText: (params: any) => `state_${params?.value}`,
  hide: hidden,
});

export const getDistrictDef = (hidden: boolean) => ({
  field: "district",
  headerName: "District",
  minWidth: 150,
  valueGetter: districtGetter,
  // filterParams: {
  //   filterOptions: ["empty", ...districtFilter],
  //   maxNumConditions: 1,
  // },
  sortable: false,
  getQuickFilterText: (params: any) => `district_${params?.value}`,
  hide: hidden,
});
