import { useRouter } from "next/router";

import { CURR_YEAR } from "../../../utils/constants";
import PageContent from "./main";

export default function TeamPage() {
  const router = useRouter();
  const team = router?.query?.team?.toString() ?? "";
  return PageContent({ team, paramYear: CURR_YEAR });
}
