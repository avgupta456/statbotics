import { BACKEND_URL } from "../../../../constants";
import { log, round } from "../../../../utils";

export async function getTeamData(team: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team/${team}`, { next: { revalidate: 60 } });
  log(`/team/${team} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }

  const data = await res.json();
  return data?.data;
}

export async function getTeamYearData(team: number, year: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team/${team}/${year}`, { next: { revalidate: 60 } });
  log(`/team/${team}/${year} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}

export async function getTeamYearsData(team: number) {
  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}/team/${team}/years`, { next: { revalidate: 60 } });
  log(`/team/${team}/years took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }
  const data = await res.json();
  return data?.data;
}
