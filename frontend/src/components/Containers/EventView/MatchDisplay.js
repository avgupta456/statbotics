import React from "react";

import { Container, Row, Col } from "react-bootstrap";

import styles from "./EventView.module.css";

function getName(key) {
  if (key.slice(0, 2) === "qm") {
    return "Quals " + key.slice(2);
  } else if (key.slice(0, 2) === "qf") {
    return "Quarters " + key[2] + " Match " + key[4];
  } else if (key.slice(0, 2) === "sf") {
    return "Semis " + key[2] + " Match " + key[4];
  } else if (key[0] === "f") {
    return "Finals " + key[1] + " Match " + key[3];
  }
  return key;
}

export default function getMatchDisplays(year, matches) {
  const parseNum = (str) =>
    str
      .replace("qm", "0")
      .replace("qf", "1")
      .replace("sf", "2")
      .replace("f", "3")
      .replace("m", "0");
  matches = matches.sort((a, b) => parseNum(a["match"]) - parseNum(b["match"]));
  const match_display = matches.map(function (x, i) {
    return (
      <Container className={styles.container} key={i}>
        <Row>
          <Col xs="2" className={styles.outline}>
            <b>{getName(x["match"])}</b>
          </Col>
          <Col xs="6" className={styles.outline}>
            <Row className={styles.red}>
              {x["red"].map(function (y, i) {
                return (
                  <Col key={i}>
                    <a
                      className={styles.link}
                      href={`./../team/${x["red"][i]}`}
                      children={
                        x["winner"] === "red" ? (
                          <b>{x["red"][i]}</b>
                        ) : (
                          x["red"][i]
                        )
                      }
                    />
                  </Col>
                );
              })}
              <Col>
                {x["winner"] === "red" ? (
                  <b>{x["red_score"]}</b>
                ) : x["red_score"] >= 0 ? (
                  x["red_score"]
                ) : (
                  ""
                )}
                {x["red_rp_1"] === 1 ? <sup>●</sup> : ""}
                {x["red_rp_2"] === 1 ? <sup>●</sup> : ""}
              </Col>
            </Row>
            <Row className={styles.blue}>
              {x["blue"].map(function (y, i) {
                return (
                  <Col key={i}>
                    <a
                      className={styles.link}
                      href={`./../team/${x["blue"][i]}`}
                      children={
                        x["winner"] === "blue" ? (
                          <b>{x["blue"][i]}</b>
                        ) : (
                          x["blue"][i]
                        )
                      }
                    />
                  </Col>
                );
              })}
              <Col>
                {x["winner"] === "blue" ? (
                  <b>{x["blue_score"]}</b>
                ) : x["blue_score"] >= 0 ? (
                  x["blue_score"]
                ) : (
                  ""
                )}
                {x["blue_rp_1"] === 1 ? <sup>●</sup> : ""}
                {x["blue_rp_2"] === 1 ? <sup>●</sup> : ""}
              </Col>
            </Row>
          </Col>
          <Col xs="4" className={styles.outline}>
            <Row>
              <Col
                className={
                  x["red_score"] >= 0
                    ? x["winner_correct"]
                      ? styles.correct
                      : styles.incorrect
                    : x["winner_pred"] === "red"
                    ? styles.red
                    : styles.blue
                }
              >
                {x["winner_pred"] === "red" ? "Red" : "Blue"}
              </Col>
              {year >= 2016 ? (
                <Col
                  className={
                    x["playoff"] || x["red_score"] < 0
                      ? styles.none
                      : x["red_rp_1_correct"]
                      ? styles.correct
                      : styles.incorrect
                  }
                >
                  {x["playoff"]
                    ? "-"
                    : parseInt(x["red_rp_1_prob"] * 100) + "%"}
                </Col>
              ) : (
                ""
              )}
              {year >= 2016 ? (
                <Col
                  className={
                    x["playoff"] || x["red_score"] < 0
                      ? styles.none
                      : x["red_rp_2_correct"]
                      ? styles.correct
                      : styles.incorrect
                  }
                >
                  {x["playoff"]
                    ? "-"
                    : parseInt(x["red_rp_2_prob"] * 100) + "%"}
                </Col>
              ) : (
                ""
              )}
            </Row>
            <Row>
              <Col
                className={
                  x["red_score"] >= 0
                    ? x["winner_correct"]
                      ? styles.correct
                      : styles.incorrect
                    : x["winner_pred"] === "red"
                    ? styles.red
                    : styles.blue
                }
              >
                {parseInt(x["win_prob"] * 100) + "%"}
              </Col>
              {year >= 2016 ? (
                <Col
                  className={
                    x["playoff"] || x["red_score"] < 0
                      ? styles.none
                      : x["blue_rp_1_correct"]
                      ? styles.correct
                      : styles.incorrect
                  }
                >
                  {x["playoff"]
                    ? "-"
                    : parseInt(x["blue_rp_1_prob"] * 100) + "%"}
                </Col>
              ) : (
                ""
              )}
              {year >= 2016 ? (
                <Col
                  className={
                    x["playoff"] || x["red_score"] < 0
                      ? styles.none
                      : x["blue_rp_2_correct"]
                      ? styles.correct
                      : styles.incorrect
                  }
                >
                  {x["playoff"]
                    ? "-"
                    : parseInt(x["blue_rp_2_prob"] * 100) + "%"}
                </Col>
              ) : (
                ""
              )}
            </Row>
          </Col>
        </Row>
      </Container>
    );
  });

  return (
    <div>
      <Container className={styles.container} key={-1}>
        <Row>
          <Col xs="2" className={styles.outline}>
            Match Number
          </Col>
          <Col xs="6" className={styles.outline}>
            <Row>
              <Col>Team 1</Col>
              <Col>Team 2</Col>
              <Col>Team 3</Col>
              <Col>Score</Col>
            </Row>
          </Col>
          <Col xs="4" className={styles.outline}>
            <Row>
              <Col>Winner Pred</Col>
              {year >= 2016 ? <Col>RP 1 Pred</Col> : ""}
              {year >= 2016 ? <Col>RP 2 Pred</Col> : ""}
            </Row>
          </Col>
        </Row>
      </Container>
      {match_display}
    </div>
  );
}
