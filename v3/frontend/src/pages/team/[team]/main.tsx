import { useState } from "react";

type TeamData = any;
type TeamYearsData = any;

export default function PageContent({ team, paramYear }: { team: string; paramYear: number }) {
  const [year, _setYear] = useState(paramYear);

  const [loading, setLoading] = useState(true);
  const [teamData, setTeamData] = useState<TeamData | undefined>();
  const [teamYearsData, setTeamYearsData] = useState<TeamYearsData | undefined>();
  const [teamYearDataDict, setTeamYearDataDict] = useState<{
    [key: number]: TeamYearData | undefined;
  }>({});

  console.log(team, year, loading, teamData, teamYearsData, teamYearDataDict);

  if (!loading && !teamData) {
    return <div>Team not found</div>;
  }

  return (
    <div>
      Team Page {team} {year}
    </div>
  );
}
