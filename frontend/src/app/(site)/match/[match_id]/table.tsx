import React from "react";

import MatchBreakdown from "../../../../components/Table/MatchBreakdown";
import { TableKey } from "../../../../components/Table/shared";
import { RP_KEYS } from "../../../../constants";
import { MatchData } from "../../../../types/data";
import { round } from "../../../../utils";

const RPSigmoid = (x: number) => 1 / (1 + Math.exp(-4 * (x - 0.5)));

const PageMatchTable = ({ data }: { data: MatchData }) => {
  const red1 = data.match.alliances.red.team_keys[0];
  const red2 = data.match.alliances.red.team_keys[1];
  const red3 = data.match.alliances.red.team_keys[2];
  const blue1 = data.match.alliances.blue.team_keys[0];
  const blue2 = data.match.alliances.blue.team_keys[1];
  const blue3 = data.match.alliances.blue.team_keys[2];

  // Used for completed matches
  const red1Data = data.team_matches.find((tm) => tm.team === red1).epa.breakdown;
  const red2Data = data.team_matches.find((tm) => tm.team === red2).epa.breakdown;
  const red3Data = data.team_matches.find((tm) => tm.team === red3).epa.breakdown;
  const blue1Data = data.team_matches.find((tm) => tm.team === blue1).epa.breakdown;
  const blue2Data = data.team_matches.find((tm) => tm.team === blue2).epa.breakdown;
  const blue3Data = data.team_matches.find((tm) => tm.team === blue3).epa.breakdown;

  // Used for upcoming matches
  const red1EventData = data.team_events.find((te) => te.team === red1).epa.breakdown;
  const red2EventData = data.team_events.find((te) => te.team === red2).epa.breakdown;
  const red3EventData = data.team_events.find((te) => te.team === red3).epa.breakdown;
  const blue1EventData = data.team_events.find((te) => te.team === blue1).epa.breakdown;
  const blue2EventData = data.team_events.find((te) => te.team === blue2).epa.breakdown;
  const blue3EventData = data.team_events.find((te) => te.team === blue3).epa.breakdown;

  console.log(red1Data, red1EventData);

  // Used for both upcoming and completed matches
  const redPredTotal = data.match.pred.red_score;
  const bluePredTotal = data.match.pred.blue_score;

  const rp1Key = RP_KEYS[data.year.year][0];
  const rp2Key = RP_KEYS[data.year.year][1];

  const redPredRP1 = data.match.pred[`red_${rp1Key}`];
  const bluePredRP1 = data.match.pred[`blue_${rp1Key}`];
  const redPredRP2 = data.match.pred[`red_${rp2Key}`];
  const bluePredRP2 = data.match.pred[`blue_${rp2Key}`];

  // Used for upcoming events

  const redEventAuto =
    red1EventData.auto_points.mean +
    red2EventData.auto_points.mean +
    red3EventData.auto_points.mean;
  const blueEventAuto =
    blue1EventData.auto_points.mean +
    blue2EventData.auto_points.mean +
    blue3EventData.auto_points.mean;
  const redEventTeleop =
    red1EventData.teleop_points.mean +
    red2EventData.teleop_points.mean +
    red3EventData.teleop_points.mean;
  const blueEventTeleop =
    blue1EventData.teleop_points.mean +
    blue2EventData.teleop_points.mean +
    blue3EventData.teleop_points.mean;
  const redEventEndgame =
    red1EventData.endgame_points.mean +
    red2EventData.endgame_points.mean +
    red3EventData.endgame_points.mean;
  const blueEventEndgame =
    blue1EventData.endgame_points.mean +
    blue2EventData.endgame_points.mean +
    blue3EventData.endgame_points.mean;
  const redEventFouls = redPredTotal - (redEventAuto + redEventTeleop + redEventEndgame);
  const blueEventFouls = bluePredTotal - (blueEventAuto + blueEventTeleop + blueEventEndgame);

  // Used for completed events

  const redMatchAuto = red1Data.auto_points + red2Data.auto_points + red3Data.auto_points;
  const blueMatchAuto = blue1Data.auto_points + blue2Data.auto_points + blue3Data.auto_points;
  const redMatchTeleop = red1Data.teleop_points + red2Data.teleop_points + red3Data.teleop_points;
  const blueMatchTeleop =
    blue1Data.teleop_points + blue2Data.teleop_points + blue3Data.teleop_points;
  const redMatchEndgame =
    red1Data.endgame_points + red2Data.endgame_points + red3Data.endgame_points;
  const blueMatchEndgame =
    blue1Data.endgame_points + blue2Data.endgame_points + blue3Data.endgame_points;
  const redMatchFouls = redPredTotal - (redMatchAuto + redMatchTeleop + redMatchEndgame);
  const blueMatchFouls = bluePredTotal - (blueMatchAuto + blueMatchTeleop + blueMatchEndgame);

  const completed = data.match.status === "Completed";

  const autoComponent = {
    name: "Auto",
    red1: completed ? red1Data.auto_points : red1EventData.auto_points.mean,
    red2: completed ? red2Data.auto_points : red2EventData.auto_points.mean,
    red3: completed ? red3Data.auto_points : red3EventData.auto_points.mean,
    redTotal: completed ? redMatchAuto : redEventAuto,
    redActual: completed ? data.match.result.red_auto_points : null,
    blue1: completed ? blue1Data.auto_points : blue1EventData.auto_points.mean,
    blue2: completed ? blue2Data.auto_points : blue2EventData.auto_points.mean,
    blue3: completed ? blue3Data.auto_points : blue3EventData.auto_points.mean,
    blueTotal: completed ? blueMatchAuto : blueEventAuto,
    blueActual: completed ? data.match.result.blue_auto_points : null,
  };

  const teleopComponent = {
    name: "Teleop",
    red1: completed ? red1Data.teleop_points : red1EventData.teleop_points.mean,
    red2: completed ? red2Data.teleop_points : red2EventData.teleop_points.mean,
    red3: completed ? red3Data.teleop_points : red3EventData.teleop_points.mean,
    redTotal: completed ? redMatchTeleop : redEventTeleop,
    redActual: completed ? data.match.result.red_teleop_points : null,
    blue1: completed ? blue1Data.teleop_points : blue1EventData.teleop_points.mean,
    blue2: completed ? blue2Data.teleop_points : blue2EventData.teleop_points.mean,
    blue3: completed ? blue3Data.teleop_points : blue3EventData.teleop_points.mean,
    blueTotal: completed ? blueMatchTeleop : blueEventTeleop,
    blueActual: completed ? data.match.result.blue_teleop_points : null,
  };

  const endgameComponent = {
    name: "Endgame",
    red1: completed ? red1Data.endgame_points : red1EventData.endgame_points.mean,
    red2: completed ? red2Data.endgame_points : red2EventData.endgame_points.mean,
    red3: completed ? red3Data.endgame_points : red3EventData.endgame_points.mean,
    redTotal: completed ? redMatchEndgame : redEventEndgame,
    redActual: completed ? data.match.result.red_endgame_points : null,
    blue1: completed ? blue1Data.endgame_points : blue1EventData.endgame_points.mean,
    blue2: completed ? blue2Data.endgame_points : blue2EventData.endgame_points.mean,
    blue3: completed ? blue3Data.endgame_points : blue3EventData.endgame_points.mean,
    blueTotal: completed ? blueMatchEndgame : blueEventEndgame,
    blueActual: completed ? data.match.result.blue_endgame_points : null,
  };

  const foulComponent = {
    name: "Fouls",
    red1: null,
    red2: null,
    red3: null,
    redTotal: completed ? redMatchFouls : redEventFouls,
    redActual: completed ? data.match.result.red_score - data.match.result.red_no_foul : null,
    blue1: null,
    blue2: null,
    blue3: null,
    blueTotal: completed ? blueMatchFouls : blueEventFouls,
    blueActual: completed ? data.match.result.blue_score - data.match.result.blue_no_foul : null,
  };

  const rp1Component = {
    name: "RP1",
    red1: completed ? red1Data[rp1Key] : red1EventData[rp1Key].mean,
    red2: completed ? red2Data[rp1Key] : red2EventData[rp1Key].mean,
    red3: completed ? red3Data[rp1Key] : red3EventData[rp1Key].mean,
    redTotal: redPredRP1,
    redActual: completed ? data.match.result[`red_${rp1Key}`] : null,
    blue1: completed ? blue1Data[rp1Key] : blue1EventData[rp1Key].mean,
    blue2: completed ? blue2Data[rp1Key] : blue2EventData[rp1Key].mean,
    blue3: completed ? blue3Data[rp1Key] : blue3EventData[rp1Key].mean,
    blueTotal: bluePredRP1,
    blueActual: completed ? data.match.result[`blue_${rp1Key}`] : null,
  };

  const rp2Component = {
    name: "RP2",
    red1: completed ? red1Data[rp2Key] : red1EventData[rp2Key].mean,
    red2: completed ? red2Data[rp2Key] : red2EventData[rp2Key].mean,
    red3: completed ? red3Data[rp2Key] : red3EventData[rp2Key].mean,
    redTotal: redPredRP2,
    redActual: completed ? data.match.result[`red_${rp1Key}`] : null,
    blue1: completed ? blue1Data[rp2Key] : blue1EventData[rp2Key].mean,
    blue2: completed ? blue2Data[rp2Key] : blue2EventData[rp2Key].mean,
    blue3: completed ? blue3Data[rp2Key] : blue3EventData[rp2Key].mean,
    blueTotal: bluePredRP2,
    blueActual: completed ? data.match.result[`blue_${rp2Key}`] : null,
  };

  const totalComponent = {
    name: "Total",
    red1: completed ? red1Data.total_points : red1EventData.total_points.mean,
    red2: completed ? red2Data.total_points : red2EventData.total_points.mean,
    red3: completed ? red3Data.total_points : red3EventData.total_points.mean,
    redTotal: redPredTotal,
    redActual: completed ? data.match.result.red_score : null,
    blue1: completed ? blue1Data.total_points : blue1EventData.total_points.mean,
    blue2: completed ? blue2Data.total_points : blue2EventData.total_points.mean,
    blue3: completed ? blue3Data.total_points : blue3EventData.total_points.mean,
    blueTotal: bluePredTotal,
    blueActual: completed ? data.match.result.blue_score : null,
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
    const redActual = component.redActual !== null ? round(component.redActual, 0) : "-";
    const blue1 = component.blue1 !== null ? round(component.blue1, digits) : "N/A";
    const blue2 = component.blue2 !== null ? round(component.blue2, digits) : "N/A";
    const blue3 = component.blue3 !== null ? round(component.blue3, digits) : "N/A";
    const blueTotal =
      component.blueTotal !== null ? round(component.blueTotal, digits === 2 ? 2 : 0) : "N/A";
    const blueActual = component.blueActual !== null ? round(component.blueActual, 0) : "-";
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
    stats: data.year,
  };

  return (
    <div className="w-full flex flex-col justify-center items-center">
      <p className="text-2xl lg:text-3xl mt-8 mb-4">Match Breakdown</p>
      <div className="w-full overflow-x-scroll md:overflow-x-auto lg:flex lg:justify-center">
        <MatchBreakdown {...MatchTableProps} />
      </div>
      <TableKey />
    </div>
  );
};

export default PageMatchTable;
