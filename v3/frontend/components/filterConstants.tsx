import { CURR_WEEK } from "../constants";

// TODO: Get options directly from year's team list
export const countryOptions = [
  { value: "", label: "All" },
  { value: "USA", label: "USA" },
  { value: "Canada", label: "Canada" },
  { value: "Turkey", label: "Turkey" },
  { value: "Mexico", label: "Mexico" },
  { value: "Israel", label: "Israel" },
  { value: "Chinese Taipei", label: "Chinese Taipei" },
  { value: "China", label: "China" },
  { value: "Australia", label: "Australia" },
  { value: "Brazil", label: "Brazil" },
  { value: "India", label: "India" },
];

export const usaOptions = [
  { value: "", label: "All" },
  { value: "AL", label: "Alabama" },
  { value: "AK", label: "Alaska" },
  { value: "AZ", label: "Arizona" },
  { value: "AR", label: "Arkansas" },
  { value: "CA", label: "California" },
  { value: "CO", label: "Colorado" },
  { value: "CT", label: "Connecticut" },
  { value: "DE", label: "Delaware" },
  { value: "FL", label: "Florida" },
  { value: "GA", label: "Georgia" },
  { value: "HI", label: "Hawaii" },
  { value: "ID", label: "Idaho" },
  { value: "IL", label: "Illinois" },
  { value: "IN", label: "Indiana" },
  { value: "IA", label: "Iowa" },
  { value: "KS", label: "Kansas" },
  { value: "KY", label: "Kentucky" },
  { value: "LA", label: "Louisiana" },
  { value: "ME", label: "Maine" },
  { value: "MD", label: "Maryland" },
  { value: "MA", label: "Massachusetts" },
  { value: "MI", label: "Michigan" },
  { value: "MN", label: "Minnesota" },
  { value: "MS", label: "Mississippi" },
  { value: "MO", label: "Missouri" },
  { value: "MT", label: "Montana" },
  { value: "NE", label: "Nebraska" },
  { value: "NV", label: "Nevada" },
  { value: "NH", label: "New Hampshire" },
  { value: "NJ", label: "New Jersey" },
  { value: "NM", label: "New Mexico" },
  { value: "NY", label: "New York" },
  { value: "NC", label: "North Carolina" },
  { value: "ND", label: "North Dakota" },
  { value: "OH", label: "Ohio" },
  { value: "OK", label: "Oklahoma" },
  { value: "OR", label: "Oregon" },
  { value: "PA", label: "Pennsylvania" },
  { value: "RI", label: "Rhode Island" },
  { value: "SC", label: "South Carolina" },
  { value: "SD", label: "South Dakota" },
  { value: "TN", label: "Tennessee" },
  { value: "TX", label: "Texas" },
  { value: "UT", label: "Utah" },
  { value: "VT", label: "Vermont" },
  { value: "VA", label: "Virginia" },
  { value: "WA", label: "Washington" },
  { value: "WV", label: "West Virginia" },
  { value: "WI", label: "Wisconsin" },
  { value: "WY", label: "Wyoming" },
  { value: "DC", label: "DC" },
];

// TODO: Get options directly from year's team list
export const canadaOptions = [
  { value: "", label: "All" },
  { value: "AB", label: "Alberta" },
  { value: "BC", label: "British Columbia" },
  { value: "ON", label: "Ontario" },
  { value: "QC", label: "Québec" },
];

// TODO: Get options directly from year's team list
export const districtOptions = [
  { value: "", label: "All" },
  { value: "chs", label: "Chesapeake" },
  { value: "fim", label: "Michigan" },
  { value: "fin", label: "Indiana" },
  { value: "fit", label: "Texas" },
  { value: "fma", label: "Mid-Atlantic" },
  { value: "fnc", label: "North Carolina" },
  { value: "isr", label: "Israel" },
  { value: "ne", label: "New England" },
  { value: "ont", label: "Ontario" },
  { value: "pch", label: "Peachtree" },
  { value: "pnw", label: "Pacific NW" },
  { value: "regionals", label: "Regionals" },
];

export const yearOptions = [
  { value: "2023", label: "2023" },
  { value: "2022", label: "2022" },
  { value: "2020", label: "2020" },
  { value: "2019", label: "2019" },
  { value: "2018", label: "2018" },
  { value: "2017", label: "2017" },
  { value: "2016", label: "2016" },
  { value: "2015", label: "2015" },
  { value: "2014", label: "2014" },
  { value: "2013", label: "2013" },
  { value: "2012", label: "2012" },
  { value: "2011", label: "2011" },
  { value: "2010", label: "2010" },
  { value: "2009", label: "2009" },
  { value: "2008", label: "2008" },
  { value: "2007", label: "2007" },
  { value: "2006", label: "2006" },
  { value: "2005", label: "2005" },
  { value: "2004", label: "2004" },
  { value: "2003", label: "2003" },
  { value: "2002", label: "2002" },
];

export const weekOptions = [
  { value: "", label: "All" },
  // { value: 0, label: "Week 0" },
  { value: 1, label: "Week 1" },
  { value: 2, label: "Week 2" },
  { value: 3, label: "Week 3" },
  { value: 4, label: "Week 4" },
  { value: 5, label: "Week 5" },
  { value: 6, label: "Week 6" },
  { value: 7, label: "Week 7" },
  { value: 8, label: "Week 8" },
  // { value: 9, label: "Offseason" },
];

export const competingOptions = [
  { value: "", label: "All Weeks" },
  { value: CURR_WEEK, label: "This Week" },
];

export const offseasonOptions = [
  { value: "", label: "All" },
  { value: "season", label: "Season Only" },
  { value: "offseason", label: "Offseason Only" },
];

export const elimOptions = [
  { value: "", label: "All" },
  { value: "qual", label: "Qual Only" },
  { value: "elim", label: "Elim Only" },
];

export const filterMatchesOptions = [
  { value: 15, label: "15 Minutes" },
  { value: 30, label: "30 Minutes" },
  { value: 60, label: "1 Hour" },
  { value: 120, label: "2 Hours" },
  { value: "", label: "All Matches" },
];

export const sortMatchesOptions = [
  { value: "predicted_time", label: "Sort by Time" },
  { value: "max_epa", label: "Max EPA" },
  { value: "sum_epa", label: "Sum EPA" },
  { value: "diff_epa", label: "Diff EPA" },
];
