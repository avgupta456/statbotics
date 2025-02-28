export const COUNTRY_FULL_NAMES: { [key: string]: string } = {
  USA: "USA",
  CAN: "Canada",
  TUR: "Türkiye",
  MEX: "Mexico",
  ISR: "Israel",
  BRA: "Brazil",
  AUS: "Australia",
  TWN: "Chinese Taipei",
  CHN: "China",
  JPN: "Japan",
  COL: "Colombia",
  IND: "India",
  POL: "Poland",
};

export const parseCountry = (country: undefined | string | string[], out: "key" | "value") => {
  if (!country) return null;
  if (Array.isArray(country)) return null;
  const countryUpper = country.toUpperCase();
  const countryMatch = Object.entries(COUNTRY_FULL_NAMES).find(
    ([k, v]) => k.toUpperCase() === countryUpper || v.toUpperCase() === countryUpper,
  );
  if (countryMatch) return out === "key" ? countryMatch[0] : countryMatch[1];
  return null;
};

export const STATE_FULL_NAMES: { [key: string]: string } = {
  AL: "Alabama",
  AK: "Alaska",
  // AS: "American Samoa",
  AZ: "Arizona",
  AR: "Arkansas",
  CA: "California",
  CO: "Colorado",
  CT: "Connecticut",
  DE: "Delaware",
  DC: "District Of Columbia",
  FL: "Florida",
  GA: "Georgia",
  // GU: "Guam",
  HI: "Hawaii",
  ID: "Idaho",
  IL: "Illinois",
  IN: "Indiana",
  IA: "Iowa",
  KS: "Kansas",
  KY: "Kentucky",
  LA: "Louisiana",
  ME: "Maine",
  MD: "Maryland",
  MA: "Massachusetts",
  MI: "Michigan",
  MN: "Minnesota",
  MS: "Mississippi",
  MO: "Missouri",
  MT: "Montana",
  NE: "Nebraska",
  NV: "Nevada",
  NH: "New Hampshire",
  NJ: "New Jersey",
  NM: "New Mexico",
  NY: "New York",
  NC: "North Carolina",
  ND: "North Dakota",
  // MP: "Northern Mariana Islands",
  OH: "Ohio",
  OK: "Oklahoma",
  OR: "Oregon",
  PA: "Pennsylvania",
  // PR: "Puerto Rico",
  RI: "Rhode Island",
  SC: "South Carolina",
  SD: "South Dakota",
  TN: "Tennessee",
  TX: "Texas",
  UT: "Utah",
  VT: "Vermont",
  // VI: "Virgin Islands",
  VA: "Virginia",
  WA: "Washington",
  WV: "West Virginia",
  WI: "Wisconsin",
  WY: "Wyoming",
  // Canada
  // NL: "Newfoundland",
  // PE: "Prince Edward Island",
  // NS: "Nova Scotia",
  // NB: "New Brunswick",
  QC: "Quebec",
  ON: "Ontario",
  // MB: "Manitoba",
  // SK: "Saskatchewan",
  AB: "Alberta",
  BC: "British Columbia",
  // YT: "Yukon",
  // NT: "Northwest Territories",
  // NU: "Nunavut",
};

export const parseState = (state: undefined | string | string[], out: "key" | "value") => {
  if (!state) return null;
  if (Array.isArray(state)) return null;
  const stateUpper = state.toUpperCase();
  const stateMatch = Object.entries(STATE_FULL_NAMES).find(
    ([k, v]) => k.toUpperCase() === stateUpper || v.toUpperCase() === stateUpper,
  );
  if (stateMatch) return out === "key" ? stateMatch[0] : stateMatch[1];
  return null;
};

export const DISTRICT_FULL_NAMES: { [key: string]: string } = {
  fim: "Michigan",
  fit: "Texas",
  ne: "New England",
  ont: "Ontario",
  fma: "Mid-Atlantic",
  pnw: "Pacific NW",
  chs: "Chesapeake",
  pch: "Peachtree",
  fnc: "North Carolina",
  fsc: "South Carolina",
  fin: "Indiana",
  isr: "Israel",
};

export const parseDistrict = (district: undefined | string | string[], out: "key" | "value") => {
  if (!district) return null;
  if (Array.isArray(district)) return null;
  const districtUpper = district.toUpperCase();
  const districtMatch = Object.entries(DISTRICT_FULL_NAMES).find(
    ([k, v]) => k.toUpperCase() === districtUpper || v.toUpperCase() === districtUpper,
  );
  if (districtMatch) return out === "key" ? districtMatch[0] : districtMatch[1];
  return null;
};
