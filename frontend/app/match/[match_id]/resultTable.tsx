import React from "react";

import MatchResultTable, {
  ResultComponent,
} from "../../../components/MatchResultTable";
import { Data } from "./types";
import { round } from "../../../utils";

const ResultTable = ({ data }: { data: Data }) => {
  const autoResultComponent: ResultComponent = {
    name: "Auto",
    redPred: data.match.red_auto_epa_sum,
    redActual: data.match.red_auto,
    bluePred: data.match.blue_auto_epa_sum,
    blueActual: data.match.blue_auto,
  };

  const teleopResultComponent: ResultComponent = {
    name: "Teleop",
    redPred: data.match.red_teleop_epa_sum,
    redActual: data.match.red_teleop,
    bluePred: data.match.blue_teleop_epa_sum,
    blueActual: data.match.blue_teleop,
  };

  const endgameResultComponent: ResultComponent = {
    name: "Endgame",
    redPred: data.match.red_endgame_epa_sum,
    redActual: data.match.red_endgame,
    bluePred: data.match.blue_endgame_epa_sum,
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
    redPred: data.match.red_epa_sum,
    redActual: data.match.red_score,
    bluePred: data.match.blue_epa_sum,
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
      component.redPred !== null ? round(component.redPred, 0) : null;
    const redActual =
      component.redActual !== null ? round(component.redActual) : null;
    const bluePred =
      component.bluePred !== null ? round(component.bluePred, 0) : null;
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
    <div className="w-full lg:w-1/2 flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-4">Results</p>
      <MatchResultTable {...MatchResultTableProps} />
    </div>
  );
};

export default ResultTable;
