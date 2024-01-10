const processTeamYear = (teamYear: any) => {
  const newTeamYear = teamYear;

  if (teamYear?.year === 2023) {
    console.log("HERE", teamYear);
    const autoBotCubes = teamYear?.epa?.breakdown?.auto_bottom_cubes;
    const autoBotCones = teamYear?.epa?.breakdown?.auto_bottom_cones;
    const autoMidCubes = teamYear?.epa?.breakdown?.auto_middle_cubes;
    const autoMidCones = teamYear?.epa?.breakdown?.auto_middle_cones;
    const autoTopCubes = teamYear?.epa?.breakdown?.auto_top_cubes;
    const autoTopCones = teamYear?.epa?.breakdown?.auto_top_cones;
    const teleBotCubes = teamYear?.epa?.breakdown?.teleop_bottom_cubes;
    const teleBotCones = teamYear?.epa?.breakdown?.teleop_bottom_cones;
    const teleMidCubes = teamYear?.epa?.breakdown?.teleop_middle_cubes;
    const teleMidCones = teamYear?.epa?.breakdown?.teleop_middle_cones;
    const teleTopCubes = teamYear?.epa?.breakdown?.teleop_top_cubes;
    const teleTopCones = teamYear?.epa?.breakdown?.teleop_top_cones;
    const totalPiecesMean =
      (autoBotCubes?.mean ?? 0) +
      (autoBotCones?.mean ?? 0) +
      (autoMidCubes?.mean ?? 0) +
      (autoMidCones?.mean ?? 0) +
      (autoTopCubes?.mean ?? 0) +
      (autoTopCones?.mean ?? 0) +
      (teleBotCubes?.mean ?? 0) +
      (teleBotCones?.mean ?? 0) +
      (teleMidCubes?.mean ?? 0) +
      (teleMidCones?.mean ?? 0) +
      (teleTopCubes?.mean ?? 0) +
      (teleTopCones?.mean ?? 0);

    const totalPiecesSd =
      ((teamYear?.epa?.breakdown?.auto_bottom_cubes?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.auto_bottom_cones?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.auto_middle_cubes?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.auto_middle_cones?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.auto_top_cubes?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.auto_top_cones?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.teleop_bottom_cubes?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.teleop_bottom_cones?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.teleop_middle_cubes?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.teleop_middle_cones?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.teleop_top_cubes?.sd ?? 0) ** 2 +
        (teamYear?.epa?.breakdown?.teleop_top_cones?.sd ?? 0) ** 2) **
      0.5;

    if (newTeamYear?.epa?.breakdown) {
      newTeamYear.epa.breakdown.total_pieces = {
        mean: totalPiecesMean,
        sd: totalPiecesSd,
      };
    }
  }

  return newTeamYear;
};

export default processTeamYear;
