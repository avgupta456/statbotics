import React, { useState, useEffect } from "react";

import { Jumbotron, Button } from "react-bootstrap";

import { fetchTeam } from './../../../api'

import styles from './Home.module.css'

import { ResponsiveLine } from '@nivo/line'

const countries = [
  {
    "id": "japan",
    "color": "hsl(216, 70%, 50%)",
    "data": [
      {
        "x": "plane",
        "y": 297
      },
      {
        "x": "helicopter",
        "y": 44
      },
      {
        "x": "boat",
        "y": 50
      },
      {
        "x": "train",
        "y": 196
      },
      {
        "x": "subway",
        "y": 9
      },
      {
        "x": "bus",
        "y": 257
      },
      {
        "x": "car",
        "y": 10
      },
      {
        "x": "moto",
        "y": 256
      },
      {
        "x": "bicycle",
        "y": 108
      },
      {
        "x": "horse",
        "y": 94
      },
      {
        "x": "skateboard",
        "y": 11
      },
      {
        "x": "others",
        "y": 81
      }
    ]
  },
  {
    "id": "france",
    "color": "hsl(252, 70%, 50%)",
    "data": [
      {
        "x": "plane",
        "y": 108
      },
      {
        "x": "helicopter",
        "y": 72
      },
      {
        "x": "boat",
        "y": 70
      },
      {
        "x": "train",
        "y": 227
      },
      {
        "x": "subway",
        "y": 229
      },
      {
        "x": "bus",
        "y": 190
      },
      {
        "x": "car",
        "y": 284
      },
      {
        "x": "moto",
        "y": 19
      },
      {
        "x": "bicycle",
        "y": 209
      },
      {
        "x": "horse",
        "y": 235
      },
      {
        "x": "skateboard",
        "y": 41
      },
      {
        "x": "others",
        "y": 44
      }
    ]
  },
  {
    "id": "us",
    "color": "hsl(116, 70%, 50%)",
    "data": [
      {
        "x": "plane",
        "y": 274
      },
      {
        "x": "helicopter",
        "y": 79
      },
      {
        "x": "boat",
        "y": 48
      },
      {
        "x": "train",
        "y": 21
      },
      {
        "x": "subway",
        "y": 3
      },
      {
        "x": "bus",
        "y": 72
      },
      {
        "x": "car",
        "y": 250
      },
      {
        "x": "moto",
        "y": 237
      },
      {
        "x": "bicycle",
        "y": 288
      },
      {
        "x": "horse",
        "y": 183
      },
      {
        "x": "skateboard",
        "y": 159
      },
      {
        "x": "others",
        "y": 230
      }
    ]
  },
  {
    "id": "germany",
    "color": "hsl(180, 70%, 50%)",
    "data": [
      {
        "x": "plane",
        "y": 201
      },
      {
        "x": "helicopter",
        "y": 187
      },
      {
        "x": "boat",
        "y": 234
      },
      {
        "x": "train",
        "y": 137
      },
      {
        "x": "subway",
        "y": 66
      },
      {
        "x": "bus",
        "y": 83
      },
      {
        "x": "car",
        "y": 221
      },
      {
        "x": "moto",
        "y": 186
      },
      {
        "x": "bicycle",
        "y": 219
      },
      {
        "x": "horse",
        "y": 150
      },
      {
        "x": "skateboard",
        "y": 204
      },
      {
        "x": "others",
        "y": 94
      }
    ]
  },
  {
    "id": "norway",
    "color": "hsl(22, 70%, 50%)",
    "data": [
      {
        "x": "plane",
        "y": 145
      },
      {
        "x": "helicopter",
        "y": 70
      },
      {
        "x": "boat",
        "y": 182
      },
      {
        "x": "train",
        "y": 185
      },
      {
        "x": "subway",
        "y": 220
      },
      {
        "x": "bus",
        "y": 141
      },
      {
        "x": "car",
        "y": 146
      },
      {
        "x": "moto",
        "y": 72
      },
      {
        "x": "bicycle",
        "y": 8
      },
      {
        "x": "horse",
        "y": 3
      },
      {
        "x": "skateboard",
        "y": 9
      },
      {
        "x": "others",
        "y": 88
      }
    ]
  }
]

const MyResponsiveLine = ({ data /* see data tab */ }) => (
    <ResponsiveLine
        data={data}
        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
        xScale={{ type: 'point' }}
        yScale={{ type: 'linear', min: 'auto', max: 'auto', stacked: true, reverse: false }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
            orient: 'bottom',
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: 'transportation',
            legendOffset: 36,
            legendPosition: 'middle'
        }}
        axisLeft={{
            orient: 'left',
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: 'count',
            legendOffset: -40,
            legendPosition: 'middle'
        }}
        colors={{ scheme: 'nivo' }}
        pointSize={10}
        pointColor={{ theme: 'background' }}
        pointBorderWidth={2}
        pointBorderColor={{ from: 'serieColor' }}
        pointLabel="y"
        pointLabelYOffset={-12}
        useMesh={true}
        legends={[
            {
                anchor: 'bottom-right',
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
)

export default function Home() {
  const [data, setData] = useState([])

  function clean(data) {
    return data.map(function(x, i){ return [
      x["year"],
      x["elo_max"]
    ]});
  }

  useEffect(() => {
    const getTeam = async (team) => {
      const new_teams = await fetchTeam(team);
      setData(clean(new_teams.results));
    };

    getTeam(5511)
  }, [])


  console.log(data)

  return (
    <Jumbotron>
      <h1>Welcome to Statbotics.io!</h1>
      <h2>Modernizing FRC Data Analytics</h2>
      <p>
        Check the tabs above for tables and charts displaying ELO rankings for FRC teams. More coming soon!
      </p>
      <p>
        <Button variant="primary" className={styles.link}>
          <a href="/teams" className={styles.link}>Visit Tables</a>
        </Button>
      </p>
      <MyResponsiveLine data=countries/>
    </Jumbotron>
  );
}
