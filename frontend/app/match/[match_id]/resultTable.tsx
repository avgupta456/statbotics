import React from "react";

import MatchResultTable, {
  ResultComponent,
} from "../../../components/MatchResultTable";
import { Data } from "./types";
import { round } from "../../../utils";

const ResultTable = ({ data }: { data: Data }) => {
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

  const autoResultComponent: ResultComponent = {
    name: "Auto",
    redPred: red1Data.auto_epa + red2Data.auto_epa + red3Data.auto_epa,
    redActual: data.match.red_auto,
    bluePred: blue1Data.auto_epa + blue2Data.auto_epa + blue3Data.auto_epa,
    blueActual: data.match.blue_auto,
  };

  const teleopResultComponent: ResultComponent = {
    name: "Teleop",
    redPred: red1Data.teleop_epa + red2Data.teleop_epa + red3Data.teleop_epa,
    redActual: data.match.red_teleop,
    bluePred:
      blue1Data.teleop_epa + blue2Data.teleop_epa + blue3Data.teleop_epa,
    blueActual: data.match.blue_teleop,
  };

  const endgameResultComponent: ResultComponent = {
    name: "Endgame",
    redPred: red1Data.endgame_epa + red2Data.endgame_epa + red3Data.endgame_epa,
    redActual: data.match.red_endgame,
    bluePred:
      blue1Data.endgame_epa + blue2Data.endgame_epa + blue3Data.endgame_epa,
    blueActual: data.match.blue_endgame,
  };

  const foulResultComponent: ResultComponent = {
    name: "Fouls",
    redPred: 0,
    redActual: data.match.red_fouls,
    bluePred: 0,
    blueActual: data.match.blue_fouls,
  };

  const rp1ResultComponent: ResultComponent = {
    name: "RP1",
    redPred: null,
    redActual: data.match.red_rp1,
    bluePred: null,
    blueActual: data.match.blue_rp1,
  };

  const rp2ResultComponent: ResultComponent = {
    name: "RP2",
    redPred: null,
    redActual: data.match.red_rp2,
    bluePred: null,
    blueActual: data.match.blue_rp2,
  };

  const totalResultComponent: ResultComponent = {
    name: "Total",
    redPred: red1Data.epa + red2Data.epa + red3Data.epa,
    redActual: data.match.red_score,
    bluePred: blue1Data.epa + blue2Data.epa + blue3Data.epa,
    blueActual: data.match.blue_score,
  };

  const matchResultData = [
    autoResultComponent,
    teleopResultComponent,
    endgameResultComponent,
    foulResultComponent,
    rp1ResultComponent,
    rp2ResultComponent,
    totalResultComponent,
  ].map((component) => {
    const redPred =
      component.redPred !== null ? round(component.redPred) : null;
    const redActual =
      component.redActual !== null ? round(component.redActual) : null;
    const bluePred =
      component.bluePred !== null ? round(component.bluePred) : null;
    const blueActual =
      component.blueActual !== null ? round(component.blueActual) : null;
    return {
      name: component.name,
      redPred,
      redActual,
      bluePred,
      blueActual,
    };
  });

  const MatchResultTableProps = {
    data: matchResultData,
    stats: data.year_stats,
  };

  return (
    <div className="w-full lg:w-1/2 flex justify-center items-center">
      <MatchResultTable {...MatchResultTableProps} />
    </div>
  );
};

export default ResultTable;
