import React, { useEffect, useState } from "react";
import { MdContentCopy } from "react-icons/md";
import Select, { createFilter } from "react-select";
import WindowedSelect from "react-windowed-select";

import Link from "next/link";

import { classnames, decompress } from "../../../utils";
import { compress } from "../../../utils";
import { TeamYearData } from "../types";

const Event = ({ data }: { data: TeamYearData }) => {
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [seed, setSeed] = useState(0);

  const [loadUrl, setLoadUrl] = useState("");

  useEffect(() => {
    if (loadUrl) {
      let url = loadUrl;
      if (url.includes("/")) {
        url = url.split("/").pop();
      }
      const data = decompress(url);
      if (data) {
        const { year, teams, match } = data;
        if (teams?.length < 6 || teams?.length > 100) {
          return;
        }
        console.log(match);
        setSelectedTeams(teams.map((team) => ({ value: team, label: team })));
        setSeed(match);
      }
    }
  }, [loadUrl]);

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
      <div className="w-full lg:w-4/5 mx-auto flex align-start mb-8">
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
            value={{ value: seed, label: seed }}
            onChange={(e) => setSeed(e.value)}
          />
        </div>
      </div>
      <div className="w-full lg:w-4/5 mx-auto flex items-center justify-center mb-16">
        <p>Or Load from URL: </p>
        <input
          className="ml-2 w-96 rounded ring-2 p-1"
          type="text"
          placeholder="statbotics.io/event/..."
          value={loadUrl}
          onChange={(e) => setLoadUrl(e.target.value)}
        />
      </div>
      {numTeams >= 6 && numTeams <= 100 && (
        <div className="w-full text-center">
          <p className="text-xl flex flex-col items-center">
            Your Custom URL is{" "}
            <div className="flex items-center">
              <Link
                href={`https://www.${url}`}
                className="text_link"
                target="_blank"
                rel="noopener noreferrer"
              >
                {url}
              </Link>
              <div className="tooltip ml-2" data-tip="Copy Link">
                <MdContentCopy
                  className="hover_icon"
                  onClick={() => navigator.clipboard.writeText(url)}
                />
              </div>
            </div>
          </p>
        </div>
      )}
    </div>
  );
};

export default Event;
