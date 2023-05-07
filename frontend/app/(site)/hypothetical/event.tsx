import React, { useState } from "react";
import Select, { createFilter } from "react-select";
import WindowedSelect from "react-windowed-select";

import Link from "next/link";

import { classnames } from "../../../utils";
import { compress } from "../../../utils";
import { TeamYearData } from "../types";

const Event = ({ data }: { data: TeamYearData }) => {
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [seed, setSeed] = useState(0);

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
      options={teamOptions}
      onChange={addTeam}
      value={selectedTeams}
      filterOption={createFilter({ ignoreAccents: false })}
      windowThreshold={100}
    />
  );

  const teamNums = selectedTeams.map((team) => team.value);
  const numTeams = teamNums.length;

  const url = `statbotics.io/event/${compress(2023, teamNums, seed)}`;

  return (
    <div className="w-full mb-8">
      <div className="w-full lg:w-4/5 mx-auto flex align-start mb-16">
        <div className="flex-grow">
          <p className="mb-2">
            <strong>Teams</strong> (Min 6, Max 100)
          </p>
          <TeamSelect className="" />
        </div>
        <div className="w-40">
          <p className="w-full mb-2">
            <strong>Schedule Seed</strong>
          </p>
          <Select
            className="w-40 text-sm"
            options={[
              ...Array(100)
                .fill(0)
                .map((_, i) => i + 1),
            ].map((i) => ({ value: i, label: i }))}
            onChange={(e) => setSeed(e.value)}
          />
        </div>
      </div>
      {numTeams >= 6 && numTeams <= 100 && (
        <div className="w-full text-center">
          <p className="text-xl flex flex-col">
            Your Custom URL is{" "}
            <Link
              href={`https://www.${url}`}
              className="text_link"
              target="_blank"
              rel="noopener noreferrer"
            >
              {url}
            </Link>
          </p>
        </div>
      )}
    </div>
  );
};

export default Event;
