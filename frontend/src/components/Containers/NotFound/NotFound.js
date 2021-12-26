import React from "react";

import { Card } from "react-bootstrap";
import { Typography } from "@material-ui/core";

import { Header } from "./../..";
import styles from "./NotFound.module.css";

export default function NotFound() {
  return (
    <div>
      <Header />
      <Card className={styles.card}>
        <Typography variant="h4">Error 404</Typography>
        <Typography variant="h6">
          Sorry, we couldn't find the thing you were looking for. Double check
          your URL and try again.
        </Typography>
      </Card>
    </div>
  );
}
