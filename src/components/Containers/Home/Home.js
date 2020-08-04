import React from "react";

import { Card } from "react-bootstrap";
import { Typography } from "@material-ui/core";

import { Header } from "./../..";
import styles from "./Home.module.css";

export default function Home() {
  return (
    <div>
      <Header />
      <Card className={styles.card}>
        <Typography>
          Welcome to Statbotics.io! Our mission is to develop and distribute FRC
          data analysis. Currently, we have calculated Elo Ratings, (component)
          OPRs, RP strengths, and win-loss records. These statistics are
          available through interactive tables, a REST API, and a Python
          library. Using these metrics, we have developed match predictions and
          a complete event simulator. We hope to continue adding new features,
          such as Zebra MotionWorks analysis and more predictive modeling. Use
          the tabs above to explore all the features. Enjoy!
        </Typography>
        <div className={styles.button_group}>
          <Card className={styles.sub_card}>
            <Typography variant="h5">Elo</Typography>
            <hr />
            Elo is a measure of a team's on-field strength, calculated using win
            margins from over 100,000 matches dating back to 2002. An Elo of
            1500 is roughly average, while an Elo of 1800+ is in the top 1%
            worldwide. At Statbotics, browse Elo ratings for teams, seasons, and
            events.
          </Card>
          <Card className={styles.sub_card}>
            <Typography variant="h5">OPR</Typography>
            <hr />
            OPR uses linear algebra to estimate a team's contribution to an
            alliance. Statbotics.io makes OPR and component OPR (Auto, Teleop,
            Endgame) data easily accessible for teams and events. For recent
            years, Ranking Point strengths are available as well.
          </Card>
          <Card className={styles.sub_card}>
            <Typography variant="h5">Insights</Typography>
            <hr />
            Combining Elo and OPR data from all prior matches, Statbotics.io
            allows users to quickly pull up and compare stats across teams. Find
            which teams performed the best this year, or the sleeper picks at
            your event.
          </Card>
          <Card className={styles.sub_card}>
            <Typography variant="h5">Predictions</Typography>
            <hr />
            Taking insights one step further, Statbotics.io leverages Elo and
            OPR statistics for accurate match prediction and event simulation.
            These tools can help your team make strategic decisions and win
            matches.
          </Card>
        </div>
        <hr />
        For more information about the metrics and methodology, read here!
      </Card>
    </div>
  );
}
