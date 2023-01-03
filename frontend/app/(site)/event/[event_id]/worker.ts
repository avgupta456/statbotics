import { APIMatch, APITeamMatch } from "../../../../components/types/api";
import { Data } from "./types";

const ctx: Worker = self as unknown as Worker;

const getTiebreakers = (year: number, match: APIMatch) => {
  if (year === 2016) {
    return [match.red_1, match.blue_1];
  } else if (year === 2017) {
    return [match.red_auto, match.blue_auto];
  } else if (year === 2018) {
    return [match.red_endgame, match.blue_endgame];
  } else if (year === 2019) {
    return [match.red_2, match.blue_2];
  } else if (year === 2020) {
    return [match.red_auto, match.blue_auto];
  } else if (year === 2022) {
    return [match.red_score, match.blue_score];
  } else {
    return [match.red_score, match.blue_score];
  }
};

async function indexSim(data: Data, index: number, simCount: number) {
  const TOTAL_SD = data.year.total_stats.sd;

  const qualMatches = data.matches
    .filter((match) => !match.playoff)
    .sort((a, b) => a.match_number - b.match_number);
  const qualTeamMatches = data.team_matches.filter((match) => !match.playoff);
  const qualN = qualMatches.length;

  const currEPAs = {};
  const currRP1EPAs = {};
  const currRP2EPAs = {};
  const currMatches = {};
  const currRPs = {};
  const currTiebreakers = {};

  const teamMatchesMap: { [key: string]: APITeamMatch[] } = {};
  for (let i = 0; i < qualTeamMatches.length; i++) {
    const teamMatch = qualTeamMatches[i];
    if (!teamMatchesMap[teamMatch.match]) {
      teamMatchesMap[teamMatch.match] = [];
    }
    teamMatchesMap[teamMatch.match].push(teamMatch);
  }

  // Initialize EPAs

  for (let i = 0; i < data.team_events.length; i++) {
    const teamEvent = data.team_events[i];
    currEPAs[teamEvent.num] = teamEvent.start_total_epa;
    currRP1EPAs[teamEvent.num] = teamEvent.start_rp_1_epa;
    currRP2EPAs[teamEvent.num] = teamEvent.start_rp_2_epa;
    currMatches[teamEvent.num] = 0;
    currRPs[teamEvent.num] = 0;
    currTiebreakers[teamEvent.num] = 0;
  }

  const redResultToRPs = { red: 2, draw: 1, blue: 0 };
  const blueResultToRPs = { red: 0, draw: 1, blue: 2 };
  for (let i = 0; i < index; i++) {
    const match = qualMatches[i];
    const redRPs = match.red_rp_1 + match.red_rp_2 + redResultToRPs[match.winner];
    const blueRPs = match.blue_rp_1 + match.blue_rp_2 + blueResultToRPs[match.winner];
    const [redTiebreaker, blueTiebreaker] = getTiebreakers(data.event.year, match);

    const teamMatches = teamMatchesMap[match.key];
    for (let j = 0; j < teamMatches.length; j++) {
      const teamMatch = teamMatches[j];
      const team = teamMatch.num;
      currEPAs[team] = teamMatch.total_epa;
      currRP1EPAs[team] = teamMatch.rp_1_epa;
      currRP2EPAs[team] = teamMatch.rp_2_epa;
      currMatches[team] += 1;
      currRPs[team] += teamMatch.alliance === "red" ? redRPs : blueRPs;
      currTiebreakers[team] += teamMatch.alliance === "red" ? redTiebreaker : blueTiebreaker;
    }
  }

  for (let i = 0; i < data.team_events.length; i++) {
    const num = data.team_events[i].num;
    currTiebreakers[num] /= currMatches[num];
  }

  // Simulate

  const simRanks = {};
  const simRPs = {};

  for (let i = 0; i < data.team_events.length; i++) {
    const teamEvent = data.team_events[i];
    simRanks[teamEvent.num] = [];
    simRPs[teamEvent.num] = [];
  }

  const jitterPercent = 0.4;
  for (let i = 0; i < simCount; i++) {
    // Jitter EPAs by plus or minus 20%
    const currSimEPAs = {};
    const currSimRP1EPAs = {};
    const currSimRP2EPAs = {};
    for (let j = 0; j < data.team_events.length; j++) {
      const team = data.team_events[j].num;
      currSimEPAs[team] = currEPAs[team] * (1 + jitterPercent * (Math.random() - 0.5));
      currSimRP1EPAs[team] = currRP1EPAs[team] * (1 + jitterPercent * (Math.random() - 0.5));
      currSimRP2EPAs[team] = currRP2EPAs[team] * (1 + jitterPercent * (Math.random() - 0.5));
    }

    const currSimRPs = {};
    for (let j = 0; j < data.team_events.length; j++) {
      const teamEvent = data.team_events[j];
      currSimRPs[teamEvent.num] = currRPs[teamEvent.num];
    }

    for (let j = index; j < qualN; j++) {
      const match = qualMatches[j];
      let redEPA = 0;
      let redRP1EPA = 0;
      let redRP2EPA = 0;
      let blueEPA = 0;
      let blueRP1EPA = 0;
      let blueRP2EPA = 0;
      const teamMatches = teamMatchesMap[match.key];
      for (let k = 0; k < teamMatches.length; k++) {
        const teamMatch = teamMatches[k];
        const team = teamMatch.num;
        if (teamMatch.alliance === "red") {
          redEPA += currSimEPAs[team];
          redRP1EPA += currSimRP1EPAs[team];
          redRP2EPA += currSimRP2EPAs[team];
        } else {
          blueEPA += currSimEPAs[team];
          blueRP1EPA += currSimRP1EPAs[team];
          blueRP2EPA += currSimRP2EPAs[team];
        }
      }

      // Normally K=-5/8, but we use -5/12 since simulating multiple matches ahead
      const winProb = 1 / (1 + Math.pow(10, ((-5 / 12) * (redEPA - blueEPA)) / TOTAL_SD));
      const redWin = Math.random() < winProb;

      const redRP1Prob = 1 / (1 + Math.pow(Math.E, -4 * (redRP1EPA - 0.5)));
      const redRP1 = Math.random() < redRP1Prob ? 1 : 0;

      const redRP2Prob = 1 / (1 + Math.pow(Math.E, -4 * (redRP2EPA - 0.5)));
      const redRP2 = Math.random() < redRP2Prob ? 1 : 0;

      const blueRP1Prob = 1 / (1 + Math.pow(Math.E, -4 * (blueRP1EPA - 0.5)));
      const blueRP1 = Math.random() < blueRP1Prob ? 1 : 0;

      const blueRP2Prob = 1 / (1 + Math.pow(Math.E, -4 * (blueRP2EPA - 0.5)));
      const blueRP2 = Math.random() < blueRP2Prob ? 1 : 0;

      const redRPs = redRP1 + redRP2 + (redWin ? 2 : 0);
      const blueRPs = blueRP1 + blueRP2 + (redWin ? 0 : 2);

      for (let k = 0; k < teamMatches.length; k++) {
        const teamMatch = teamMatches[k];
        const team = teamMatch.num;
        if (teamMatch.alliance === "red") {
          currSimRPs[team] += redRPs;
        } else {
          currSimRPs[team] += blueRPs;
        }
      }
    }

    const simRanksArr = Object.keys(currSimRPs).sort((a, b) => {
      if (currSimRPs[a] === currSimRPs[b]) {
        if (currTiebreakers[a] === currTiebreakers[b]) {
          return Math.random() - 0.5;
        }
        return currTiebreakers[b] - currTiebreakers[a];
      }
      return currSimRPs[b] - currSimRPs[a];
    });

    for (let j = 0; j < data.team_events.length; j++) {
      const teamEvent = data.team_events[j];
      simRanks[teamEvent.num].push(simRanksArr.indexOf(teamEvent.num.toString()) + 1);
      simRPs[teamEvent.num].push(currSimRPs[teamEvent.num]);
    }
  }

  ctx.postMessage({ index, simRanks, simRPs });
}

ctx.addEventListener("message", (evt) => {
  switch (evt.data.type) {
    case "indexSim":
      indexSim(evt.data.data, evt.data.index, evt.data.simCount);
      return;
  }
});

export {};
