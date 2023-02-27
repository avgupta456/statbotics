import React from "react";

import MatchBreakdown from "../../../../components/Table/MatchBreakdown";
import { TableKey } from "../../../../components/Table/shared";
import { round } from "../../../../utils";
import { Data } from "./types";

const RPSigmoid = (x: number) => 1 / (1 + Math.exp(-4 * (x - 0.5)));

const PageMatchTable = ({ data }: { data: Data }) => {
  const red1 = data.match.red[0];
  const red2 = data.match.red[1];
  const red3 = data.match.red[2];
  const blue1 = data.match.blue[0];
  const blue2 = data.match.blue[1];
  const blue3 = data.match.blue[2];

  // Used for completed matches
  const red1Data = data.team_matches.find((teamMatch) => teamMatch.num === red1);
  const red2Data = data.team_matches.find((teamMatch) => teamMatch.num === red2);
  const red3Data = data.team_matches.find((teamMatch) => teamMatch.num === red3);
  const blue1Data = data.team_matches.find((teamMatch) => teamMatch.num === blue1);
  const blue2Data = data.team_matches.find((teamMatch) => teamMatch.num === blue2);
  const blue3Data = data.team_matches.find((teamMatch) => teamMatch.num === blue3);

  // Used for upcoming matches
  const red1EventData = data.team_events.find((teamEvent) => teamEvent.num === red1);
  const red2EventData = data.team_events.find((teamEvent) => teamEvent.num === red2);
  const red3EventData = data.team_events.find((teamEvent) => teamEvent.num === red3);
  const blue1EventData = data.team_events.find((teamEvent) => teamEvent.num === blue1);
  const blue2EventData = data.team_events.find((teamEvent) => teamEvent.num === blue2);
  const blue3EventData = data.team_events.find((teamEvent) => teamEvent.num === blue3);

  // Used for both upcoming and completed matches
  const redFouls = data.match.red_epa_pred * data.year.foul_rate;
  const blueFouls = data.match.blue_epa_pred * data.year.foul_rate;

  const redEventAuto = red1EventData.auto_epa + red2EventData.auto_epa + red3EventData.auto_epa;
  const blueEventAuto = blue1EventData.auto_epa + blue2EventData.auto_epa + blue3EventData.auto_epa;
  const redEventTeleop =
    red1EventData.teleop_epa + red2EventData.teleop_epa + red3EventData.teleop_epa;
  const blueEventTeleop =
    blue1EventData.teleop_epa + blue2EventData.teleop_epa + blue3EventData.teleop_epa;
  const redEventEndgame =
    red1EventData.endgame_epa + red2EventData.endgame_epa + red3EventData.endgame_epa;
  const blueEventEndgame =
    blue1EventData.endgame_epa + blue2EventData.endgame_epa + blue3EventData.endgame_epa;
  const redEventRP1 = red1EventData.rp_1_epa + red2EventData.rp_1_epa + red3EventData.rp_1_epa;
  const blueEventRP1 = blue1EventData.rp_1_epa + blue2EventData.rp_1_epa + blue3EventData.rp_1_epa;
  const redEventRP2 = red1EventData.rp_2_epa + red2EventData.rp_2_epa + red3EventData.rp_2_epa;
  const blueEventRP2 = blue1EventData.rp_2_epa + blue2EventData.rp_2_epa + blue3EventData.rp_2_epa;
  const redEventTotal = redEventAuto + redEventTeleop + redEventEndgame + redFouls;
  const blueEventTotal = blueEventAuto + blueEventTeleop + blueEventEndgame + blueFouls;

  const completed = data.match.status === "Completed";

  const autoComponent = {
    name: "Auto",
    red1: completed ? red1Data.auto_epa : red1EventData.auto_epa,
    red2: completed ? red2Data.auto_epa : red2EventData.auto_epa,
    red3: completed ? red3Data.auto_epa : red3EventData.auto_epa,
    redTotal: completed ? data.match.red_auto_epa_pred : redEventAuto,
    redActual: completed ? data.match.red_auto : null,
    blue1: completed ? blue1Data.auto_epa : blue1EventData.auto_epa,
    blue2: completed ? blue2Data.auto_epa : blue2EventData.auto_epa,
    blue3: completed ? blue3Data.auto_epa : blue3EventData.auto_epa,
    blueTotal: completed ? data.match.blue_auto_epa_pred : blueEventAuto,
    blueActual: completed ? data.match.blue_auto : null,
  };

  const teleopComponent = {
    name: "Teleop",
    red1: completed ? red1Data.teleop_epa : red1EventData.teleop_epa,
    red2: completed ? red2Data.teleop_epa : red2EventData.teleop_epa,
    red3: completed ? red3Data.teleop_epa : red3EventData.teleop_epa,
    redTotal: completed ? data.match.red_teleop_epa_pred : redEventTeleop,
    redActual: completed ? data.match.red_teleop : null,
    blue1: completed ? blue1Data.teleop_epa : blue1EventData.teleop_epa,
    blue2: completed ? blue2Data.teleop_epa : blue2EventData.teleop_epa,
    blue3: completed ? blue3Data.teleop_epa : blue3EventData.teleop_epa,
    blueTotal: completed ? data.match.blue_teleop_epa_pred : blueEventTeleop,
    blueActual: completed ? data.match.blue_teleop : null,
  };

  const endgameComponent = {
    name: "Endgame",
    red1: completed ? red1Data.endgame_epa : red1EventData.endgame_epa,
    red2: completed ? red2Data.endgame_epa : red2EventData.endgame_epa,
    red3: completed ? red3Data.endgame_epa : red3EventData.endgame_epa,
    redTotal: completed ? data.match.red_endgame_epa_pred : redEventEndgame,
    redActual: completed ? data.match.red_endgame : null,
    blue1: completed ? blue1Data.endgame_epa : blue1EventData.endgame_epa,
    blue2: completed ? blue2Data.endgame_epa : blue2EventData.endgame_epa,
    blue3: completed ? blue3Data.endgame_epa : blue3EventData.endgame_epa,
    blueTotal: completed ? data.match.blue_endgame_epa_pred : blueEventEndgame,
    blueActual: completed ? data.match.blue_endgame : null,
  };

  const foulComponent = {
    name: "Fouls",
    red1: null,
    red2: null,
    red3: null,
    redTotal: redFouls,
    redActual: completed ? data.match.red_fouls : null,
    blue1: null,
    blue2: null,
    blue3: null,
    blueTotal: blueFouls,
    blueActual: completed ? data.match.blue_fouls : null,
  };

  const rp1Component = {
    name: "RP1",
    red1: completed ? red1Data.rp_1_epa : red1EventData.rp_1_epa,
    red2: completed ? red2Data.rp_1_epa : red2EventData.rp_1_epa,
    red3: completed ? red3Data.rp_1_epa : red3EventData.rp_1_epa,
    redTotal: completed ? RPSigmoid(data.match.red_rp_1_pred) : RPSigmoid(redEventRP1),
    redActual: completed ? data.match.red_rp_1 : null,
    blue1: completed ? blue1Data.rp_1_epa : blue1EventData.rp_1_epa,
    blue2: completed ? blue2Data.rp_1_epa : blue2EventData.rp_1_epa,
    blue3: completed ? blue3Data.rp_1_epa : blue3EventData.rp_1_epa,
    blueTotal: completed ? RPSigmoid(data.match.blue_rp_1_pred) : RPSigmoid(blueEventRP1),
    blueActual: completed ? data.match.blue_rp_1 : null,
  };

  const rp2Component = {
    name: "RP2",
    red1: completed ? red1Data.rp_2_epa : red1EventData.rp_2_epa,
    red2: completed ? red2Data.rp_2_epa : red2EventData.rp_2_epa,
    red3: completed ? red3Data.rp_2_epa : red3EventData.rp_2_epa,
    redTotal: completed ? RPSigmoid(data.match.red_rp_2_pred) : RPSigmoid(redEventRP2),
    redActual: completed ? data.match.red_rp_2 : null,
    blue1: completed ? blue1Data.rp_2_epa : blue1EventData.rp_2_epa,
    blue2: completed ? blue2Data.rp_2_epa : blue2EventData.rp_2_epa,
    blue3: completed ? blue3Data.rp_2_epa : blue3EventData.rp_2_epa,
    blueTotal: completed ? RPSigmoid(data.match.blue_rp_2_pred) : RPSigmoid(blueEventRP2),
    blueActual: completed ? data.match.blue_rp_2 : null,
  };

  const totalComponent = {
    name: "Total",
    red1: completed ? red1Data.total_epa : red1EventData.total_epa,
    red2: completed ? red2Data.total_epa : red2EventData.total_epa,
    red3: completed ? red3Data.total_epa : red3EventData.total_epa,
    redTotal: completed ? data.match.red_epa_pred + redFouls : redEventTotal,
    redActual: completed ? data.match.red_score : null,
    blue1: completed ? blue1Data.total_epa : blue1EventData.total_epa,
    blue2: completed ? blue2Data.total_epa : blue2EventData.total_epa,
    blue3: completed ? blue3Data.total_epa : blue3EventData.total_epa,
    blueTotal: completed ? data.match.blue_epa_pred + blueFouls : blueEventTotal,
    blueActual: completed ? data.match.blue_score : null,
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
      <div className="w-full overflow-x-scroll md:overflow-x-auto md:flex md:justify-center">
        <MatchBreakdown {...MatchTableProps} />
      </div>
      <TableKey />
    </div>
  );
};

export default PageMatchTable;
