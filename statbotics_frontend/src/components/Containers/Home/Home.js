import React from "react";

import { Card, Button } from "react-bootstrap";
import { Typography } from '@material-ui/core'

import { Header } from './../..'
import styles from './Home.module.css'

export default function Home() {
  return (
    <div>
    <Header />
    <Card className={styles.card}>
      <Typography>
        Welcome to Statbotics.io! Our mission is to develop and distribute FRC data analysis. Currently, we are focused on Elo Ratings, building upon Caleb Sykes' previous work. We're in the early stages, and hope to add content related to OPR, event prediction, and Zebra MotionWorks soon. Stay tuned!
      </Typography>
      <div className={styles.height}></div>
      <Typography>
        Elo is a measure of a team's on-field strength, calculated using win margins from over 100,000 matches dating back to 2002. A Elo of 1500 is roughly average, and an Elo of 1800+ is in the top 1% worldwide. Check the menu above or buttons below for tables and charts displaying Elo trends. Remember, this is just one method to rank teams, and shouldn't be taken too seriously ;)
      </Typography>
      <div className={styles.button_group}>
        <Button variant="primary" className={styles.button} href="/teams">
          Team Tables
        </Button>
        <Button variant="primary" className={styles.button} href="/years">
          Year Tables
        </Button>
        <Button variant="primary" className={styles.button} href="/compare">
          Compare Teams
        </Button>
        <Button variant="primary" className={styles.button} href="/predict">
          Predict Match
        </Button>
      </div>
    </Card>
    </div>
  );
}
