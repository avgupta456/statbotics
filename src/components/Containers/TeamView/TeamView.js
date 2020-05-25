import React, { useState, useEffect } from "react";

import { Jumbotron } from "react-bootstrap";

import { fetchTeam } from './../../../api'

import styles from './TeamView.module.css'

import { ResponsiveLine } from '@nivo/line'

export function chart(data) {
  return (
    <ResponsiveLine
        data={data}
        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
        xScale={{ type: 'point' }}
        yScale={{ type: 'linear', min: 1200, max: 2200, stacked: false, reverse: false }}
        curve="linear"
        axisBottom={{
            orient: 'bottom',
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: 'Year',
            legendOffset: 40,
            legendPosition: 'middle'
        }}
        axisLeft={{
            orient: 'left',
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: 'Max ELO',
            legendOffset: -50,
            legendPosition: 'middle'
        }}
        colors={{ scheme: 'set1' }}
        pointSize={10}
        pointLabel="y"
        pointLabelYOffset={-12}
        useMesh={true}
        legends={[
            {
                anchor: 'top-right',
                direction: 'column',
                justify: false,
                translateX: 100,
                translateY: 0,
                itemsSpacing: 0,
                itemDirection: 'left-to-right',
                itemWidth: 80,
                itemHeight: 20,
                itemOpacity: 0.75,
                symbolSize: 12,
                symbolShape: 'circle',
                symbolBorderColor: 'rgba(0, 0, 0, .5)',
                effects: [
                    {
                        on: 'hover',
                        style: {
                            itemBackground: 'rgba(0, 0, 0, .03)',
                            itemOpacity: 1
                        }
                    }
                ]
            }
        ]}
    />
  );
}

export default function TeamView() {
  const [teamData, setTeamData] = useState([])

  function clean(data) {
    console.log(data)
    const new_data = data.map(function(x, i){ return {
      x: x["year"],
      y: x["elo_max"],
    }});
    console.log(new_data)
    return new_data
  };

  useEffect(() => {
    const getTeam = async (team) => {
      const new_teams = await fetchTeam(team);
      setTeamData(clean(new_teams.results));
    };

    getTeam(254)
  }, [])

  console.log(teamData)
  const newTeamData = [{data: teamData, id: "254"}}]
  console.log(newTeamData)

  return (
    <Jumbotron className={styles.height}>
      {chart(newTeamData)}
    </Jumbotron>
  );
}
