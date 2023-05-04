import React, { useState } from "react";
import Select, { createFilter } from "react-select";
import WindowedSelect from "react-windowed-select";

import { multiSelectStyles } from "../../../components/multiSelect";
import { classnames } from "../../../utils";
import { compress } from "../../../utils";
import { TeamYearData } from "../types";

const Event = ({ data }: { data: TeamYearData }) => {
  const [selectedTeams, setSelectedTeams] = useState<any>([]);

  const addTeam = async (selected) => {
    if (selected.length > selectedTeams.length) {
      const team = selected[selected.length - 1].value;
    }
    setSelectedTeams(selected);
  };

  const teamOptions = data.team_years
    .sort((a, b) => a.num - b.num)
    .map((team) => ({
      value: team.num,
      label: `${team.num} | ${team.team}`,
    }));

  const TeamSelect = ({ className }) => (
    <WindowedSelect
      isMulti
      instanceId={"team-select"}
      className={classnames("flex-grow text-sm mr-2", className)}
      styles={multiSelectStyles((value) => {
        let index = 0;
        if (selectedTeams.length > 0) {
          index = selectedTeams.findIndex((team) => team?.value === value);
        }
        return index;
      })}
      options={teamOptions}
      onChange={addTeam}
      value={selectedTeams}
      filterOption={createFilter({ ignoreAccents: false })}
      windowThreshold={100}
    />
  );

  const teamNums = selectedTeams.map((team) => team.value);

  return (
    <div className="w-full mb-8">
      <div className="md:w-4/5 mx-auto flex flex-col mb-4">
        <p className="mb-2">
          <strong>Enter Teams</strong> (Min 6, Max 100)
        </p>
        <TeamSelect className="hidden md:inline-block" />
      </div>
      {compress(2023, teamNums, 0)}
    </div>
  );
};

export default Event;
