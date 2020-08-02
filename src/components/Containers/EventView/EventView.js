import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import { Paper, Slider } from "@material-ui/core";
import { Tabs, Tab } from "react-bootstrap";

import { ReactTable } from "./../../../components";
import { default as getMatchDisplays } from "./MatchDisplay";
import { default as BarChart } from "./Bar";

import RingLoader from "react-spinners/RingLoader";

import {
  fetchEvent,
  fetchTeamEvents,
  fetchRankings,
  fetchMatches_Event,
  fetchSimIndex,
} from "./../../../api";

import styles from "./EventView.module.css";

export default function EventView() {
  let { key } = useParams();

  const [done, setDone] = useState(false);

  const [event, setEvent] = useState("");
  const [year, setYear] = useState("");
  const [teams, setTeams] = useState([]);

  const [acc, setAcc] = useState(0);
  const [rp1Acc, setRp1Acc] = useState(0);
  const [rp2Acc, setRp2Acc] = useState(0);

  const [rankings, setRankings] = useState([]);
  const [rawStats, setRawStats] = useState([]);
  const [stats, setStats] = useState([]);

  const [rawMatches, setRawMatches] = useState([]);
  const [matches, setMatches] = useState([]);

  const [quals, setQuals] = useState(50);
  const [index, setIndex] = useState(0);
  const [rawSim, setRawSim] = useState([]);
  const [cleanSim, setCleanSim] = useState([]);

  const [oprs, setOPRs] = useState([]);

  //column name, searchable, visible, link, hint
  const columns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, "Click name for details"],
    ["Rank", false, true, false, "Rank at Event"],
    ["Elo", false, true, false, "Current Elo"],
    ["OPR", false, true, false, "Current OPR"],
    ["Auto OPR", false, true, false, ""],
    ["Teleop OPR", false, true, false, ""],
    ["Endgame OPR", false, true, false, ""],
    ["ILS 1", false, true, false, ""],
    ["ILS 2", false, true, false, ""],
  ];

  //column name, searchable, visible, link, hint
  const oldColumns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, "Click name for details"],
    ["Rank", false, true, false, "Rank at Event"],
    ["Elo", false, true, false, "Current Elo"],
    ["OPR", false, true, false, "Current OPR"],
  ];

  //column name, searchable, visible, link, hint
  const simColumns = [
    ["Predicted Rank", false, true, false, ""],
    ["Number", true, true, false, ""],
    ["Name", true, true, true, "Click name for details"],
    ["Mean Rank", false, true, false, ""],
    ["5% Rank", false, true, false, ""],
    ["Median Rank", false, true, false, ""],
    ["95% Rank", false, true, false, ""],
    ["Mean RPs", false, true, false, ""],
  ];

  useEffect(() => {
    if (
      year > 2000 &&
      event.length > 0 &&
      rawStats.length > 0 &&
      rankings.length !== 0 &&
      matches.length > 0
    ) {
      setDone(true);
    }
  }, [year, event, rawStats, rankings, matches]);

  useEffect(() => {
    const getEvent = async (key) => {
      const event = await fetchEvent(key);
      setEvent(event["name"]);
      setYear(event["year"]);
      setAcc(event["mix_acc"]);
      setRp1Acc(event["rp1_acc"]);
      setRp2Acc(event["rp2_acc"]);
    };

    const getTeamEvents = async (key) => {
      const team_events = await fetchTeamEvents(key, "-elo_end");
      setRawStats(team_events);
    };

    const getRankings = async (key) => {
      const rankings = await fetchRankings(key);
      setRankings(rankings);
    };

    const getMatches = async (key) => {
      const matches = await fetchMatches_Event(key);
      setRawMatches(matches);
    };

    getEvent(key);
    getTeamEvents(key);
    getRankings(key);
    getMatches(key);
  }, [key]);

  useEffect(() => {
    const getSim = async (key, index) => {
      const sim = await fetchSimIndex(key, index, 0);
      setRawSim(sim);
    };

    setRawSim([]);
    getSim(key, index);
  }, [key, index]);

  useEffect(() => {
    function clean(rawStats, rankings) {
      let cleanStats;
      let temp_teams = [];
      if (year >= 2016) {
        cleanStats = rawStats.map(function (x, i) {
          temp_teams.push({ team: x["team"], name: x["name"] });
          return [
            x["team"],
            "./../teams/" + x["team"] + "|" + x["name"],
            rankings[x["team"]],
            x["elo_end"],
            parseInt(x["opr_no_fouls"] * 10) / 10,
            parseInt(x["opr_auto"] * 10) / 10,
            parseInt(x["opr_teleop"] * 10) / 10,
            parseInt(x["opr_endgame"] * 10) / 10,
            x["ils_1_end"],
            x["ils_2_end"],
          ];
        });
      } else {
        cleanStats = rawStats.map(function (x, i) {
          temp_teams.push({ team: x["team"], name: x["name"] });
          return [
            x["team"],
            "./../teams/" + x["team"] + "|" + x["name"],
            rankings[x["team"]],
            x["elo_end"],
            parseInt(x["opr_end"] * 10) / 10,
          ];
        });
      }
      setTeams(temp_teams);
      cleanStats.sort((a, b) => a[2] - b[2]);
      return cleanStats;
    }

    setStats(clean(rawStats, rankings));
  }, [year, rawStats, rankings]);

  useEffect(() => {
    function clean(rawMatches, year) {
      if (!rawMatches) {
        return [];
      }
      let cleanMatches;
      let quals = 0;
      if (year >= 2016) {
        cleanMatches = rawMatches.map(function (x, i) {
          if (x["key"].split("_")[1].slice(0, 2) === "qm") {
            quals += 1;
          }
          return {
            match: x["key"].split("_")[1],
            playoff: x["playoff"],
            blue: x["blue"].split(","),
            red: x["red"].split(","),
            blue_score: x["blue_score"],
            red_score: x["red_score"],
            winner: x["winner"],
            winner_pred: x["mix_winner"],
            win_prob:
              x["mix_winner"] === "red"
                ? x["mix_win_prob"]
                : 1 - x["mix_win_prob"],
            winner_correct: x["winner"] === x["mix_winner"],
            blue_rp_1: x["blue_rp_1"],
            blue_rp_1_prob: x["blue_rp_1_prob"],
            blue_rp_1_correct:
              x["blue_rp_1"] === 1
                ? x["blue_rp_1_prob"] >= 0.5
                : x["blue_rp_1_prob"] < 0.5,
            blue_rp_2: x["blue_rp_2"],
            blue_rp_2_prob: x["blue_rp_2_prob"],
            blue_rp_2_correct:
              x["blue_rp_2"] === 1
                ? x["blue_rp_2_prob"] >= 0.5
                : x["blue_rp_2_prob"] < 0.5,
            red_rp_1: x["red_rp_1"],
            red_rp_1_prob: x["red_rp_1_prob"],
            red_rp_1_correct:
              x["red_rp_1"] === 1
                ? x["red_rp_1_prob"] >= 0.5
                : x["red_rp_1_prob"] < 0.5,
            red_rp_2: x["red_rp_2"],
            red_rp_2_prob: x["red_rp_2_prob"],
            red_rp_2_correct:
              x["red_rp_2"] === 1
                ? x["red_rp_2_prob"] >= 0.5
                : x["red_rp_2_prob"] < 0.5,
          };
        });
      } else {
        cleanMatches = rawMatches.map(function (x, i) {
          if (x["key"].split("_")[1].slice(0, 2) === "qm") {
            quals += 1;
          }
          return {
            match: x["key"].split("_")[1],
            playoff: x["playoff"],
            blue: x["blue"].split(","),
            red: x["red"].split(","),
            blue_score: x["blue_score"],
            red_score: x["red_score"],
            winner: x["winner"],
            winner_pred: x["mix_winner"],
            win_prob:
              x["mix_winner"] === "red"
                ? x["mix_win_prob"]
                : 1 - x["mix_win_prob"],
            winner_correct: x["winner"] === x["mix_winner"],
          };
        });
      }
      setQuals(quals);
      return cleanMatches;
    }

    setMatches(clean(rawMatches, year));
  }, [year, rawMatches]);

  useEffect(() => {
    let clean = teams.map(function (x, i) {
      let rank_mean = "";
      let rank_5 = "";
      let rank_median = "";
      let rank_95 = "";
      let rps_mean = "";
      try {
        rank_mean = rawSim["sim_ranks"][x["team"]];
        rps_mean = rawSim["mean_rps"][x["team"]];
        let cum_sum = 0;
        for (let j = 1; j <= teams.length; j++) {
          let prob = rawSim["sim_rank_probs"][x["team"]][j];
          cum_sum += prob;
          if (rank_5 === "" && cum_sum >= 0.05) {
            rank_5 = j;
          }
          if (rank_median === "" && cum_sum >= 0.5) {
            rank_median = j;
          }
          if (rank_95 === "" && cum_sum >= 0.95) {
            rank_95 = j;
          }
        }
      } catch (e) {}
      return [
        x["team"],
        "./../teams/" + x["team"] + "|" + x["name"],
        rank_mean,
        rank_5,
        rank_median,
        rank_95,
        rps_mean,
      ];
    });
    clean.sort((a, b) => a[2] - b[2]);
    clean = clean.map(function (x, i) {
      return [i + 1, x[0], x[1], x[2], x[3], x[4], x[5], x[6]];
    });
    setCleanSim(clean);
  }, [rawSim, teams, index]);

  const handleSliderChange = (event, newIndex) => {
    setIndex(newIndex);
  };

  useEffect(() => {
    let temp_stats = stats;
    temp_stats.sort((a, b) => b[4] - a[4]);
    temp_stats = temp_stats.slice(0, 15);
    const oprs = temp_stats.map(function (x, i) {
      return {
        team: x[0],
        "Auto OPR": x[5],
        "Teleop OPR": x[6],
        "Endgame OPR": x[7],
      };
    });
    console.log(oprs);
    setOPRs(oprs);
  }, [stats]);

  function simTab() {
    if (quals === 0) {
      return <Tab eventKey="simulation" title="Simulation" disabled></Tab>;
    } else {
      return (
        <Tab eventKey="simulation" title="Simulation">
          <br />
          <h4>Simulation</h4>
          Using the Elo, OPR, and ILS statistics from a snapshot in time, we can
          simulate the remainder of the event. For each seed index, 100
          simulations are run and analyzed. The first tiebreaker is included
          from 2016 onwards.{" "}
          <b>
            The simulation happens live, and may take a few seconds to load. Be
            patient :)
          </b>
          <hr />
          Simulate from:
          {index === 0 ? " Schedule Release" : ` Qualification Match ${index}`}
          <div className={styles.slider}>
            <Slider
              defaultValue={0}
              onChangeCommitted={handleSliderChange}
              valueLabelDisplay="auto"
              marks
              step={1}
              min={0}
              max={quals}
            />
          </div>
          <ReactTable
            title="Ranking Simulation"
            columns={simColumns}
            data={cleanSim}
          />
        </Tab>
      );
    }
  }

  if (done === false) {
    return (
      <div className={styles.center}>
        <RingLoader size={150} color={"#123abc"} loading={true} />
      </div>
    );
  }

  return (
    <Paper className={styles.body}>
      <h2>
        {year} {event}
      </h2>
      <br />
      <Tabs defaultActiveKey="insights" id="tab">
        <Tab eventKey="insights" title="Insights">
          <ReactTable
            title="Current Statistics"
            columns={year >= 2016 ? columns : oldColumns}
            data={stats}
          />
        </Tab>
        {simTab()}
        <Tab eventKey="Matches" title="Matches">
          <br />
          <h4>Match Predictions</h4>
          Remember, match predictions are just for fun, you control your own
          destiny!
          {year >= 2016 ? (
            <div>
              <b>Accuracy: {parseInt(acc * 1000) / 10}%</b>
              <br />
              <b>RP1 Accuracy: {parseInt(rp1Acc * 1000) / 10}%</b>
              <br />
              <b>RP2 Accuracy: {parseInt(rp2Acc * 1000) / 10}%</b>
            </div>
          ) : (
            <div>
              <b>Accuracy: {parseInt(acc * 1000) / 10}%</b>
            </div>
          )}
          <hr />
          <div className={styles.matches}>
            {getMatchDisplays(year, matches)}
          </div>
        </Tab>
        <Tab eventKey="Figures" title="Figures">
          <br />
          <h4>Figures!</h4>
          <hr />
          <h5>Top 15 OPRs</h5>
          <BarChart data={oprs} />
        </Tab>
      </Tabs>
    </Paper>
  );
}
