export const COUNTRIES: string[] = [
  "USA",
  "Canada",
  "Türkiye",
  "Mexico",
  "Israel",
  "Brazil",
  "Australia",
  "Chinese Taipei",
  "China",
  "Japan",
  "Colombia",
  "India",
  "Poland",
];

export const parseCountry = (country: undefined | string | string[]) => {
  if (!country) return null;
  if (Array.isArray(country)) return null;
  const countryUpper = country.toUpperCase();
  const countryMatch = COUNTRIES.find((c) => c.toUpperCase() === countryUpper);
  if (countryMatch) return countryMatch;
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

export const parseState = (state: undefined | string | string[]) => {
  if (!state) return null;
  if (Array.isArray(state)) return null;
  const stateUpper = state.toUpperCase();
  const stateMatch = Object.entries(STATE_FULL_NAMES).find(
    ([k, v]) => k.toUpperCase() === stateUpper || v.toUpperCase() === stateUpper,
  );
  if (stateMatch) return stateMatch[1];
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
  fin: "Indiana",
  isr: "Israel",
};

export const parseDistrict = (district: undefined | string | string[]) => {
  if (!district) return null;
  if (Array.isArray(district)) return null;
  const districtUpper = district.toUpperCase();
  const districtMatch = Object.entries(DISTRICT_FULL_NAMES).find(
    ([k, v]) => k.toUpperCase() === districtUpper || v.toUpperCase() === districtUpper,
  );
  if (districtMatch) return districtMatch[1];
  return null;
};