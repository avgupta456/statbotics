import { useState } from "react";

import { Select as MantineSelect, SelectProps } from "@mantine/core";

export default function Select({ value, searchable, ...props }: SelectProps) {
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
