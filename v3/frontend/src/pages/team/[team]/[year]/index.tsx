import { useRouter } from "next/router";

import { CURR_YEAR } from "../../../../utils/constants";
import PageContent from "../main";

export default function TeamPage() {
  const router = useRouter();
  const team = router?.query?.team?.toString() ?? "";
  const rawYear = parseInt(router?.query?.year?.toString() ?? "");
  const cleanYear = Math.max(2002, Math.min(CURR_YEAR, rawYear ?? CURR_YEAR));
  return PageContent({ team, paramYear: cleanYear });
}
