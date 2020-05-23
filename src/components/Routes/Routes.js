import React from "react";
import { Route, Switch } from "react-router-dom";

import { Home } from "./../Containers/index.js";

export default function Routes() {
  return (
    <Switch>
      <Route exact path="/Home">
        <Home />
      </Route>
    </Switch>
  );
}
