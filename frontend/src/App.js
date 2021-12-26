import React from "react";

import { Route, Switch, Redirect } from "react-router-dom";
import { Navigation } from "./components";

import {
  Home,
  TeamLookup,
  TeamYearLookup,
  EventLookup,
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
        <Route path="/events/:key">
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
