import React from "react";
import { Route, Switch } from "react-router-dom";

import { About, TeamLookup } from "./../Containers/index.js";

export default function Routes() {
  return (
    <Switch>
      <Route exact path="/About">
        <About />
      </Route>
      <Route exact path="/Teams">
        <TeamLookup />
      </Route>
    </Switch>
  );
}
