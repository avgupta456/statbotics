import React from "react";

import { Route, Switch, Redirect } from "react-router-dom";
import { Navigation } from "./components";

import {
  Home,
  TeamLookup,
  TeamYearLookup,
  CurrentTeamYearLookup,
  EventLookup,
  CurrentEventLookup,
  TeamView,
  EventView,
  TeamCompare,
  Hypothetical,
  Swagger,
  NotFound,
} from "./components/Containers";
import styles from "./App.module.css";

const App = () => {
  return (
    <div>
      <Navigation className={styles.nav} />
      <Switch className={styles.body}>
        <Route exact path="/">
          <Home />
        </Route>
        <Route exact path="/teams">
          <CurrentTeamYearLookup />
        </Route>
        <Route exact path="/events">
          <CurrentEventLookup />
        </Route>
        <Route exact path="/all/teams">
          <TeamLookup />
        </Route>
        <Route exact path="/all/team-years">
          <TeamYearLookup />
        </Route>
        <Route exact path="/all/events">
          <EventLookup />
        </Route>
        <Route path="/team/:team">
          <TeamView />
        </Route>
        <Route path="/event/:key">
          <EventView />
        </Route>
        <Route exact path="/compare">
          <TeamCompare />
        </Route>
        <Route exact path="/predict">
          <Hypothetical />
        </Route>
        <Route exact path="/docs">
          <Swagger />
        </Route>
        <Route exact path="/404">
          <NotFound />
        </Route>
        <Redirect from="/*" to="/404" />
      </Switch>
    </div>
  );
};

export default App;
