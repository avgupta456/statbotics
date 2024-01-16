const axisOptionsGeneral = [
  {
    key: "total_points",
    label: "Total Points",
    accessor: (d: any) => d.epa?.total_points?.mean,
    units: "points",
    group: "General",
  },
];

const axisOptionsPost2016 = [
  {
    key: "teleop_points",
    label: "Teleop Points",
    accessor: (d: any) => d.epa?.breakdown?.teleop_points?.mean,
    units: "points",
    group: "Components",
  },
  {
    key: "auto_points",
    label: "Auto Points",
    accessor: (d: any) => d.epa?.breakdown?.auto_points?.mean,
    units: "points",
    group: "Components",
  },
  {
    key: "endgame_points",
    label: "Endgame Points",
    accessor: (d: any) => d.epa?.breakdown?.endgame_points?.mean,
    units: "points",
    group: "Components",
  },
];

const axisOptions2023 = [
  {
    key: "total_pieces",
    label: "Total Pieces",
    accessor: (d: any) => d.epa?.breakdown?.total_pieces?.mean,
    units: "pieces",
    group: "Breakdown",
  },
  {
    key: "links",
    label: "Links",
    accessor: (d: any) => d.epa?.breakdown?.links?.mean,
    units: "links",
    group: "Breakdown",
  },
  {
    key: "auto_pieces",
    label: "Auto Pieces",
    accessor: (d: any) => d.epa?.breakdown?.auto_pieces?.mean,
    units: "pieces",
    group: "Breakdown",
  },
  {
    key: "teleop_pieces",
    label: "Teleop Pieces",
    accessor: (d: any) => d.epa?.breakdown?.teleop_pieces?.mean,
    units: "pieces",
    group: "Breakdown",
  },
  {
    key: "bottom_pieces",
    label: "Bottom Pieces",
    accessor: (d: any) => d.epa?.breakdown?.bottom_pieces?.mean,
    units: "pieces",
    group: "Breakdown",
  },
  {
    key: "middle_pieces",
    label: "Middle Pieces",
    accessor: (d: any) => d.epa?.breakdown?.middle_pieces?.mean,
    units: "pieces",
    group: "Breakdown",
  },
  {
    key: "top_pieces",
    label: "Top Pieces",
    accessor: (d: any) => d.epa?.breakdown?.top_pieces?.mean,
    units: "pieces",
    group: "Breakdown",
  },
  {
    key: "cubes_scored",
    label: "Cubes Scored",
    accessor: (d: any) => d.epa?.breakdown?.cubes_scored?.mean,
    units: "pieces",
    group: "Breakdown",
  },
  {
    key: "cones_scored",
    label: "Cones Scored",
    accessor: (d: any) => d.epa?.breakdown?.cones_scored?.mean,
    units: "pieces",
    group: "Breakdown",
  },
];

const getAxisOptions = (year: number) => {
  if (year < 2016) {
    return axisOptionsGeneral;
  }
  if (year === 2017) {
    return [...axisOptionsGeneral, ...axisOptionsPost2016];
  }
  if (year === 2018) {
    return [...axisOptionsGeneral, ...axisOptionsPost2016];
  }
  if (year === 2019) {
    return [...axisOptionsGeneral, ...axisOptionsPost2016];
  }
  if (year === 2020) {
    return [...axisOptionsGeneral, ...axisOptionsPost2016];
  }
  if (year === 2021) {
    return [...axisOptionsGeneral, ...axisOptionsPost2016];
  }
  if (year === 2022) {
    return [...axisOptionsGeneral, ...axisOptionsPost2016];
  }
  if (year === 2023) {
    return [...axisOptionsGeneral, ...axisOptionsPost2016, ...axisOptions2023];
  }
  if (year === 2024) {
    return [...axisOptionsGeneral, ...axisOptionsPost2016];
  }
  return axisOptionsGeneral;
};

export default getAxisOptions;
