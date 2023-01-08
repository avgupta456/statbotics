import React from "react";

const Page = () => {
  return (
    <div className="w-4/5 mx-auto">
      <div className="w-full h-full py-16 prose prose-slate max-w-none">
        <h2 className="w-full text-center">The EPA Model</h2>
        <p className="lead">
          The Expected Points Added (EPA) model builds upon the Elo rating system, and provides
          strong prediction accuracy, interpretability, and accessibility. Let&apos;s dive into the
          details!
        </p>
        <h3>Motivation</h3>
        <p>In 2022, Statbotics displayed both Elo and OPR ratings for each team.</p>
        <h3>Derivation from Elo</h3>
        <h3>Modifications</h3>
        <h3>Component EPA</h3>
        <h3>Ranking Point Predictions</h3>
        <h3>Year Normalized EPA</h3>
      </div>
    </div>
  );
};

export default Page;
