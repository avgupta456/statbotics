import React, {useEffect} from "react";

import WindowedSelect from "react-windowed-select";
import { fetchTeams } from './../../api'

export default function TeamSelect({className, onChange, isMulti}) {
  const [teams, setTeams] = React.useState([])

  function cleanList(teams) {
    return (
      teams.map(
        function(x, i) {return x["team"]}
      )
    )
  }

  useEffect(() => {
    const getTeams = async () => {
      const new_teams = await fetchTeams(true, "elo_recent");
      setTeams(cleanList(new_teams.results))
    }

    if(teams.length===0) {getTeams()}

  }, [teams])

  return (
      <WindowedSelect
        className={className}
        isMulti = {isMulti}
        onChange = {onChange}
        options={teams.map(function(x) {return({value: x, label: x})})}
      />
  );
}
