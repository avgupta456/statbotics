import React from "react";

import { makeStyles } from '@material-ui/core/styles';
import { Paper, TextField, Typography } from "@material-ui/core";
import { ButtonGroup } from "react-bootstrap";

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

  function updateRed1(e) {setRed1(e.target.value)}
  function updateRed2(e) {setRed2(e.target.value)}
  function updateRed3(e) {setRed3(e.target.value)}

  function updateBlue1(e) {setBlue1(e.target.value)}
  function updateBlue2(e) {setBlue2(e.target.value)}
  function updateBlue3(e) {setBlue3(e.target.value)}

  function updateYear(e) {setYear(e.target.value)}

  return (
    <Paper className={styles.main}>
    {console.log(red1)}
    {console.log(red2)}
    {console.log(red3)}
    {console.log(blue1)}
    {console.log(blue2)}
    {console.log(blue3)}
    {console.log(year)}
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
    </Paper>
  );
}
