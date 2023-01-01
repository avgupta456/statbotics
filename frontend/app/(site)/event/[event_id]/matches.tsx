import React from "react";

import MatchTable from "../../../../components/MatchTable";
import { classnames } from "../../../../utils";
import { Data } from "./types";

const MatchSection = ({ eventId, data }: { eventId: string; data: Data }) => {
  return (
    <div>
      <MatchTable
        year={2022} // TODO
        teamNum={null}
        matches={data.matches}
        foulRate={0} // TODO
      />
    </div>
  );
};

export default MatchSection;
