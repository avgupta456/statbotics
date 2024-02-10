import { MdRefresh } from "react-icons/md";

import { Tooltip } from "@mantine/core";

import FilterBar, { LocationFilter } from "../../components/filterBar";
import { Select } from "../../components/select";
import { useLocation } from "../../contexts/locationContext";
import {
  elimOptions,
  matchSortOptions,
  timeRangeOptions,
  weekOptions,
} from "../../utils/filterOptions";

export default function MatchesFilterBar({
  week = undefined,
  setWeek = undefined,
  elim,
  setElim,
  timeRange = undefined,
  setTimeRange = undefined,
  sort = undefined,
  setSort = undefined,
  incrementRefresh = undefined,
}: {
  week?: number | null;
  // eslint-disable-next-line no-unused-vars
  setWeek?: (value: number | null) => void;
  elim: string | null;
  // eslint-disable-next-line no-unused-vars
  setElim: (value: string | null) => void;
  timeRange?: string | null;
  // eslint-disable-next-line no-unused-vars
  setTimeRange?: (value: string | null) => void;
  sort?: string;
  // eslint-disable-next-line no-unused-vars
  setSort?: (value: string) => void;
  incrementRefresh?: () => void;
}) {
  const { setLocation } = useLocation();
  return (
    <FilterBar
      className="flex w-full flex-row flex-wrap justify-center gap-2 px-4"
      onClearFilters={() => {
        if (setWeek) setWeek(null);
        setLocation(null);
        setElim(null);
        if (setTimeRange) setTimeRange(null);
        if (setSort) setSort("time");
      }}
    >
      {setWeek && (
        <Select
          className="w-32"
          value={week?.toString() ?? null}
          onChange={(value) => (value ? setWeek(parseInt(value)) : setWeek(null))}
          data={weekOptions}
          placeholder="All Weeks"
          allowDeselect={false}
          clearable
        />
      )}
      <LocationFilter />
      <Select
        className="w-32"
        value={elim?.toString() ?? null}
        onChange={setElim}
        data={elimOptions}
        placeholder="Comp Level"
        allowDeselect={false}
        clearable
      />
      {setTimeRange && (
        <Select
          className="w-32"
          value={timeRange ?? null}
          onChange={setTimeRange}
          data={timeRangeOptions}
          placeholder="Time Range"
          allowDeselect={false}
          clearable
        />
      )}
      {setSort && (
        <Select
          className="w-32"
          value={sort ?? "time"}
          onChange={(value) => setSort(value ?? "time")}
          data={matchSortOptions}
          allowDeselect={false}
        />
      )}
      {incrementRefresh && (
        <Tooltip label="Refresh">
          <div className="cursor-pointer">
            <MdRefresh className="my-1.5 h-6 w-6 text-zinc-600" onClick={incrementRefresh} />
          </div>
        </Tooltip>
      )}
    </FilterBar>
  );
}
