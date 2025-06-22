import {
  canadaOptions,
  competingOptions,
  countryOptions,
  districtOptions,
  usaOptions,
  yearOptions,
} from "./filterConstants";

export const validateFilters = (
  filters: { [key: string]: any },
  validFilters: string[],
  defaultFilters: string[]
) => {
  const outFilters: { [key: string]: any } = {};

  const keyToOptions = {
    year: yearOptions,
    is_competing: competingOptions,
  };

  // Note: week, playoff, filterMatches, sortMatches are not validated here

  for (const key of ["year", "is_competing"]) {
    if (validFilters.includes(key) && filters[key]) {
      outFilters[key] = keyToOptions[key].filter(
        (x) => x.value?.toLowerCase() === filters[key]?.toLowerCase()
      )?.[0]?.value;
    }
  }

  if (validFilters.includes("country") && filters["country"]) {
    outFilters["country"] = countryOptions.filter(
      (x) => x.value?.toLowerCase() === filters["country"]?.toLowerCase()
    )?.[0]?.value;
  }

  if (outFilters["country"] === "USA" || !outFilters["country"]) {
    if (validFilters.includes("state") && filters["state"]) {
      outFilters["state"] = usaOptions.filter(
        (x) => x.value?.toLowerCase() === filters["state"]?.toLowerCase()
      )?.[0]?.value;
    }
    if (outFilters["state"]) outFilters["country"] = "USA";
  }

  if (outFilters["country"] === "Canada" || !outFilters["country"]) {
    if (validFilters.includes("state") && filters["state"]) {
      outFilters["state"] = canadaOptions.filter(
        (x) => x.value?.toLowerCase() === filters["state"]?.toLowerCase()
      )?.[0]?.value;
    }
    if (outFilters["state"]) outFilters["country"] = "Canada";
  }

  if (!outFilters["country"] && !outFilters["state"]) {
    if (validFilters.includes("district") && filters["district"]) {
      outFilters["district"] = districtOptions.filter(
        (x) => x.value?.toLowerCase() === filters["district"]?.toLowerCase()
      )?.[0]?.value;
    }
  }

  for (const key of ["search", "refresh"]) {
    if (validFilters.includes(key) && filters[key]) {
      outFilters[key] = filters[key];
    }
  }

  validFilters.forEach((key, i) => {
    if (!outFilters[key]) {
      outFilters[key] = defaultFilters[i];
    }
  });

  return outFilters;
};

export const filterData = (data: any[] | undefined, filter: any) => {
  if (!data) {
    return [];
  }

  let filteredData = data;
  Object.keys(filter).forEach((key) => {
    const value = filter[key];
    if (key !== "search" && value !== "") {
      if (key === "is_competing") {
        filteredData = filteredData.filter((datum) => datum["competing"]["this_week"]);
      } else if (key === "district" && value === "regionals") {
        filteredData = filteredData.filter((datum) => datum["district"] === null);
      } else if (key === "country" && value === "Europe") {
        let countries = [
          "albania",
          "andorra",
          "austria",
          "belarus",
          "belgium",
          "bosnia-herzegovina",
          "bulgaria",
          "croatia",
          "cyprus",
          "czech republic",
          "denmark",
          "estonia",
          "finland",
          "france",
          "germany",
          "greece",
          "hungary",
          "iceland",
          "ireland",
          "italy",
          "kosovo",
          "latvia",
          "liechtenstein",
          "lithuania",
          "luxembourg",
          "malta",
          "moldova",
          "monaco",
          "montenegro",
          "netherlands",
          "macedonia",
          "norway",
          "poland",
          "portugal",
          "romania",
          "san marino",
          "serbia",
          "slovakia",
          "slovenia",
          "spain",
          "sweden",
          "switzerland",
          "ukraine",
          "united kingdom",
        ];
        filteredData = filteredData.filter((datum) =>
          countries.includes(datum["country"]?.toLowerCase())
        );
      } else {
        filteredData = filteredData.filter((datum) => datum[key] === value);
      }
    }
  });
  return filteredData;
};
