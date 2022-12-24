import React from "react";

import { Filters } from "@tanstack/react-table";

type Datum = { [key: string]: any };
type Filter = { [key: string]: any };

export const filterData = (data: Datum[], filter: Filter) => {
  let filteredData = data;
  Object.keys(filter).forEach((key) => {
    const value = filter[key];
    if (value) {
      filteredData = filteredData.filter((datum) => datum[key] === value);
    }
  });
  return filteredData;
};
