import { ReactNode } from "react";

import { Tabs } from "@mantine/core";

import { Select } from "../components/select";
import { useData } from "../contexts/dataContext";
import { usePreferences } from "../contexts/preferencesContext";
import { CURR_YEAR, YEAR_OPTIONS } from "../utils/constants";
import { classnames } from "../utils/utils";

export function TabPanel({
  value,
  children,
  loading = false,
  error = false,
  ...props
}: {
  value: string;
  children: any;
  loading?: boolean;
  error?: boolean;
  props?: any;
}) {
  // TODO: Add loading and error states

  if (loading) {
    return (
      <Tabs.Panel value={value} {...props}>
        <div>Loading...</div>
      </Tabs.Panel>
    );
  }

  if (error) {
    return (
      <Tabs.Panel value={value} {...props}>
        <div>Error</div>
      </Tabs.Panel>
    );
  }

  return (
    <Tabs.Panel value={value} {...props}>
      {children}
    </Tabs.Panel>
  );
}

export default function TabsLayout({
  showYearSelector = false,
  title,
  header,
  tab,
  setTab,
  defaultTab,
  children,
}: {
  showYearSelector?: boolean;
  title: string;
  header?: ReactNode;
  tab: string;
  // eslint-disable-next-line no-unused-vars
  setTab: (newTab: string) => void;
  defaultTab: string;
  children: ReactNode;
}) {
  const { colorScheme } = usePreferences();

  const { year, setYear } = useData();

  return (
    <div className="pt-4 md:p-2 lg:p-4">
      {showYearSelector && (
        <div className="mb-2 flex w-full items-center justify-center">
          <Select
            data={YEAR_OPTIONS}
            value={year.toString()}
            onChange={(newYear: string | null) =>
              newYear ? setYear(parseInt(newYear)) : CURR_YEAR
            }
            allowDeselect={false}
            className="mr-4 w-24"
          />
          <div className="text-center text-3xl">{title}</div>
        </div>
      )}
      {header}
      <Tabs
        variant="pills"
        classNames={{
          list: classnames(
            "border-b pb-px flex-nowrap overflow-x-scroll whitespace-nowrap",
            colorScheme === "light" ? "border-gray-200" : "border-gray-600",
          ),
        }}
        defaultValue={defaultTab}
        value={tab}
        onChange={(newValue) => setTab(newValue ?? defaultTab)}
      >
        {children}
      </Tabs>
    </div>
  );
}
