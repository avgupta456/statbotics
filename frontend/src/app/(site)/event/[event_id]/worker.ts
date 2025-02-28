import Gaussian from "gaussian";

import { APIMatch, APITeamMatch } from "../../../../types/api";
import { EventData } from "../../../../types/data";

const ctx: Worker = self as unknown as Worker;

const shuffle = (a) => {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

const getTiebreakers = (year: number, match: APIMatch) => {
  return [match.result.red_tiebreaker, match.result.blue_tiebreaker];
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
    } else if (year === 2024) {
      return 45 + Math.round(Math.random() * 20);
    } else if (year === 2025) {
      // TODO: Replace with mean/sd after week 1
      return 45 + Math.round(Math.random() * 20);
    } else {
      return 0;
    }
  } else {
    // Use local MEAN and SD
    const arr = currArr.map((a) => a % 10000); // Do not predict any tech fouls
    const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
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

const getRPProb = (rpEPA) => 1 / (1 + Math.pow(Math.E, -4 * (rpEPA - 0.5)));

async function preSim(
  data: EventData,
  simCount: number,
  numMatches: number,
  postEvent: boolean,
  postMessage: boolean
) {
  const TOTAL_SD = data.year.score_sd;
  const yearNum = data.year.year;

  const teamsN = data.team_events.length;
  const schedule = await getSchedule(teamsN, numMatches);

  const currEPAs = {};
  const currRP1EPAs = {};
  const currRP2EPAs = {};
  const currRP3EPAs = {};

  // Initialize EPAs

  for (let i = 0; i < data.team_events.length; i++) {
    const teamEvent = data.team_events[i];
    let currEPA = postEvent ? teamEvent.epa.breakdown.total_points : teamEvent.epa.stats.start;
    if (!currEPA) currEPA = teamEvent.epa.breakdown.total_points || 0;

    let currRP1EPA = postEvent ? teamEvent.epa.breakdown.rp_1 : 0; // TODO: fix start rp epa
    if (!currRP1EPA) currRP1EPA = teamEvent.epa.breakdown.rp_1 || 0;

    let currRP2EPA = postEvent ? teamEvent.epa.breakdown.rp_2 : 0; // TODO: fix start rp epa
    if (!currRP2EPA) currRP2EPA = teamEvent.epa.breakdown.rp_2 || 0;

    let currRP3EPA = postEvent ? teamEvent.epa.breakdown.rp_3 : 0; // TODO: fix start rp epa
    if (!currRP3EPA) currRP3EPA = teamEvent.epa.breakdown.rp_3 || 0;

    currEPAs[teamEvent.team] = currEPA;
    currRP1EPAs[teamEvent.team] = currRP1EPA;
    currRP2EPAs[teamEvent.team] = currRP2EPA;
    currRP3EPAs[teamEvent.team] = currRP3EPA;
  }

  // Simulate

  const simRanks = {};
  const simRPs = {};

  for (let i = 0; i < data.team_events.length; i++) {
    const teamEvent = data.team_events[i];
    simRanks[teamEvent.team] = [];
    simRPs[teamEvent.team] = [];
  }

  for (let i = 0; i < simCount; i++) {
    const currSimMatches = {};
    const currSimRPs = {};
    const indexToTeam = {};
    const randArr = shuffle(
      Array(teamsN)
        .fill(0)
        .map((_, i) => i + 1)
    );
    for (let j = 0; j < data.team_events.length; j++) {
      const teamEvent = data.team_events[j];
      indexToTeam[randArr[j]] = teamEvent.team;
      currSimMatches[teamEvent.team] = 0;
      currSimRPs[teamEvent.team] = 0;
    }

    for (let j = 0; j < schedule.length; j++) {
      const match = schedule[j];
      const red = match.red.map((index) => indexToTeam[index]);
      const blue = match.blue.map((index) => indexToTeam[index]);

      let redEPA = currEPAs[red[0]] + currEPAs[red[1]] + currEPAs[red[2]];
      let redRP1EPA = currRP1EPAs[red[0]] + currRP1EPAs[red[1]] + currRP1EPAs[red[2]];
      let redRP2EPA = currRP2EPAs[red[0]] + currRP2EPAs[red[1]] + currRP2EPAs[red[2]];
      let redRP3EPA = currRP3EPAs[red[0]] + currRP3EPAs[red[1]] + currRP3EPAs[red[3]];
      let blueEPA = currEPAs[blue[0]] + currEPAs[blue[1]] + currEPAs[blue[2]];
      let blueRP1EPA = currRP1EPAs[blue[0]] + currRP1EPAs[blue[1]] + currRP1EPAs[blue[2]];
      let blueRP2EPA = currRP2EPAs[blue[0]] + currRP2EPAs[blue[1]] + currRP2EPAs[blue[2]];
      let blueRP3EPA = currRP3EPAs[blue[0]] + currRP3EPAs[blue[1]] + currRP3EPAs[blue[3]];

      const winProb = 1 / (1 + Math.pow(10, ((-5 / 8) * (redEPA - blueEPA)) / TOTAL_SD));
      const redWin = Math.random() < winProb ? 1 : 0;

      const redRP1Prob = getRPProb(redRP1EPA);
      const redRP2Prob = getRPProb(redRP2EPA);
      const redPR3Prob = getRPProb(redRP3EPA);
      const redRP1 = Math.random() < redRP1Prob ? 1 : 0;
      const redRP2 = Math.random() < redRP2Prob ? 1 : 0;
      const redRP3 = Math.random() < redPR3Prob ? 1 : 0;

      const blueRP1Prob = getRPProb(blueRP1EPA);
      const blueRP2Prob = getRPProb(blueRP2EPA);
      const bluePR3Prob = getRPProb(blueRP3EPA);
      const blueRP1 = Math.random() < blueRP1Prob ? 1 : 0;
      const blueRP2 = Math.random() < blueRP2Prob ? 1 : 0;
      const blueRP3 = Math.random() < bluePR3Prob ? 1 : 0;

      const redRPs =
        yearNum >= 2025
          ? redRP1 + redRP2 + redRP3 + (redWin ? 3 : 0)
          : redRP1 + redRP2 + (redWin ? 2 : 0);
      const blueRPs =
        yearNum >= 2025
          ? blueRP1 + blueRP2 + blueRP3 + (redWin ? 0 : 3)
          : blueRP1 + blueRP2 + (redWin ? 0 : 2);

      red.forEach((team) => {
        if (currSimMatches[team] < numMatches) {
          currSimRPs[team] += redRPs;
          currSimMatches[team]++;
        }
      });

      blue.forEach((team) => {
        if (currSimMatches[team] < numMatches) {
          currSimRPs[team] += blueRPs;
          currSimMatches[team]++;
        }
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
      simRanks[teamEvent.team].push(simRanksArr.indexOf(teamEvent.team.toString()) + 1);
      simRPs[teamEvent.team].push(currSimRPs[teamEvent.team]);
    }
  }

  if (postMessage) {
    ctx.postMessage({ simRanks, simRPs });
  }

  return { simRanks, simRPs };
}

async function indexSim(
  data: EventData,
  index: number,
  simCount: number,
  postEvent: boolean,
  postMessage: boolean
) {
  const TOTAL_SD = data.year.score_sd;
  const yearNum = data.year.year;

  const qualMatches = data.matches
    .filter((match) => !match.elim)
    .sort((a, b) => a.match_number - b.match_number);
  const qualTeamMatches = data.team_matches.filter((match) => !match.elim);
  const qualN = qualMatches.length;

  const currEPAs = {};
  const currRP1EPAs = {};
  const currRP2EPAs = {};
  const currRP3EPAs = {};
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
    let currEPA = postEvent ? teamEvent.epa.breakdown.total_points : teamEvent.epa.stats.start;
    if (!currEPA) currEPA = teamEvent.epa.breakdown.total_points || 0;

    let currRP1EPA = postEvent ? teamEvent.epa.breakdown.rp_1 : 0; // TODO: fix start rp epa
    if (!currRP1EPA) currRP1EPA = teamEvent.epa.breakdown.rp_1 || 0;

    let currRP2EPA = postEvent ? teamEvent.epa.breakdown.rp_2 : 0; // TODO: fix start rp epa
    if (!currRP2EPA) currRP2EPA = teamEvent.epa.breakdown.rp_2 || 0;

    let currRP3EPA = postEvent ? teamEvent.epa.breakdown.rp_3 : 0; // TODO: fix start rp epa
    if (!currRP3EPA) currRP3EPA = teamEvent.epa.breakdown.rp_3 || 0;

    currEPAs[teamEvent.team] = currEPA;
    currRP1EPAs[teamEvent.team] = currRP1EPA;
    currRP2EPAs[teamEvent.team] = currRP2EPA;
    currRP3EPAs[teamEvent.team] = currRP3EPA;
    currRPs[teamEvent.team] = 0;
    currTiebreakers[teamEvent.team] = [];
  }

  let redResultToRPs = { red: 2, tie: 1, blue: 0 };
  let blueResultToRPs = { red: 0, tie: 1, blue: 2 };
  if (yearNum >= 2025) {
    redResultToRPs = { red: 3, tie: 1, blue: 0 };
    blueResultToRPs = { red: 0, tie: 1, blue: 3 };
  }
  for (let i = 0; i < index; i++) {
    const match = qualMatches[i];
    // always completed unless a match needs to be replayed
    let [redRPs, blueRPs, redTiebreaker, blueTiebreaker] = [2, 2, 0, 0];
    if (match.status === "Completed") {
      redRPs =
        match.result.red_rp_1 +
        match.result.red_rp_2 +
        match.result.red_rp_3 +
        redResultToRPs[match.result.winner];
      blueRPs =
        match.result.blue_rp_1 +
        match.result.blue_rp_2 +
        match.result.blue_rp_3 +
        blueResultToRPs[match.result.winner];
      [redTiebreaker, blueTiebreaker] = getTiebreakers(data.event.year, match);
    }

    const teamMatches = teamMatchesMap[match.key];
    for (let j = 0; j < teamMatches.length; j++) {
      const teamMatch = teamMatches[j];
      const team = teamMatch.team;
      if (!postEvent) {
        // only update EPAs if we're simulating pre-event
        currEPAs[team] = teamMatch.epa.post ?? teamMatch.epa.breakdown.total_points;
        currRP1EPAs[team] = teamMatch.epa.breakdown.rp_1;
        currRP2EPAs[team] = teamMatch.epa.breakdown.rp_2;
        currRP3EPAs[team] = teamMatch.epa.breakdown.rp_3;
      }
      if (
        !match.alliances.red.surrogate_team_keys.includes(team) &&
        !match.alliances.blue.surrogate_team_keys.includes(team) &&
        !match.alliances.red.dq_team_keys.includes(team) &&
        !match.alliances.blue.dq_team_keys.includes(team)
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
    simRanks[teamEvent.team] = [];
    simRPs[teamEvent.team] = [];
  }

  for (let i = 0; i < simCount; i++) {
    const currSimRPs = {};
    const currSimTiebreakers = {};
    for (let j = 0; j < data.team_events.length; j++) {
      const teamEvent = data.team_events[j];
      currSimRPs[teamEvent.team] = currRPs[teamEvent.team];
      currSimTiebreakers[teamEvent.team] = [...currTiebreakers[teamEvent.team]];
    }

    for (let j = index; j < qualN; j++) {
      const match = qualMatches[j];
      let redEPA = 0;
      let redRP1EPA = 0;
      let redRP2EPA = 0;
      let redRP3EPA = 0;
      let blueEPA = 0;
      let blueRP1EPA = 0;
      let blueRP2EPA = 0;
      let blueRP3EPA = 0;
      const teamMatches = teamMatchesMap[match.key];
      for (let k = 0; k < teamMatches.length; k++) {
        const teamMatch = teamMatches[k];
        const team = teamMatch.team;
        if (teamMatch.alliance === "red") {
          redEPA += currEPAs[team];
          redRP1EPA += currRP1EPAs[team];
          redRP2EPA += currRP2EPAs[team];
          redRP3EPA += currRP3EPAs[team];
        } else {
          blueEPA += currEPAs[team];
          blueRP1EPA += currRP1EPAs[team];
          blueRP2EPA += currRP2EPAs[team];
          blueRP3EPA += currRP3EPAs[team];
        }
      }

      const winProb = 1 / (1 + Math.pow(10, ((-5 / 8) * (redEPA - blueEPA)) / TOTAL_SD));
      const redWin = Math.random() < winProb;

      const redRP1Prob = getRPProb(redRP1EPA);
      const redRP1 = Math.random() < redRP1Prob ? 1 : 0;

      const redRP2Prob = getRPProb(redRP2EPA);
      const redRP2 = Math.random() < redRP2Prob ? 1 : 0;

      const redRP3Prob = getRPProb(redRP3EPA);
      const redRP3 = Math.random() < redRP3Prob ? 1 : 0;

      const blueRP1Prob = getRPProb(blueRP1EPA);
      const blueRP1 = Math.random() < blueRP1Prob ? 1 : 0;

      const blueRP2Prob = getRPProb(blueRP2EPA);
      const blueRP2 = Math.random() < blueRP2Prob ? 1 : 0;

      const blueRP3Prob = getRPProb(blueRP3EPA);
      const blueRP3 = Math.random() < blueRP3Prob ? 1 : 0;

      const redRPs =
        yearNum >= 2025
          ? redRP1 + redRP2 + redRP3 + (redWin ? 3 : 0)
          : redRP1 + redRP2 + (redWin ? 2 : 0);
      const blueRPs =
        yearNum >= 2025
          ? blueRP1 + blueRP2 + blueRP3 + (redWin ? 0 : 3)
          : blueRP1 + blueRP2 + (redWin ? 0 : 2);

      for (let k = 0; k < teamMatches.length; k++) {
        const teamMatch = teamMatches[k];
        const team = teamMatch.team;
        if (
          !match.alliances.red.surrogate_team_keys.includes(team) &&
          !match.alliances.blue.surrogate_team_keys.includes(team)
        ) {
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
      simRanks[teamEvent.team].push(simRanksArr.indexOf(teamEvent.team.toString()) + 1);
      simRPs[teamEvent.team].push(currSimRPs[teamEvent.team]);
    }
  }

  if (postMessage) {
    ctx.postMessage({ index, simRanks, simRPs });
  }

  return { index, simRanks, simRPs };
}

async function _strengthOfSchedule(data: EventData, simCount: number, postEvent: boolean) {
  const N = Math.round((6 * data.event.qual_matches) / data.team_events.length);
  const { simRanks: preSimRanks, simRPs: preSimRPs } = await preSim(
    data,
    simCount,
    N,
    postEvent,
    false
  );
  const { simRanks, simRPs } = await indexSim(data, 0, simCount, postEvent, false);

  const teamPartners = {};
  const teamOpponents = {};
  for (let i = 0; i < data.team_events.length; i++) {
    teamPartners[data.team_events[i].team] = [];
    teamOpponents[data.team_events[i].team] = [];
  }
  for (let i = 0; i < data.matches.length; i++) {
    const match = data.matches[i];
    if (match.elim) continue;
    const redTeams = match.alliances.red.team_keys;
    const blueTeams = match.alliances.blue.team_keys;
    for (let j = 0; j < redTeams.length; j++) {
      const currPartners = [];
      for (let k = 0; k < redTeams.length; k++) {
        if (j === k) continue;
        currPartners.push(redTeams[k]);
      }
      teamPartners[redTeams[j]].push(currPartners);

      const currOpponents = [];
      for (let k = 0; k < blueTeams.length; k++) {
        currOpponents.push(blueTeams[k]);
      }
      teamOpponents[redTeams[j]].push(currOpponents);
    }
    for (let j = 0; j < blueTeams.length; j++) {
      const currPartners = [];
      for (let k = 0; k < blueTeams.length; k++) {
        if (j === k) continue;
        currPartners.push(blueTeams[k]);
      }
      teamPartners[blueTeams[j]].push(currPartners);

      const currOpponents = [];
      for (let k = 0; k < redTeams.length; k++) {
        currOpponents.push(redTeams[k]);
      }
      teamOpponents[blueTeams[j]].push(currOpponents);
    }
  }

  const flattenedTeamPartners = {};
  const flattenedTeamOpponents = {};
  for (let i = 0; i < data.team_events.length; i++) {
    const teamNum = data.team_events[i].team;
    flattenedTeamPartners[teamNum] = [];
    flattenedTeamOpponents[teamNum] = [];
    for (let j = 0; j < teamPartners[teamNum].length; j++) {
      flattenedTeamPartners[teamNum].push(...teamPartners[teamNum][j]);
      flattenedTeamOpponents[teamNum].push(...teamOpponents[teamNum][j]);
    }
  }

  const teamEPAs = {};
  let epaAvg = 0;
  let epaSd = 0;
  for (let j = 0; j < data.team_events.length; j++) {
    const teamEvent = data.team_events[j];
    let currEPA = postEvent ? teamEvent.epa.breakdown.total_points : teamEvent.epa.stats.start;
    if (!currEPA) currEPA = teamEvent.epa.breakdown.total_points || 0;
    teamEPAs[teamEvent.team] = currEPA;
    epaAvg += currEPA;
    epaSd += currEPA ** 2;
  }
  epaAvg /= data.team_events.length;
  epaSd = Math.sqrt(epaSd / data.team_events.length - epaAvg ** 2);

  const sosMetrics = {};
  for (let i = 0; i < data.team_events.length; i++) {
    const teamNum = data.team_events[i].team;
    const currPreSimRanks = preSimRanks[teamNum];
    const preSimAvgRank = currPreSimRanks.reduce((x, y) => x + y, 0) / simCount;

    const currPreSimRPs = preSimRPs[teamNum];
    const preSimAvgRP = currPreSimRPs.reduce((x, y) => x + y, 0) / simCount;

    const currSimRanks = simRanks[teamNum];
    const simAvgRank = currSimRanks.reduce((x, y) => x + y, 0) / simCount;

    const currSimRPs = simRPs[teamNum];
    const simAvgRP = currSimRPs.reduce((x, y) => x + y, 0) / simCount;

    const deltaRank = simAvgRank - preSimAvgRank;
    const deltaRP = simAvgRP - preSimAvgRP;

    const rankPercentile = currPreSimRanks.filter((x) => x <= simAvgRank).length / simCount;
    const rpPercentile = currPreSimRPs.filter((x) => x >= simAvgRP).length / simCount;

    const currTeamPartners = flattenedTeamPartners[teamNum];
    const currTeamOpponents = flattenedTeamOpponents[teamNum];

    const avgPartnerEPA =
      currTeamPartners.map((x) => teamEPAs[x]).reduce((x, y) => x + y, 0) / currTeamPartners.length;

    const avgOpponentEPA =
      currTeamOpponents.map((x) => teamEPAs[x]).reduce((x, y) => x + y, 0) /
      currTeamOpponents.length;

    const deltaEPA = epaAvg + 2 * avgPartnerEPA - 3 * avgOpponentEPA;
    const distrib = Gaussian(0, (epaSd * epaSd * 5) / N);
    const epaPercentile = 1 - distrib.cdf(deltaEPA);

    const overallPercentile = (rankPercentile + rpPercentile + epaPercentile) / 3;

    sosMetrics[data.team_events[i].team] = {
      preSimAvgRank,
      simAvgRank,
      deltaRank,
      rankPercentile,
      preSimAvgRP,
      simAvgRP,
      deltaRP,
      rpPercentile,
      avgPartnerEPA,
      avgOpponentEPA,
      deltaEPA,
      epaPercentile,
      overallPercentile,
    };
  }

  return sosMetrics;
}

async function strengthOfSchedule(data: EventData, simCount: number, postMessage: boolean) {
  const preEventMetrics = await _strengthOfSchedule(data, simCount, false);
  const postEventMetrics = await _strengthOfSchedule(data, simCount, true);

  if (postMessage) {
    ctx.postMessage({
      preEventMetrics,
      postEventMetrics,
    });
  }

  return {
    preEventMetrics,
    postEventMetrics,
  };
}

ctx.addEventListener("message", (evt) => {
  switch (evt.data.type) {
    case "preSim":
      const qualMatches = evt.data.data?.event?.qual_matches;
      const teamEvents = evt.data.data?.team_events?.length;
      const matchesPerTeam = evt.data?.matchesPerTeam || 12;
      const N =
        qualMatches > 0 && teamEvents ? Math.round((6 * qualMatches) / teamEvents) : matchesPerTeam;
      preSim(evt.data.data, evt.data.simCount, N, false, true);
      return;
    case "indexSim":
      indexSim(evt.data.data, evt.data.index, evt.data.simCount, false, true);
      return;
    case "strengthOfSchedule":
      strengthOfSchedule(evt.data.data, evt.data.simCount, true);
      return;
  }
});

export {};
