import React, { useState, useEffect } from "react";
import { useParams, useHistory } from "react-router-dom";

import { Paper, Slider, Typography } from "@material-ui/core";
import { Tabs, Tab, Col, Row, Button } from "react-bootstrap";

import { ReactTable, useWindowDimensions } from "./../../../components";
import { default as getMatchDisplays } from "./MatchDisplay";
import { BarElo, BarOPR, Scatter } from "./Figures";

import RingLoader from "react-spinners/RingLoader";

import {
  fetchEvent,
  fetchTeamEvents,
  fetchMatches_Event,
  fetchSimIndex,
} from "./../../../api";

import { ilsMapping } from "./../../../constants";

import styles from "./EventView.module.css";
import NotFound from "../NotFound/NotFound";

export default function EventView() {
  let { key } = useParams();
  const history = useHistory();

  // eslint-disable-next-line no-unused-vars
  const { height, width } = useWindowDimensions();

  const [done, setDone] = useState(false);
  const [show404, setShow404] = useState(false);

  const [eventObj, setEventObj] = useState({});
  const [event, setEvent] = useState("");
  const [year, setYear] = useState("");
  const [ILS1, setILS1] = useState("");
  const [ILS2, setILS2] = useState("");
  const [teams, setTeams] = useState([]);

  const [rp1Acc, setRp1Acc] = useState(0);
  const [rp2Acc, setRp2Acc] = useState(0);

  const [rawStats, setRawStats] = useState([]);
  const [stats, setStats] = useState([]);

  const [rawMatches, setRawMatches] = useState([]);
  const [qualMatches, setQualMatches] = useState([]);
  const [qualsAcc, setQualsAcc] = useState([]);
  const [elimMatches, setElimMatches] = useState([]);
  const [elimsAcc, setElimsAcc] = useState([]);
  const [numMatches, setNumMatches] = useState([]);

  const [quals, setQuals] = useState(50);
  const [index, setIndex] = useState(-1);
  const [rawSim, setRawSim] = useState([]);
  const [cleanSim, setCleanSim] = useState([]);

  const [figState, setFigState] = useState("OPR");
  const [barAll, setBarAll] = useState(false);
  const [barOPRs, setBarOPRs] = useState([]);
  const [barElos, setBarElos] = useState([]);
  const [scatterOPRs, setScatterOPRs] = useState([]);
  const [scatterElos, setScatterElos] = useState([]);

  //column name, searchable, visible, link, hint
  const columns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, ""],
    ["Rank", false, true, false, "Rank at Event"],
    ["Elo", false, true, false, "Current Elo"],
    ["OPR", false, true, false, "Current OPR"],
    ["Auto OPR", false, true, false, ""],
    ["Teleop OPR", false, true, false, ""],
    ["Endgame OPR", false, true, false, ""],
    [ILS1, false, true, false, "ILS score (higher is better)"],
    [ILS2, false, true, false, "ILS score (higher is better)"],
  ];

  const upcomingColumns = [
    columns[0],
    columns[1],
    columns[3],
    columns[4],
    columns[8],
    columns[9],
  ];

  //column name, searchable, visible, link, hint
  const oldColumns = [
    ["Number", true, true, false, ""],
    ["Name", true, true, true, ""],
    ["Rank", false, true, false, "Rank at Event"],
    ["Elo", false, true, false, "Current Elo"],
    ["OPR", false, true, false, "Current OPR"],
  ];

  //column name, searchable, visible, link, hint
  const simColumns = [
    ["Predicted Rank", false, true, false, ""],
    ["Number", true, true, false, ""],
    ["Name", true, true, true, ""],
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
      numMatches > 0
    ) {
      setDone(true);
      setShow404(false);
      setBarAll(false);
    }
  }, [year, event, rawStats, numMatches]);

  useEffect(() => {
    const getEvent = async (key) => {
      const event = await fetchEvent(key);
      if (event !== undefined) {
        setEventObj(event);
        setEvent(event["name"]);
        setYear(event["year"]);
        if (event["year"] >= 2016) {
          setILS1(ilsMapping[event["year"]][0]);
          setILS2(ilsMapping[event["year"]][1]);
        }
        setRp1Acc(event["rp1_acc"]);
        setRp2Acc(event["rp2_acc"]);
        setIndex(
          event.current_match > event.qual_matches ? 0 : event.current_match
        );
      } else {
        setShow404(true);
      }
    };

    const getTeamEvents = async (key) => {
      const team_events = await fetchTeamEvents(key, "-elo_end");
      setRawStats(team_events);
    };

    const getMatches = async (key) => {
      const matches = await fetchMatches_Event(key);
      setRawMatches(matches);
    };

    setDone(false);
    setShow404(false);
    setEvent("");
    setRawStats([]);
    setRawMatches([]);

    getEvent(key);
    getTeamEvents(key);
    getMatches(key);
  }, [key, history]);

  useEffect(() => {
    const getSim = async (key, index) => {
      const sim = await fetchSimIndex(key, index, 0);
      setRawSim(sim);
    };

    setRawSim([]);
    if (year >= 2016 && index >= 0) {
      getSim(key, index);
    }
  }, [year, key, index]);

  useEffect(() => {
    function clean(rawStats) {
      let cleanStats;
      let temp_teams = [];
      if (year >= 2016 && eventObj.current_match > 0) {
        cleanStats = rawStats.map(function (x, i) {
          temp_teams.push({ team: x["team"], name: x["team_name"] });
          return [
            x["team"],
            "./../team/" + x["team"] + "|" + x["team_name"],
            x["rank"] > 0 ? x["rank"] : "",
            x["elo_end"],
            parseInt(x["opr_no_fouls"] * 10) / 10,
            parseInt(x["opr_auto"] * 10) / 10,
            parseInt(x["opr_teleop"] * 10) / 10,
            parseInt(x["opr_endgame"] * 10) / 10,
            x["ils_1_end"],
            x["ils_2_end"],
          ];
        });
        cleanStats.sort((a, b) => a[2] - b[2]);
      } else if (year >= 2016) {
        cleanStats = rawStats.map(function (x, i) {
          temp_teams.push({ team: x["team"], name: x["team_name"] });
          const opr = x["opr_no_fouls"] > 0 ? x["opr_no_fouls"] : x["opr_end"];
          return [
            x["team"],
            "./../team/" + x["team"] + "|" + x["team_name"],
            x["elo_end"],
            parseInt(opr * 10) / 10,
            x["ils_1_end"],
            x["ils_2_end"],
          ];
        });
        cleanStats.sort((a, b) => b[2] - a[2]);
      } else {
        cleanStats = rawStats.map(function (x, i) {
          temp_teams.push({ team: x["team"], name: x["team_name"] });
          return [
            x["team"],
            "./../team/" + x["team"] + "|" + x["team_name"],
            x["rank"] > 0 ? x["rank"] : "",
            x["elo_end"],
            parseInt(x["opr_end"] * 10) / 10,
          ];
        });
        cleanStats.sort((a, b) => a[2] - b[2]);
      }
      setTeams(temp_teams);
      return cleanStats;
    }

    setStats(clean(rawStats));
  }, [year, eventObj, rawStats]);

  useEffect(() => {
    function clean(rawMatches, year, playoffs) {
      if (!rawMatches) {
        return [];
      }

      let cleanMatches;

      let tempMatches = [];
      for (let i = 0; i < rawMatches.length; i++) {
        let prefix = rawMatches[i]["key"].split("_")[1].slice(0, 2);
        if ((prefix === "qm" && !playoffs) || (prefix !== "qm" && playoffs)) {
          tempMatches.push(rawMatches[i]);
        }
      }

      let correct = 0;
      let total = 0;
      if (year >= 2016) {
        cleanMatches = tempMatches.map(function (x, i) {
          if (x["status"] === "Completed") {
            total += 1;
            if (x["winner"] === x["mix_winner"]) {
              correct += 1;
            }
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
        cleanMatches = tempMatches.map(function (x, i) {
          if (x["status"] === "Completed") {
            total += 1;
            if (x["winner"] === x["mix_winner"]) {
              correct += 1;
            }
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

      const parseNum = (str) =>
        str
          .replace("qm", "0")
          .replace("qf", "1")
          .replace("sf", "2")
          .replace("f", "3")
          .replace("m", "0");
      cleanMatches = cleanMatches.sort(
        (a, b) => parseNum(a["match"]) - parseNum(b["match"])
      );

      return [cleanMatches, total > 0 ? correct / total : 0];
    }

    const quals = clean(rawMatches, year, false);
    setQualMatches(quals[0]);
    setQualsAcc(quals[1]);

    const elims = clean(rawMatches, year, true);
    setElimMatches(elims[0]);
    setElimsAcc(elims[1]);

    setQuals(quals[0].length);
    setNumMatches(quals.length + elims.length);
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
        "./../team/" + x["team"] + "|" + x["name"],
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
    const getBarOPRs = (stats, barAll) => {
      let temp_stats = stats.slice();
      temp_stats = temp_stats.filter((x) => x[2] > 0);
      temp_stats.sort((a, b) => b[4] - a[4]);
      if (!barAll) {
        temp_stats = temp_stats.slice(0, 15);
      }
      let oprs = [];
      if (year >= 2016) {
        oprs = temp_stats.map(function (x, i) {
          return {
            team: x[0].toString(),
            "Auto OPR": x[5],
            "Teleop OPR": x[6],
            "Endgame OPR": x[7],
          };
        });
      } else {
        oprs = temp_stats.map(function (x, i) {
          return {
            team: x[0].toString(),
            OPR: x[4],
          };
        });
      }
      setBarOPRs(oprs);
    };

    const getBarElos = (stats, barAll) => {
      let temp_stats = stats.slice();
      temp_stats = temp_stats.filter((x) => x[2] > 0);
      temp_stats.sort((a, b) => b[3] - a[3]);
      if (!barAll) {
        temp_stats = temp_stats.slice(0, 15);
      }
      const elos = temp_stats.map(function (x, i) {
        return {
          team: x[0].toString(),
          Elo: x[3],
        };
      });
      setBarElos(elos);
    };

    const getScatterOPRs = (stats) => {
      const pairs = stats.map(function (a, i) {
        return {
          id: a[0].toString(),
          data: [{ x: a[2], y: a[4] }],
        };
      });
      setScatterOPRs(pairs);
    };

    const getScatterElos = (stats) => {
      const pairs = stats.map(function (a, i) {
        return {
          id: a[0].toString(),
          data: [{ x: a[2], y: a[3] }],
        };
      });
      setScatterElos(pairs);
    };

    if (stats.length > 0) {
      getBarOPRs(stats, barAll);
      getBarElos(stats, barAll);
      getScatterOPRs(stats);
      getScatterElos(stats);
    }
  }, [stats, year, barAll]);

  function FigClick() {
    if (figState === "OPR") {
      setFigState("Elo");
    } else {
      setFigState("OPR");
    }
  }

  function simTab() {
    return (
      <Tab
        eventKey="simulation"
        title="Simulation"
        tabClassName={width > 600 ? "" : styles.mobileTab}
        disabled={quals === 0 || year < 2016}
      >
        <br />
        <h4>Simulation</h4>
        Using the Elo, OPR, and ILS statistics from a snapshot in time, we can
        simulate the remainder of the event. For each seed index, 100
        simulations are run and analyzed. The first tiebreaker is included from
        2016 onwards.{" "}
        <b>
          The simulation happens live, and may take a few seconds to load. Be
          patient :)
        </b>
        <hr />
        Simulate from:
        {index === 0 ? " Schedule Release" : ` Qualification Match ${index}`}
        {eventObj.current_match > eventObj.qual_matches && (
          <div className={styles.slider}>
            <Slider
              defaultValue={0}
              onChangeCommitted={handleSliderChange}
              valueLabelDisplay="auto"
              marks
              step={1}
              min={0}
              max={eventObj.current_match}
            />
          </div>
        )}
        <ReactTable
          title="Ranking Simulation"
          columns={simColumns}
          data={cleanSim}
        />
      </Tab>
    );
  }

  function getBarChart() {
    if (figState === "OPR") {
      const keys =
        year >= 2016 ? ["Auto OPR", "Teleop OPR", "Endgame OPR"] : ["OPR"];
      return (
        <div>
          <div className={styles.horizontal}>
            <h5 className={styles.rightPad}>Top OPRs</h5>
            <Button
              variant="outline-dark"
              onClick={() => setBarAll(!barAll)}
              className={styles.button}
            >
              <Typography>{barAll ? "Less" : "More"}</Typography>
            </Button>
          </div>
          <BarOPR data={barOPRs} keys={keys} />
        </div>
      );
    } else {
      return (
        <div>
          <div className={styles.horizontal}>
            <h5 className={styles.rightPad}>Top Elos</h5>
            <Button
              variant="outline-dark"
              onClick={() => setBarAll(!barAll)}
              className={styles.button}
            >
              <Typography>{barAll ? "Less" : "More"}</Typography>
            </Button>
          </div>
          <BarElo data={barElos} />
        </div>
      );
    }
  }

  function getScatterChart() {
    if (figState === "OPR") {
      return (
        <div>
          <h5>OPR vs Rank</h5>
          <Scatter data={scatterOPRs} axis={"OPR"} />
        </div>
      );
    } else {
      return (
        <div>
          <h5>Elo vs Rank</h5>
          <Scatter data={scatterElos} axis={"Elo"} />
        </div>
      );
    }
  }

  //Function Render Below

  if (show404) {
    return <NotFound />;
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
        {year} {event}{" "}
        <a
          href={`https://www.thebluealliance.com/event/${key}`}
          target="_blank"
          rel="noopener noreferrer"
        >
          (TBA)
        </a>
      </h2>
      <br />
      <Tabs defaultActiveKey="insights" id="tab">
        <Tab
          eventKey="insights"
          title="Insights"
          tabClassName={width > 600 ? "" : styles.mobileTab}
        >
          <br />
          <h4>Team Statistics</h4>
          <ReactTable
            title="Team Statistics"
            columns={
              year >= 2016
                ? eventObj.current_match <= 0
                  ? upcomingColumns
                  : columns
                : oldColumns
            }
            data={stats.filter((x) => year <= 2006 || x[2] > 0)}
          />
        </Tab>

        <Tab
          eventKey="Figures"
          title="Figures"
          tabClassName={width > 600 ? "" : styles.mobileTab}
          disabled={eventObj.current_match <= 0 || year <= 2006}
        >
          <br />
          <Row>
            <Col xs="auto" className={styles.slider}>
              <h4>Figures!</h4>
            </Col>
            <Col>
              <Button variant="outline-dark" onClick={() => FigClick()}>
                <Typography>
                  {figState === "OPR" ? "Show Elo" : "Show OPR"}
                </Typography>
              </Button>
            </Col>
          </Row>
          <hr />
          {getBarChart()}
          <hr />
          {getScatterChart()}
        </Tab>

        <Tab
          eventKey="Quals"
          title="Qual Matches"
          tabClassName={width > 600 ? "" : styles.mobileTab}
          disabled={eventObj.current_match < 0}
        >
          <br />
          <h4>Match Predictions</h4>
          Remember, match predictions are just for fun, you control your own
          destiny!
          {year >= 2016 ? (
            <div>
              <p>
                <b>Accuracy: {parseInt(qualsAcc * 1000) / 10}%</b>
                &nbsp;| RP1 Accuracy: {parseInt(rp1Acc * 1000) / 10}% &nbsp;|
                RP2 Accuracy: {parseInt(rp2Acc * 1000) / 10}%
              </p>
            </div>
          ) : (
            <div>
              <b>Accuracy: {parseInt(qualsAcc * 1000) / 10}%</b>
            </div>
          )}
          <hr />
          <div className={styles.matches}>
            {getMatchDisplays(year, qualMatches)}
          </div>
        </Tab>

        <Tab
          eventKey="Elims"
          title="Elim Matches"
          tabClassName={width > 600 ? "" : styles.mobileTab}
          disabled={
            eventObj.current_match < 0 ||
            eventObj.current_match < eventObj.qual_matches
          }
        >
          <br />
          <h4>Match Predictions</h4>
          Remember, match predictions are just for fun, you control your own
          destiny!
          <div>
            <b>Accuracy: {parseInt(elimsAcc * 1000) / 10}%</b>
          </div>
          <hr />
          <div className={styles.matches}>
            {getMatchDisplays(year, elimMatches)}
          </div>
        </Tab>

        {simTab()}
      </Tabs>
    </Paper>
  );
}
