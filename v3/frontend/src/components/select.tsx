import { useState } from "react";

import {
  MultiSelect as MantineMultiSelect,
  Select as MantineSelect,
  MultiSelectProps,
  SelectProps,
} from "@mantine/core";

export function Select({ value, searchable, ...props }: SelectProps) {
  const [searchValue, setSearchValue] = useState<string>("");

  return (
    <MantineSelect
      searchable={searchable}
      searchValue={searchValue}
      onSearchChange={setSearchValue}
      selectFirstOptionOnChange={value === null && searchValue !== ""}
      withCheckIcon={false}
      value={value}
      {...props}
    />
  );
}

export function MultiSelect({ value, searchable, ...props }: MultiSelectProps) {
  const [searchValue, setSearchValue] = useState<string>("");

  return (
    <MantineMultiSelect
      searchable={searchable}
      searchValue={searchValue}
      onSearchChange={setSearchValue}
      selectFirstOptionOnChange={searchValue !== ""}
      withCheckIcon
      value={value}
      {...props}
    />
  );
}
