import React, {useEffect} from "react";

import { makeStyles } from '@material-ui/core/styles';
import { Paper, TextField, Typography } from "@material-ui/core";
import { ButtonGroup, Button } from "react-bootstrap";

import { fetchTeamYear } from './../../../api';
import styles from './Hypothetical.module.css';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    margin: theme.spacing(3),
    flex: "0 0 175px",
  },
}));

export default function Hypothetical() {
  const classes = useStyles();
  const default_year = 2019;

  const [red1, setRed1] = React.useState(0)
  const [red2, setRed2] = React.useState(0)
  const [red3, setRed3] = React.useState(0)

  const [blue1, setBlue1] = React.useState(0)
  const [blue2, setBlue2] = React.useState(0)
  const [blue3, setBlue3] = React.useState(0)

  const [year, setYear] = React.useState(default_year)
  const [button, setButton] = React.useState(0)

  function updateRed1(e) {setRed1(e.target.value)}
  function updateRed2(e) {setRed2(e.target.value)}
  function updateRed3(e) {setRed3(e.target.value)}

  function updateBlue1(e) {setBlue1(e.target.value)}
  function updateBlue2(e) {setBlue2(e.target.value)}
  function updateBlue3(e) {setBlue3(e.target.value)}

  function updateYear(e) {setYear(e.target.value)}

  function buttonClick() {setButton(button+1)}

  const [redElo1, setRedElo1] = React.useState(0)
  const [redElo2, setRedElo2] = React.useState(0)
  const [redElo3, setRedElo3] = React.useState(0)

  const [blueElo1, setBlueElo1] = React.useState(0)
  const [blueElo2, setBlueElo2] = React.useState(0)
  const [blueElo3, setBlueElo3] = React.useState(0)

  useEffect(() => {
    const setElo = async (team, func) => {
      const data = await fetchTeamYear(team, year, "elo")
      func(data.results[0].elo_max)
    };

    if(button>0) {
      console.log("Made It")
      setElo(red1, setRedElo1)
      setElo(red2, setRedElo2)
      setElo(red3, setRedElo3)
      setElo(blue1, setBlueElo1)
      setElo(blue2, setBlueElo2)
      setElo(blue3, setBlueElo3)
      setButton(0)
    }

    const redTotal = redElo1+redElo2+redElo3
    const blueTotal = blueElo1+blueElo2+blueElo3

    console.log(redTotal)
    console.log(blueTotal)

  }, [button, red1, red2, red3, blue1, blue2, blue3, year,
      redElo1, redElo2, redElo3, blueElo1, blueElo2, blueElo3])

  return (
    <Paper className={styles.main}>
    <Typography variant="h6">Predict a Match!</Typography>
    <ButtonGroup className={styles.button_group}>
      <TextField
        defaultValue=""
        variant="outlined"
        className={classes.textField}
        onChange={updateRed1}
        helperText="Enter Red 1"
        margin="normal"
      />
      <TextField
        defaultValue=""
        variant="outlined"
        className={classes.textField}
        onChange={updateRed2}
        helperText="Enter Red 2"
        margin="normal"
      />
      <TextField
        defaultValue=""
        variant="outlined"
        className={classes.textField}
        onChange={updateRed3}
        helperText="Enter Red 3"
        margin="normal"
      />
    </ButtonGroup>
    <ButtonGroup className={styles.button_group}>
      <TextField
        defaultValue=""
        variant="outlined"
        className={classes.textField}
        onChange={updateBlue1}
        helperText="Enter Blue 1"
        margin="normal"
      />
      <TextField
        defaultValue=""
        variant="outlined"
        className={classes.textField}
        onChange={updateBlue2}
        helperText="Enter Blue 2"
        margin="normal"
      />
      <TextField
        defaultValue=""
        variant="outlined"
        className={classes.textField}
        onChange={updateBlue3}
        helperText="Enter Blue 3"
        margin="normal"
      />
    </ButtonGroup>
    <TextField
      defaultValue={default_year}
      variant="outlined"
      className={classes.textField}
      onChange={updateYear}
      helperText="Enter Year"
      margin="normal"
    />
    <Button
      variant="outline-dark"
      onClick={() => buttonClick()}
      className={styles.button}
    >
      Predict Match
    </Button>
    </Paper>
  );
}
