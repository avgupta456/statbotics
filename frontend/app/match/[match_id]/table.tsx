import React from "react";

import MatchTable, { Component } from "../../../components/MatchTable";
import { classnames, round } from "../../../utils";
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

  const autoComponent: Component = {
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

  const teleopComponent: Component = {
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

  const endgameComponent: Component = {
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

  const foulComponent: Component = {
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

  console.log(data.match);

  const rp1Component: Component = {
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

  const rp2Component: Component = {
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

  const totalComponent: Component = {
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

  console.log(rp1Component);
  console.log(rp2Component);

  const matchPredictionData = [
    autoComponent,
    teleopComponent,
    endgameComponent,
    foulComponent,
    rp1Component,
    rp2Component,
    totalComponent,
  ].map((component, i) => {
    const digits = i === 4 || i === 5 ? 2 : 1;
    const red1 = component.red1 !== null ? round(component.red1, digits) : null;
    const red2 = component.red2 !== null ? round(component.red2, digits) : null;
    const red3 = component.red3 !== null ? round(component.red3, digits) : null;
    const redTotal =
      component.redTotal !== null
        ? round(component.redTotal, digits === 2 ? 2 : 0)
        : null;
    const redActual =
      component.redActual !== null ? round(component.redActual, 0) : null;
    const blue1 =
      component.blue1 !== null ? round(component.blue1, digits) : null;
    const blue2 =
      component.blue2 !== null ? round(component.blue2, digits) : null;
    const blue3 =
      component.blue3 !== null ? round(component.blue3, digits) : null;
    const blueTotal =
      component.blueTotal !== null
        ? round(component.blueTotal, digits === 2 ? 2 : 0)
        : null;
    const blueActual =
      component.blueActual !== null ? round(component.blueActual, 0) : null;
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

  const MatchPredictionTableProps = {
    teams: [red1, red2, red3, blue1, blue2, blue3],
    data: matchPredictionData,
    stats: data.year_stats,
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-4">Match Breakdown</p>
      <MatchTable {...MatchPredictionTableProps} />
    </div>
  );
};

export const TableKey = () => (
  <>
    <div className="w-full flex justify-center items-center text-xs mt-8">
      <p className="text-sm">Key (Multiples of Mean):</p>
      {[
        { color: "text-red-700 bg-red-300", text: "< 0.5" },
        {
          color: "text-gray-800 bg-gray-200",
          text: "0.5 - 1.5",
        },
        { color: "text-green-500 bg-green-100", text: "1.5 - 2" },
        { color: "text-green-700 bg-green-300", text: "2 - 3" },
        { color: "text-black bg-green-500", text: "3 - 4" },
        { color: "text-blue-500 bg-blue-100", text: "4 - 5" },
        { color: "text-blue-700 bg-blue-300", text: "5 - 6" },
        { color: "text-white bg-blue-500", text: "6+" },
      ].map((item) => (
        <span
          key={item.color}
          className={classnames(
            item.color,
            "data w-16 p-1 ml-4 rounded lg:rounded-lg flex justify-center items-center"
          )}
        >
          {item.text}
        </span>
      ))}
    </div>
    <div className="hidden lg:flex w-full justify-center items-center text-sm mt-4">
      Note: Nonlinear sum for alliance component predictions, see docs for more
      details!
    </div>
  </>
);

export default PageMatchTable;
