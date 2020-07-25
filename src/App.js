import React from "react";

import { Route, Switch } from "react-router-dom";
import { Navigation } from "./components";

import {
  Home,
  TeamLookup,
  TeamYearLookup,
  EventLookup,
  TeamView,
  TeamCompare,
  Hypothetical,
  Swagger,
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
          <TeamLookup />
        </Route>
        <Route exact path="/years">
          <TeamYearLookup />
        </Route>
        <Route exact path="/events">
          <EventLookup />
        </Route>
        <Route path="/teams/:team">
          <TeamView />
        </Route>
        <Route path="/compare">
          <TeamCompare />
        </Route>
        <Route path="/predict">
          <Hypothetical />
        </Route>
        <Route path="/docs">
          <Swagger />
        </Route>
      </Switch>
    </div>
  );
};

export default App;
