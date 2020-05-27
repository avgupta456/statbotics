import React, {useEffect} from "react";

import { makeStyles } from '@material-ui/core/styles';
import { TextField, Typography, Button } from "@material-ui/core";
import { Card, ButtonGroup, ProgressBar } from "react-bootstrap";

import { fetchTeamYearElo } from './../../../api';
import styles from './Hypothetical.module.css';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft:  theme.spacing(3),
    marginRight:  theme.spacing(3),
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
    width: "175",
    maxWidth: "175px",
    '@media (max-width: 800px)': {
      width: "100px"
    }
  },
  button: {
    marginLeft:  theme.spacing(3),
    marginRight:  theme.spacing(3),
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
    width: "200px",
    height: "40px",
  },
  container: {
    width: "100%",
    display: 'flex',
  },
  type: {
    margin: "auto",
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

  function buttonClick() {setButton(button+2)}

  const [redElo1, setRedElo1] = React.useState(0)
  const [redElo2, setRedElo2] = React.useState(0)
  const [redElo3, setRedElo3] = React.useState(0)

  const [blueElo1, setBlueElo1] = React.useState(0)
  const [blueElo2, setBlueElo2] = React.useState(0)
  const [blueElo3, setBlueElo3] = React.useState(0)

  const [winProb, setWinProb] = React.useState(0.5)

  useEffect(() => {
    const setElo = async (team, func) => {
      const data = await fetchTeamYearElo(team, year)
      func(data)
    };

    if(button>1) {
      setElo(red1, setRedElo1)
      setElo(red2, setRedElo2)
      setElo(red3, setRedElo3)
      setElo(blue1, setBlueElo1)
      setElo(blue2, setBlueElo2)
      setElo(blue3, setBlueElo3)
      setButton(1)
    }

    const redTotal = redElo1+redElo2+redElo3
    const blueTotal = blueElo1+blueElo2+blueElo3
    const diff = blueTotal-redTotal
    const prob = 1/(1+10**(diff/400))
    setWinProb((100*prob).toFixed(1))

  }, [button, red1, red2, red3, blue1, blue2, blue3, year,
      redElo1, redElo2, redElo3, blueElo1, blueElo2, blueElo3])

  return (
    <Card className={styles.main}>
    <Typography variant="h6">Predict a Match using ELO!</Typography>
    <div className={styles.height}></div>
    <ButtonGroup className={styles.button_group}>
      <div className={[styles.red, styles.row].join(' ')}>
        <TextField
          defaultValue=""
          variant="outlined"
          className={classes.textField}
          onChange={updateRed1}
          helperText="Enter Red 1"
          margin="dense"
        />
        <TextField
          defaultValue=""
          variant="outlined"
          className={classes.textField}
          onChange={updateRed2}
          helperText="Enter Red 2"
          margin="dense"
        />
        <TextField
          defaultValue=""
          variant="outlined"
          className={classes.textField}
          onChange={updateRed3}
          helperText="Enter Red 3"
          margin="dense"
        />
      </div>
    </ButtonGroup>
    <ButtonGroup className={styles.button_group}>
      <div className={[styles.blue, styles.row].join(' ')}>
        <TextField
          defaultValue=""
          variant="outlined"
          className={classes.textField}
          onChange={updateBlue1}
          helperText="Enter Blue 1"
          margin="dense"
        />
        <TextField
          defaultValue=""
          variant="outlined"
          className={classes.textField}
          onChange={updateBlue2}
          helperText="Enter Blue 2"
          margin="dense"
        />
        <TextField
          defaultValue=""
          variant="outlined"
          className={classes.textField}
          onChange={updateBlue3}
          helperText="Enter Blue 3"
          margin="dense"
        />
      </div>
    </ButtonGroup>
    <ButtonGroup className={styles.button_group}>
      <TextField
        defaultValue={default_year}
        variant="outlined"
        className={classes.textField}
        onChange={updateYear}
        helperText="Enter Year"
        margin="dense"
      />
      <Button
        variant="outlined"
        color="primary"
        onClick={() => buttonClick()}
        className={classes.button}
      >
        Predict Match
      </Button>
    </ButtonGroup>
    <div className={classes.container}>
      <Typography className={classes.type}>
        {button===0 ? "Enter teams and click 'Predict Match'" :
          winProb>50 ? `ELO predicts Red Alliance has a ${winProb}% chance of winning.` :
            `ELO predicts Blue Alliance has a ${100-winProb}% chance of winning.`}
      </Typography>
    </div>
    <br/>
    <div className={classes.container}>
      <ProgressBar now={winProb} variant="danger" className={styles.progress}/>
    </div>
    <br/>
    <p className={styles.center}>
      Note: If a team does not exist, they are assigned an ELO of 0, so double check your team numbers!
    </p>
    </Card>
  );
}
