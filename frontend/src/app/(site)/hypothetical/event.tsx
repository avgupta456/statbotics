import React, { useEffect, useState } from "react";
import { MdContentCopy } from "react-icons/md";
import Select, { createFilter } from "react-select";
import WindowedSelect from "react-windowed-select";

import Link from "next/link";

import { PROD } from "../../../constants";
import { TeamYearsData } from "../../../types/data";
import { classnames, decompress } from "../../../utils";
import { compress } from "../../../utils";

// for multi-select
const formatTeam = (team) => ({
  value: team.num,
  label: `${team.num} | ${team.team}`,
});

const Event = ({ data, year }: { data: TeamYearsData; year: number }) => {
  const [selectedTeams, setSelectedTeams] = useState<any>([]);
  const [seed, setSeed] = useState(0);

  const [loadUrl, setLoadUrl] = useState("");
  const [invalidUrl, setInvalidUrl] = useState(false);

  const [commaSep, setCommaSep] = useState("");
  const [invalidCommaSep, setInvalidCommaSep] = useState(false);

  useEffect(() => {
    if (loadUrl) {
      let url = loadUrl;
      if (url.includes("/")) {
        url = url.split("/").pop();
      }
      const decompressData = decompress(url);
      if (data) {
        const { year: dataYear, teams: dataTeams, match: dataMatch } = decompressData;
        if (dataYear !== year) {
          setInvalidUrl(true);
          return;
        }

        if (dataTeams?.length < 6 || dataTeams?.length > 100) {
          setInvalidUrl(true);
          return;
        }

        // get from data.team_years
        const teamObjs = dataTeams.map((team) =>
          data.team_years.find((teamYear) => teamYear.num === team)
        );

        if (teamObjs.some((team) => !team)) {
          setInvalidUrl(true);
          return;
        }

        setSelectedTeams(teamObjs.map((team) => formatTeam(team)));
        setSeed(dataMatch);
      }
    }
  }, [data, year, loadUrl]);

  useEffect(() => {
    if (commaSep) {
      const teams = commaSep.split(",").map((team) => team.trim());
      if (teams.length === 0 || teams.length > 100) {
        setInvalidCommaSep(true);
        return;
      }

      const teamObjs = teams.map((team) =>
        data.team_years.find((teamYear) => teamYear.num === parseInt(team))
      );

      if (teamObjs.some((team) => !team)) {
        setInvalidCommaSep(true);
        return;
      }

      setSelectedTeams(teamObjs.map((team) => formatTeam(team)));
    }
  }, [data, commaSep]);

  const addTeam = async (selected) => {
    if (selected.length > 100) {
      return;
    }
    setLoadUrl("");
    setCommaSep("");
    setSelectedTeams(selected);
  };

  const setRandomSeed = (seed) => {
    setLoadUrl("");
    setCommaSep("");
    setSeed(seed);
  };

  const teamOptions = data.team_years.sort((a, b) => a.num - b.num).map((team) => formatTeam(team));

  const TeamSelect = ({ className }) => (
    <WindowedSelect
      autoFocus={!loadUrl && !commaSep}
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

  const url = PROD
    ? `statbotics.io/event/${compress(year, teamNums, seed)}`
    : `localhost:3000/event/${compress(year, teamNums, seed)}`;

  const fullUrl = PROD ? `https://www.${url}` : `http://${url}`;

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
            onChange={(e) => setRandomSeed(e.value)}
          />
        </div>
      </div>
      <div className="w-full lg:w-4/5 mx-auto flex items-center justify-center mb-8">
        <p>Or Load from URL: </p>
        <input
          className={classnames(
            "ml-2 w-96 rounded border border-gray-300 p-1",
            invalidUrl && "border-red-500 bg-red-100"
          )}
          type="text"
          placeholder="statbotics.io/event/..."
          value={loadUrl}
          onChange={(e) => {
            setInvalidUrl(false);
            setLoadUrl(e.target.value);
          }}
        />
      </div>
      <div className="w-full lg:w-4/5 mx-auto flex items-center justify-center mb-16">
        <p>Or Load from Comma-Separated Team List: </p>
        <input
          className={classnames(
            "ml-2 w-96 rounded border border-gray-300 p-1",
            invalidCommaSep && "border-red-500 bg-red-100"
          )}
          type="text"
          placeholder="A, B, C, ..."
          value={commaSep}
          onChange={(e) => {
            setInvalidCommaSep(false);
            setCommaSep(e.target.value);
          }}
        />
      </div>
      {numTeams >= 6 && numTeams <= 100 && (
        <div className="w-full text-center">
          <p className="text-xl flex flex-col items-center">
            Your Custom URL is{" "}
            <div className="flex items-center">
              <Link href={fullUrl} className="text_link" target="_blank" rel="noopener noreferrer">
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
