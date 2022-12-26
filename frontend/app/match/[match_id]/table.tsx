import React from "react";

import MatchTable, { Component } from "../../../components/Table/MatchTable";
import { TableKey } from "../../../components/Table/shared";
import { round } from "../../../utils";
import { Data } from "./types";

const PageMatchTable = ({ data }: { data: Data }) => {
  const red1 = data.match.red[0];
  const red1Data = data.team_matches[red1];
  const red2 = data.match.red[1];
  const red2Data = data.team_matches[red2];
  const red3 = data.match.red[2];
  const red3Data = data.team_matches[red3];
  const blue1 = data.match.blue[0];
  const blue1Data = data.team_matches[blue1];
  const blue2 = data.match.blue[1];
  const blue2Data = data.team_matches[blue2];
  const blue3 = data.match.blue[2];
  const blue3Data = data.team_matches[blue3];

  const autoComponent = {
    name: "Auto",
    red1: red1Data.auto_epa,
    red2: red2Data.auto_epa,
    red3: red3Data.auto_epa,
    redTotal: data.match.red_auto_epa_sum,
    redActual: data.match.red_auto,
    blue1: blue1Data.auto_epa,
    blue2: blue2Data.auto_epa,
    blue3: blue3Data.auto_epa,
    blueTotal: data.match.blue_auto_epa_sum,
    blueActual: data.match.blue_auto,
  };

  const teleopComponent = {
    name: "Teleop",
    red1: red1Data.teleop_epa,
    red2: red2Data.teleop_epa,
    red3: red3Data.teleop_epa,
    redTotal: data.match.red_teleop_epa_sum,
    redActual: data.match.red_teleop,
    blue1: blue1Data.teleop_epa,
    blue2: blue2Data.teleop_epa,
    blue3: blue3Data.teleop_epa,
    blueTotal: data.match.blue_teleop_epa_sum,
    blueActual: data.match.blue_teleop,
  };

  const endgameComponent = {
    name: "Endgame",
    red1: red1Data.endgame_epa,
    red2: red2Data.endgame_epa,
    red3: red3Data.endgame_epa,
    redTotal: data.match.red_endgame_epa_sum,
    redActual: data.match.red_endgame,
    blue1: blue1Data.endgame_epa,
    blue2: blue2Data.endgame_epa,
    blue3: blue3Data.endgame_epa,
    blueTotal: data.match.blue_endgame_epa_sum,
    blueActual: data.match.blue_endgame,
  };

  const foulComponent = {
    name: "Fouls",
    red1: null,
    red2: null,
    red3: null,
    redTotal: data.match.red_epa_sum * data.year_stats.foul_rate,
    redActual: data.match.red_fouls,
    blue1: null,
    blue2: null,
    blue3: null,
    blueTotal: data.match.blue_epa_sum * data.year_stats.foul_rate,
    blueActual: data.match.blue_fouls,
  };

  const rp1Component = {
    name: "RP1",
    red1: red1Data.rp_1_epa,
    red2: red2Data.rp_1_epa,
    red3: red3Data.rp_1_epa,
    redTotal: data.match.red_rp_1_prob,
    redActual: data.match.red_rp_1,
    blue1: blue1Data.rp_1_epa,
    blue2: blue2Data.rp_1_epa,
    blue3: blue3Data.rp_1_epa,
    blueTotal: data.match.blue_rp_1_prob,
    blueActual: data.match.blue_rp_1,
  };

  const rp2Component = {
    name: "RP2",
    red1: red1Data.rp_2_epa,
    red2: red2Data.rp_2_epa,
    red3: red3Data.rp_2_epa,
    redTotal: data.match.red_rp_2_prob,
    redActual: data.match.red_rp_2,
    blue1: blue1Data.rp_2_epa,
    blue2: blue2Data.rp_2_epa,
    blue3: blue3Data.rp_2_epa,
    blueTotal: data.match.blue_rp_2_prob,
    blueActual: data.match.blue_rp_2,
  };

  const totalComponent = {
    name: "Total",
    red1: red1Data.epa,
    red2: red2Data.epa,
    red3: red3Data.epa,
    redTotal: data.match.red_epa_sum * (1 + data.year_stats.foul_rate),
    redActual: data.match.red_score,
    blue1: blue1Data.epa,
    blue2: blue2Data.epa,
    blue3: blue3Data.epa,
    blueTotal: data.match.blue_epa_sum * (1 + data.year_stats.foul_rate),
    blueActual: data.match.blue_score,
  };

  const matchData = [
    autoComponent,
    teleopComponent,
    endgameComponent,
    foulComponent,
    rp1Component,
    rp2Component,
    totalComponent,
  ].map((component, i) => {
    const digits = i === 4 || i === 5 ? 2 : 1;
    const red1 = component.red1 !== null ? round(component.red1, digits) : "N/A";
    const red2 = component.red2 !== null ? round(component.red2, digits) : "N/A";
    const red3 = component.red3 !== null ? round(component.red3, digits) : "N/A";
    const redTotal =
      component.redTotal !== null ? round(component.redTotal, digits === 2 ? 2 : 0) : "N/A";
    const redActual = component.redActual !== null ? round(component.redActual, 0) : "N/A";
    const blue1 = component.blue1 !== null ? round(component.blue1, digits) : "N/A";
    const blue2 = component.blue2 !== null ? round(component.blue2, digits) : "N/A";
    const blue3 = component.blue3 !== null ? round(component.blue3, digits) : "N/A";
    const blueTotal =
      component.blueTotal !== null ? round(component.blueTotal, digits === 2 ? 2 : 0) : "N/A";
    const blueActual = component.blueActual !== null ? round(component.blueActual, 0) : "N/A";
    return {
      name: component.name,
      red1,
      red2,
      red3,
      redTotal,
      redActual,
      blue1,
      blue2,
      blue3,
      blueTotal,
      blueActual,
    };
  });

  const MatchTableProps = {
    teams: [red1, red2, red3, blue1, blue2, blue3],
    data: matchData,
    stats: data.year_stats,
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-2">Match Breakdown</p>
      <TableKey />
      <MatchTable {...MatchTableProps} />
    </div>
  );
};

export default PageMatchTable;
