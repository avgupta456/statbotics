import React from "react";

import { Jumbotron, Button } from "react-bootstrap";

import styles from './Home.module.css'

export default function Home() {
  return (
    <Jumbotron>
      <h1>Welcome to Statbotics.io!</h1>
      <h2>Modernizing FRC Data Analytics</h2>
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
  );
}
