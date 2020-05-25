import React from "react";

import { Jumbotron, Button } from "react-bootstrap";

import styles from './Home.module.css'

export default function Home() {
  return (
    <Jumbotron>
      <h1>Welcome to Statbotics.io!</h1>
      <h2>Modernizing FRC Data Analytics</h2>
      <p>
        Check the tabs above for tables and charts displaying ELO rankings for FRC teams. More coming soon!
      </p>
      <p>
        <Button variant="primary" className={styles.link}>
          <a href="/teams" className={styles.link}>Visit Tables</a>
        </Button>
      </p>
    </Jumbotron>
  );
}
