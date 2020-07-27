import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import styles from "./EventView.module.css";

export default function EventView() {
  let { event } = useParams();

  return <h1>{event}</h1>;
}
