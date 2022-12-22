import { match } from "assert";
import React from "react";

import MatchPredictionTable, {
  PredComponent,
} from "../../../components/MatchPredictionTable";
import MatchResultTable, {
  ResultComponent,
} from "../../../components/MatchResultTable";
import PieChart from "../../../components/Pie";
import { RED, BLUE } from "../../../constants";
import { classnames } from "../../../utils";

async function getData(match_id: string) {
  const res = await fetch("http://localhost:8000/api/match/" + match_id);
  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

async function Match({ params }: { params: { match_id: string } }) {
  const { match_id } = params;
  console.log("Fetching match data for match_id: " + match_id);
  const start = performance.now();
  const data = await getData(match_id);
  console.log(
    "Fetched match data for match_id: " +
      match_id +
      ". Took " +
      Math.round(performance.now() - start) +
      "ms"
  );

  if (!data) {
    return <div>Match not found</div>;
  }

  let truncatedEventName = data.event_name;
  if (data.event_name.length > 30) {
    truncatedEventName = data.event_name.slice(0, 27) + "...";
  }

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

  // Match Prediction Table
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

  const round = (num: number, digits: number = 1) => {
    const factor = 10 ** digits;
    return Math.round(num * factor) / factor;
  };
  const matchPredictionData = [
    autoPredComponent,
    teleopPredComponent,
    endgamePredComponent,
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

  const winProb = data.match.epa_win_prob;
  const redWinProb = winProb * 100;
  const blueWinProb = (1 - winProb) * 100;

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
    <div className="w-full h-full p-4">
      <div className="container mx-auto">
        <div className="flex flex-row items-end mb-4">
          <p className="text-3xl lg:text-4xl">{data.match_name}</p>
          <a
            href={`/event/${data.match.event}`}
            target="_blank"
            rel="noopener noreferrer"
            className="lg:text-2xl ml-2 text-blue-500 hover:text-blue-600 cursor-pointer underline"
          >
            {truncatedEventName}
          </a>
        </div>
        <p className="text-2xl lg:text-3xl mt-8 mb-4">Predictions</p>
        <div className="w-full flex flex-row flex-wrap">
          <div className="w-full lg:w-1/2 flex justify-center items-center">
            <MatchPredictionTable {...MatchPredictionTableProps} />
          </div>
          <div className="w-full lg:w-1/2 flex flex-row flex-wrap">
            <div className="w-full lg:w-1/2 h-full flex flex-col justify-around">
              <div className="w-full flex flex-col items-center">
                <div className="flex text-3xl">
                  <p
                    className={classnames(
                      "data text-red-500",
                      data.match.red_epa_sum > data.match.blue_epa_sum
                        ? "font-bold"
                        : ""
                    )}
                  >
                    {Math.round(data.match.red_epa_sum)}
                  </p>
                  <p className="mx-2">-</p>
                  <p
                    className={classnames(
                      "data text-blue-500",
                      data.match.blue_epa_sum > data.match.red_epa_sum
                        ? "font-bold"
                        : ""
                    )}
                  >
                    {Math.round(data.match.blue_epa_sum)}
                  </p>
                </div>
                <div className="mt-4 text-lg flex">
                  Projected Winner:{" "}
                  <p
                    className={classnames(
                      "ml-2",
                      data.match.epa_winner === "red"
                        ? "text-red-500"
                        : "text-blue-500"
                    )}
                  >
                    {data.match.epa_winner.toUpperCase()}
                  </p>
                </div>
              </div>
              <div className="w-full flex flex-col items-center">
                <div className="flex text-3xl">
                  <p
                    className={classnames(
                      "data text-red-500",
                      data.match.red_score > data.match.blue_score
                        ? "font-bold"
                        : ""
                    )}
                  >
                    {Math.round(data.match.red_score)}
                  </p>
                  <p className="mx-2">-</p>
                  <p
                    className={classnames(
                      "data text-blue-500",
                      data.match.blue_score > data.match.red_score
                        ? "font-bold"
                        : ""
                    )}
                  >
                    {Math.round(data.match.blue_score)}
                  </p>
                </div>
                <div className="mt-4 text-lg flex">
                  Actual Winner:{" "}
                  <p
                    className={classnames(
                      "ml-2",
                      data.match.winner === "red"
                        ? "text-red-500"
                        : "text-blue-500"
                    )}
                  >
                    {data.match.winner.toUpperCase()}
                  </p>
                </div>
              </div>
            </div>
            <div className="w-full lg:w-1/2 h-full flex flex-col justify-center items-center">
              <PieChart
                data={[
                  {
                    title: "Red",
                    value: redWinProb,
                    label: `${Math.round(redWinProb)}%`,
                  },
                  {
                    title: "Blue",
                    value: blueWinProb,
                    label: `${Math.round(blueWinProb)}%`,
                  },
                ]}
                colors={[RED, BLUE]}
              />
              <div className="text-lg">Win Probability</div>
            </div>
          </div>
        </div>
        <p className="text-2xl lg:text-3xl mt-8 mb-4">Results</p>
        <div className="w-full flex flex-row flex-wrap">
          <div className="w-full lg:w-1/2 flex justify-center items-center">
            <MatchResultTable {...MatchResultTableProps} />
          </div>
          <div className="w-full lg:w-1/2">
            <div className="relative pb-[56.25%]">
              <iframe
                className="absolute top-0 left-0 w-full h-full"
                src={`https://www.youtube.com/embed/${data.match.video}`}
                title="YouTube video player"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Match;
