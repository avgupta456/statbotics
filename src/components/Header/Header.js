import React from 'react';

import { Divider } from '@material-ui/core';
import Typist from 'react-typist';

import styles from './Header.module.css';
import './main.scss';

export default function Header() {

  return (
    <div>
    <br/>
    <Divider/>
    <br/>
      <Typist
        cursor={{blink: true, hideWhenDone: true}}
        className={styles.header}
        avgTypingDelay={80}
        stdTypingDelay={20}
      >
        Statbotics.io
      </Typist>
      <div className={styles.fix_height}>
        <Typist
          cursor={{blink: true, hideWhenDone: true}}
          className={styles.subheader}
          avgTypingDelay={50}
          stdTypingDelay={10}
          startDelay = {1500}
        >
          Modernizing FRC Data Analytics
        </Typist>
      </div>
      <br/>
      <Divider/>
      <br/>
    </div>
  );
}
