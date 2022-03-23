import React, { useState, useEffect } from "react";
import { useParams, useHistory } from "react-router-dom";

import { Paper, Typography } from "@material-ui/core";
import Select from "react-select";

import { fetchTeam_Years, fetchTeamEvents_TeamYear } from "./../../../api";
import { ReactTable, LineChart } from "./../../";

import styles from "./TeamView.module.css";

import { yearOptions } from "./../../../constants";
import NotFound from "../NotFound/NotFound";

export default function TeamView() {
  const history = useHistory();

  const [show404, setShow404] = useState(false);

  const [eventData, setEventData] = useState([]);
  const [yearData, setYearData] = useState([]);
  const [chartData, setChartData] = useState({
    id: "",
    data: [{ x: 0, y: 0 }],
  });

  let { team } = useParams();
  const [name, setName] = useState([]);

  const [year, setYear] = useState(2020);

  //column name, searchable, visible, link, hint
  const eventColumns = [
    ["Key", false, true, false, ""],
    ["Name", false, true, true, ""],
    ["Year", false, true, false, ""],
    ["Week", false, true, false, ""],
    ["Record", false, true, false, ""],
    ["Rank", false, true, false, ""],
    ["Elo", false, true, false, ""],
    ["OPR", false, true, false, ""],
  ];

  //column name, searchable, visible, link, hint
  const yearColumns = [
    ["Year", false, true, false, ""],
    ["Record", false, true, false, ""],
    ["Win Rate", false, true, false, ""],
    ["Max Elo", false, true, false, ""],
    ["Mean Elo", false, false, false, ""],
    ["Start Elo", false, false, false, ""],
    ["Pre Champs Elo", false, false, false, ""],
    ["End Elo", false, false, false, ""],
    ["Elo Rank", false, true, false, ""],
    ["Elo Percentile", false, true, false, ""],
    ["OPR", false, true, false, ""],
    ["Auto OPR", false, false, false, ""],
    ["Teleop OPR", false, false, false, ""],
    ["Endgame OPR", false, false, false, ""],
    ["ILS 1", false, false, false, ""],
    ["ILS 2", false, false, false, ""],
    ["OPR Rank", false, true, false, ""],
    ["OPR Percentile", false, true, false, ""],
  ];

  function cleanChart(team, data) {
    return {
      id: team,
      data: data.map(function (x, i) {
        return {
          x: x["year"],
          y: x["elo_max"],
        };
      }),
    };
  }

  function cleanYear(data) {
    const temp_data = data.reverse();
    return temp_data.map(function (x, i) {
      setName(x["name"]);

      let opr = parseInt(x["opr"] * 10) / 10;
      let opr_auto = -1;
      let opr_teleop = -1;
      let opr_endgame = -1;
      let ils_1 = -1;
      let ils_2 = -1;
      if (x["year"] >= 2016) {
        opr = parseInt(x["opr_no_fouls"] * 10) / 10;
        opr_auto = parseInt(x["opr_auto"] * 10) / 10;
        opr_teleop = parseInt(x["opr_teleop"] * 10) / 10;
        opr_endgame = parseInt(x["opr_endgame"] * 10) / 10;
        ils_1 = x["ils_1"];
        ils_2 = x["ils_2"];
      }
      return [
        x["year"],
        x["wins"] + "-" + x["losses"] + "-" + x["ties"],
        parseInt(x["winrate"] * 1000) / 1000,
        x["elo_max"],
        x["elo_mean"],
        x["elo_start"],
        x["elo_pre_champs"],
        x["elo_end"],
        x["elo_rank"],
        100 - Math.max((100 * x["elo_percentile"]).toFixed(1), 0.1),
        opr,
        opr_auto,
        opr_teleop,
        opr_endgame,
        ils_1,
        ils_2,
        x["opr_rank"],
        100 - Math.max((100 * x["opr_percentile"]).toFixed(1), 0.1),
      ];
    });
  }

  function cleanEvent(data) {
    const temp_data = data.reverse();
    return temp_data.map(function (x, i) {
      let opr = x["opr_end"];
      if (x["year"] >= 2016) {
        opr = x["opr_no_fouls"];
      }
      let event_name = x["event_name"];
      if (event_name.length > 30) {
        event_name = event_name.slice(0, 27) + "...";
      }
      return [
        x["event"],
        "./../event/" + x["event"] + "|" + event_name,
        x["year"],
        x["week"],
        x["wins"] + "-" + x["losses"] + "-" + x["ties"],
        x["rank"] > 0 ? x["rank"] : "",
        x["elo_max"],
        opr,
      ];
    });
  }

  useEffect(() => {
    const getTeamYears = async (team) => {
      const team_years = await fetchTeam_Years(team);
      if (team_years.length > 0) {
        setChartData(cleanChart(team, team_years));
        setYearData(cleanYear(team_years));
        setYear(team_years[0]["year"]);
      } else {
        setShow404(true);
      }
    };

    getTeamYears(team);
  }, [team, history]);

  useEffect(() => {
    const getTeamEvents = async (team, year) => {
      const team_events = await fetchTeamEvents_TeamYear(team, year);
      setEventData(cleanEvent(team_events));
    };

    getTeamEvents(team, year);
  }, [team, year]);

  const yearClick = (year) => {
    setYear(year["value"]);
  };

  function getTitle() {
    return (
      <div className={styles.title}>
        <div className={styles.title_text}>
          <Typography variant="h6">{team}:&nbsp;</Typography>
        </div>
        <Select
          className={styles.dropdown}
          styles={{
            menu: (provided) => ({ ...provided, zIndex: 9999 }),
          }}
          options={yearOptions}
          onChange={yearClick}
          value={{ value: `${year}`, label: `${year}` }}
        />
        <div className={styles.title_text}>
          <Typography variant="h6">&nbsp;Events</Typography>
        </div>
      </div>
    );
  }

  if (show404) {
    return <NotFound />;
  }

  return (
    <Paper elevation={3} className={styles.body}>
      <Typography variant="h4">
        Team {team} - {name}
      </Typography>
      <ReactTable title={getTitle()} columns={eventColumns} data={eventData} />
      <hr />
      <br />
      <ReactTable
        title={<Typography variant="h6">{team}: Recent Years</Typography>}
        columns={yearColumns}
        data={yearData}
      />
      <hr />
      <br />
      <div className={styles.chart}>
        <Typography variant="h6">{team}: Elo through Time</Typography>
        <LineChart data={[chartData]} />
      </div>
    </Paper>
  );
}
