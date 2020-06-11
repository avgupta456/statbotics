import React, { Component } from "react";
import SwaggerUi, { presets } from "swagger-ui";
import "swagger-ui/dist/swagger-ui.css";

class SwaggerTest extends Component {
  componentDidMount() {
    SwaggerUi({
      dom_id: "#swaggerContainer",
      url: `https://backend.statbotics.io/swagger/`,
      presets: [presets.apis],
    });
  }

  render() {
    return <div id="swaggerContainer" />;
  }
}

export default SwaggerTest;
