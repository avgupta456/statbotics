import { APIMatch, APITeamMatch } from "../../../../components/types/api";
import { Data } from "./types";

const ctx: Worker = self as unknown as Worker;

const shuffle = (a) => {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

const getTiebreakers = (year: number, match: APIMatch) => {
  // # TODO: remove this once we have stored tiebreakers pre 2023
  if (year === 2016) {
    return [-match.blue_fouls, -match.red_fouls];
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
  } else if (year === 2023) {
    return [match.red_tiebreaker, match.blue_tiebreaker];
  } else {
    return [match.red_score, match.blue_score];
  }
};

const getRandomTiebreaker = (year: number, currArr: number[]) => {
  // roughly MEAN +/- 1 SD
  if (currArr.length < 5) {
    // Use global MEAN and SD
    if (year === 2016) {
      return -Math.round(Math.random() * 10);
    } else if (year === 2017) {
      return 14 + Math.round(Math.random() * 64);
    } else if (year === 2018) {
      return 23 + Math.round(Math.random() * 46);
    } else if (year === 2019) {
      return 9 + Math.round(Math.random() * 20);
    } else if (year === 2020) {
      return 8 + Math.round(Math.random() * 8);
    } else if (year === 2022) {
      return 26 + Math.round(Math.random() * 60);
    } else if (year === 2023) {
      return (Math.random() > 0.9 ? 10000 : 0) + 10 + Math.round(Math.random() * 20);
    } else {
      return 0;
    }
  } else {
    // Use local MEAN and SD
    const arr = currArr.map((a) => a % 10000); // Do not predict any tech fouls
    const mean = arr.map((a) => a % 10000).reduce((a, b) => a + b, 0) / arr.length;
    const std = Math.sqrt(arr.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / arr.length);
    return Math.round(mean + 5 * (Math.random() - 0.5) * std);
  }
};

const getSchedule = async (numTeams: number, numMatches: number) => {
  // TODO: remove this once we have pre-generated schedules for 100+ teams
  if (numTeams > 100) {
    const schedule1 = await getSchedule(100, numMatches);
    let schedule2 = await getSchedule(numTeams - 100, numMatches);
    schedule2 = schedule2.map((match) => {
      return {
        red: match.red.map((team) => team + 100),
        blue: match.blue.map((team) => team + 100),
      };
    });
    return schedule1.concat(schedule2);
  }

  // load csv from external URL using fetch
  return await fetch(
    `https://raw.githubusercontent.com/Team254/cheesy-arena/main/schedules/${numTeams}_${numMatches}.csv`
  )
    .then((response) => response.text())
    .then((data) => {
      const lines = data.split("\n");
      const schedule = [];
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const match = line.split(",");
        if (match.length < 12) {
          continue;
        }
        const red = [parseInt(match[0]), parseInt(match[2]), parseInt(match[4])];
        const blue = [parseInt(match[6]), parseInt(match[8]), parseInt(match[10])];
        schedule.push({ red, blue });
      }
      return schedule;
    });
};

async function preSim(data: Data, simCount: number) {
  const TOTAL_SD = data.year.score_sd;

  const teamsN = data.team_events.length;
  const schedule = await getSchedule(teamsN, 12);

  const currEPAs = {};
  const currRP1EPAs = {};
  const currRP2EPAs = {};

  // Initialize EPAs

  for (let i = 0; i < data.team_events.length; i++) {
    const teamEvent = data.team_events[i];
    currEPAs[teamEvent.num] = teamEvent.start_total_epa;
    currRP1EPAs[teamEvent.num] = teamEvent.start_rp_1_epa;
    currRP2EPAs[teamEvent.num] = teamEvent.start_rp_2_epa;
  }

  // Simulate

  const simRanks = {};
  const simRPs = {};

  for (let i = 0; i < data.team_events.length; i++) {
    const teamEvent = data.team_events[i];
    simRanks[teamEvent.num] = [];
    simRPs[teamEvent.num] = [];
  }

  for (let i = 0; i < simCount; i++) {
    const currSimRPs = {};
    const indexToTeam = {};
    const randArr = shuffle(
      Array(teamsN)
        .fill(0)
        .map((_, i) => i + 1)
    );
    for (let j = 0; j < data.team_events.length; j++) {
      const teamEvent = data.team_events[j];
      indexToTeam[randArr[j]] = teamEvent.num;
      currSimRPs[teamEvent.num] = 0;
    }

    for (let j = 0; j < schedule.length; j++) {
      const match = schedule[j];
      const red = match.red.map((index) => indexToTeam[index]);
      const blue = match.blue.map((index) => indexToTeam[index]);

      let redEPA = currEPAs[red[0]] + currEPAs[red[1]] + currEPAs[red[2]];
      let redRP1EPA = currRP1EPAs[red[0]] + currRP1EPAs[red[1]] + currRP1EPAs[red[2]];
      let redRP2EPA = currRP2EPAs[red[0]] + currRP2EPAs[red[1]] + currRP2EPAs[red[2]];
      let blueEPA = currEPAs[blue[0]] + currEPAs[blue[1]] + currEPAs[blue[2]];
      let blueRP1EPA = currRP1EPAs[blue[0]] + currRP1EPAs[blue[1]] + currRP1EPAs[blue[2]];
      let blueRP2EPA = currRP2EPAs[blue[0]] + currRP2EPAs[blue[1]] + currRP2EPAs[blue[2]];

      const winProb = 1 / (1 + Math.pow(10, ((-5 / 8) * (redEPA - blueEPA)) / TOTAL_SD));
      const redWin = Math.random() < winProb ? 1 : 0;

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

      red.forEach((team) => {
        currSimRPs[team] += redRPs;
      });

      blue.forEach((team) => {
        currSimRPs[team] += blueRPs;
      });
    }

    const simRanksArr = Object.keys(currSimRPs).sort((a, b) => {
      if (currSimRPs[a] === currSimRPs[b]) {
        return Math.random() - 0.5;
      }
      return currSimRPs[b] - currSimRPs[a];
    });

    for (let j = 0; j < data.team_events.length; j++) {
      const teamEvent = data.team_events[j];
      simRanks[teamEvent.num].push(simRanksArr.indexOf(teamEvent.num.toString()) + 1);
      simRPs[teamEvent.num].push(currSimRPs[teamEvent.num]);
    }
  }

  ctx.postMessage({ simRanks, simRPs });
}

async function indexSim(data: Data, index: number, simCount: number) {
  const TOTAL_SD = data.year.score_sd;

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
    currTiebreakers[teamEvent.num] = [];
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
      currEPAs[team] = teamMatch.post_epa ?? teamMatch.total_epa;
      currRP1EPAs[team] = teamMatch.rp_1_epa;
      currRP2EPAs[team] = teamMatch.rp_2_epa;
      currMatches[team] += 1;
      if (
        !match.red_surrogates.includes(team) &&
        !match.blue_surrogates.includes(team) &&
        !match.red_dqs.includes(team) &&
        !match.blue_dqs.includes(team)
      ) {
        currRPs[team] += teamMatch.alliance === "red" ? redRPs : blueRPs;
        currTiebreakers[team].push(teamMatch.alliance === "red" ? redTiebreaker : blueTiebreaker);
      }
    }
  }

  // Simulate

  const simRanks = {};
  const simRPs = {};

  for (let i = 0; i < data.team_events.length; i++) {
    const teamEvent = data.team_events[i];
    simRanks[teamEvent.num] = [];
    simRPs[teamEvent.num] = [];
  }

  for (let i = 0; i < simCount; i++) {
    const currSimRPs = {};
    const currSimTiebreakers = {};
    for (let j = 0; j < data.team_events.length; j++) {
      const teamEvent = data.team_events[j];
      currSimRPs[teamEvent.num] = currRPs[teamEvent.num];
      currSimTiebreakers[teamEvent.num] = [...currTiebreakers[teamEvent.num]];
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
          redEPA += currEPAs[team];
          redRP1EPA += currRP1EPAs[team];
          redRP2EPA += currRP2EPAs[team];
        } else {
          blueEPA += currEPAs[team];
          blueRP1EPA += currRP1EPAs[team];
          blueRP2EPA += currRP2EPAs[team];
        }
      }

      const winProb = 1 / (1 + Math.pow(10, ((-5 / 8) * (redEPA - blueEPA)) / TOTAL_SD));
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
        if (!match.red_surrogates.includes(team) && !match.blue_surrogates.includes(team)) {
          currSimRPs[team] += teamMatch.alliance === "red" ? redRPs : blueRPs;
          currSimTiebreakers[team].push(
            getRandomTiebreaker(data.year.year, currSimTiebreakers[team])
          );
        }
      }
    }

    const simRanksArr = Object.keys(currSimRPs).sort((a, b) => {
      if (currSimRPs[a] === currSimRPs[b]) {
        const tiebreakerA = currSimTiebreakers[a].reduce((x, y) => x + y, 0);
        const tiebreakerB = currSimTiebreakers[b].reduce((x, y) => x + y, 0);
        if (tiebreakerA === tiebreakerB) {
          return Math.random() - 0.5;
        }
        return tiebreakerB - tiebreakerA;
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
    case "preSim":
      preSim(evt.data.data, evt.data.simCount);
      return;
    case "indexSim":
      indexSim(evt.data.data, evt.data.index, evt.data.simCount);
      return;
  }
});

export {};
