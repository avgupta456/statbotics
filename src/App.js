import React, { Fragment } from "react";
import ReactDOM from "react-dom";

import { makeStyles, Theme } from '@material-ui/core/styles';
import { AppBar, Toolbar, Tabs, Tab, Typography, IconButton } from "@material-ui/core";

import { Switch, Route, Link, BrowserRouter, Redirect } from "react-router-dom";

import styles from './App.module.css'
import logo from "./static/favicon.ico";

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    flexGrow: 1,
  },
  tab_root: {
    justifyContent: "center",
  },
  scroller: {
    flexGrow: 0,
  },
  logoButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    verticalAlign: "middle",
    display: 'inline-block'
  }
}));


export default function App() {
  const classes = useStyles();
  const allTabs = ['/', '/tab2', '/tab3'];

  return (
    <BrowserRouter>
      <Route
        path="/"
        render={({ location }) => (
          <Fragment>
            <AppBar position="static">
            <div className={styles.row}>
              <div className={styles.left_column}>
                <IconButton edge="start" className={classes.logoButton} color="inherit" aria-label="menu">
                  <img
                    alt="Logo" src={logo} width="25" height="25"
                    className="d-inline-block align-top"
                  />
                </IconButton>
                <Typography variant="h6" className={classes.title}>Statbotics</Typography>
              </div>
              <div className={styles.middle_column}>
                <Tabs
                  classes={{root: classes.tab_root, scroller: classes.scroller}}
                  value={location.pathname}
                  variant="scrollable"
                  scrollButtons="on"
                >
                  <Tab label="Item One" value="/" component={Link} to={allTabs[0]} />
                  <Tab label="Item Two" value="/tab2" component={Link} to={allTabs[1]} />
                  <Tab label="Item Three" value="/tab3" component={Link} to={allTabs[2]} />
                </Tabs>
                </div>
                <div className={styles.right_column}/>
              </div>
            </AppBar>
            <Switch>
              <Route path={allTabs[1]} render={() => <div>Tab 2</div>} />
              <Route path={allTabs[2]} render={() => <div>Tab 3</div>} />
              <Route path={allTabs[0]} render={() => <div>Tab 1</div>} />
            </Switch>
          </Fragment>
        )}
      />
    </BrowserRouter>
  );
}
