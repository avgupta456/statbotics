import { useRouter } from "next/router";

import { PageContent } from "..";
import { CURR_YEAR } from "../../../../utils/constants";

export default function TeamYearPage() {
  const router = useRouter();
  const { team } = router.query;
  let paramYear = parseInt(router.query.year as string);
  if (Number.isNaN(paramYear) || paramYear < 2002 || paramYear > CURR_YEAR) {
    paramYear = CURR_YEAR;
  }

  if (typeof team !== "string") {
    return null;
  }

  return (
    <PageContent
      team={team as string}
      paramYear={paramYear}
      interpolation={{ team, year: paramYear }}
    />
  );
}
