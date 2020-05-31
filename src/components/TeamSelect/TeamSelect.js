import React, {useEffect} from "react";

import WindowedSelect from "react-windowed-select";
import { fetchTeams_Simple } from './../../api'

export default function TeamSelect({className, onChange, isMulti}) {
  const [teams, setTeams] = React.useState([])
  const max_length = 30

  function cleanList(teams) {
    return (
      teams.map(
        function(x, i) {
          if(x["name"].length>max_length) {
            x["name"]=x["name"].substring(0, max_length-3)+"..."
          }
          return {
            value: x["team"],
            label: x["team"] + " | " + x["name"],
          }
        }
      )
    )
  }

  useEffect(() => {
    const getTeams = async () => {
      const new_teams = await fetchTeams_Simple();
      setTeams(cleanList(new_teams.results))
    }

    if(teams.length===0) {getTeams()}

  }, [teams])

  return (
      <WindowedSelect
        placeholder={"Search Teams"}
        className={className}
        isMulti = {isMulti}
        onChange = {onChange}
        options={teams}
      />
  );
}
