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
  const data = await getData(match_id);

  if (!data) {
    return <div>Match not found</div>;
  }

  return (
    <div>
      <h1>Match: {match_id}</h1>
    </div>
  );
}

export default Match;
