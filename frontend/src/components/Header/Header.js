import React from "react";
import Typist from "react-typist";

import styles from "./Header.module.css";

export default function Header() {
  return (
    <div>
      <br />
      <Typist
        cursor={{ blink: true, hideWhenDone: true }}
        className={[styles.header, styles.typist].join(" ")}
        avgTypingDelay={80}
        stdTypingDelay={20}
      >
        Statbotics.io
      </Typist>
      <Typist
        cursor={{ blink: true, hideWhenDone: true }}
        className={[styles.subheader, styles.typist].join(" ")}
        avgTypingDelay={50}
        stdTypingDelay={10}
        startDelay={1500}
      >
        Modernizing FRC Data Analytics
      </Typist>
    </div>
  );
}
