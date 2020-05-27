import React from "react";

import { Jumbotron, Button } from "react-bootstrap";
import { Typography, Divider } from '@material-ui/core'

import { Header } from './../..'
import styles from './Home.module.css'

export default function Home() {
  return (
    <div>
    <Header />
    <Jumbotron>
      <Typography variant="h2">Statbotics.io</Typography>
      <Typography variant="h5">Modernizing FRC Data Analytics</Typography>
      <br/>
      <Divider />
      <br/>
      <p>
        Welcome to Statbotics.io. We are working towards modernizing and distributing FRC data analytics. Currently focusing on ELO ratings, building of Caleb Sykes' work. Check the tabs above for tables and charts displaying ELO rankings for FRC teams. We're in the early stages, more coming soon!
      </p>
      <p>
        <Button variant="primary" className={styles.link}>
          <a href="/teams" className={styles.link}>Team Tables</a>
        </Button>
        <Button variant="primary" className={styles.link}>
          <a href="/years" className={styles.link}>Year Tables</a>
        </Button>
        <Button variant="primary" className={styles.link}>
          <a href="/compare" className={styles.link}>Compare Teams</a>
        </Button>
      </p>
    </Jumbotron>
    </div>
  );
}
