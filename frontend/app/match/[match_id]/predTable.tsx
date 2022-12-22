import React from "react";

import MatchPredictionTable, {
  PredComponent,
} from "../../../components/MatchPredictionTable";
import { round } from "../../../utils";
import { Data } from "./types";

const PredTable = ({ data }: { data: Data }) => {
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

  const autoPredComponent: PredComponent = {
    name: "Auto",
    red1: red1Data.auto_epa,
    red2: red2Data.auto_epa,
    red3: red3Data.auto_epa,
    redTotal: red1Data.auto_epa + red2Data.auto_epa + red3Data.auto_epa,
    blue1: blue1Data.auto_epa,
    blue2: blue2Data.auto_epa,
    blue3: blue3Data.auto_epa,
    blueTotal: blue1Data.auto_epa + blue2Data.auto_epa + blue3Data.auto_epa,
  };

  const teleopPredComponent: PredComponent = {
    name: "Teleop",
    red1: red1Data.teleop_epa,
    red2: red2Data.teleop_epa,
    red3: red3Data.teleop_epa,
    redTotal: red1Data.teleop_epa + red2Data.teleop_epa + red3Data.teleop_epa,
    blue1: blue1Data.teleop_epa,
    blue2: blue2Data.teleop_epa,
    blue3: blue3Data.teleop_epa,
    blueTotal:
      blue1Data.teleop_epa + blue2Data.teleop_epa + blue3Data.teleop_epa,
  };

  const endgamePredComponent: PredComponent = {
    name: "Endgame",
    red1: red1Data.endgame_epa,
    red2: red2Data.endgame_epa,
    red3: red3Data.endgame_epa,
    redTotal:
      red1Data.endgame_epa + red2Data.endgame_epa + red3Data.endgame_epa,
    blue1: blue1Data.endgame_epa,
    blue2: blue2Data.endgame_epa,
    blue3: blue3Data.endgame_epa,
    blueTotal:
      blue1Data.endgame_epa + blue2Data.endgame_epa + blue3Data.endgame_epa,
  };

  const foulPredComponent: PredComponent = {
    name: "Fouls",
    red1: 0,
    red2: 0,
    red3: 0,
    redTotal: 0,
    blue1: 0,
    blue2: 0,
    blue3: 0,
    blueTotal: 0,
  };

  const rp1PredComponent: PredComponent = {
    name: "RP1",
    red1: null,
    red2: null,
    red3: null,
    redTotal: null,
    blue1: null,
    blue2: null,
    blue3: null,
    blueTotal: null,
  };

  const rp2PredComponent: PredComponent = {
    name: "RP2",
    red1: null,
    red2: null,
    red3: null,
    redTotal: null,
    blue1: null,
    blue2: null,
    blue3: null,
    blueTotal: null,
  };

  const totalPredComponent: PredComponent = {
    name: "Total",
    red1: red1Data.epa,
    red2: red2Data.epa,
    red3: red3Data.epa,
    redTotal: red1Data.epa + red2Data.epa + red3Data.epa,
    blue1: blue1Data.epa,
    blue2: blue2Data.epa,
    blue3: blue3Data.epa,
    blueTotal: blue1Data.epa + blue2Data.epa + blue3Data.epa,
  };

  const matchPredictionData = [
    autoPredComponent,
    teleopPredComponent,
    endgamePredComponent,
    foulPredComponent,
    rp1PredComponent,
    rp2PredComponent,
    totalPredComponent,
  ].map((component) => {
    const red1 = component.red1 !== null ? round(component.red1) : null;
    const red2 = component.red2 !== null ? round(component.red2) : null;
    const red3 = component.red3 !== null ? round(component.red3) : null;
    const redTotal =
      component.redTotal !== null ? round(component.redTotal, 0) : null;
    const blue1 = component.blue1 !== null ? round(component.blue1) : null;
    const blue2 = component.blue2 !== null ? round(component.blue2) : null;
    const blue3 = component.blue3 !== null ? round(component.blue3) : null;
    const blueTotal =
      component.blueTotal !== null ? round(component.blueTotal, 0) : null;
    return {
      name: component.name,
      red1,
      red2,
      red3,
      redTotal,
      blue1,
      blue2,
      blue3,
      blueTotal,
    };
  });

  const MatchPredictionTableProps = {
    teams: [red1, red2, red3, blue1, blue2, blue3],
    data: matchPredictionData,
    stats: data.year_stats,
  };

  return (
    <div className="w-full lg:w-1/2 flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-4">Predictions</p>
      <MatchPredictionTable {...MatchPredictionTableProps} />
    </div>
  );
};

export default PredTable;
