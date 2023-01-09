import React from "react";

const PageLayout = ({ title, lead, children }) => {
  return (
    <div className="w-4/5 mx-auto">
      <div className="w-full h-full py-16 prose prose-slate max-w-none">
        <h2 className="w-full text-center">{title}</h2>
        <p className="lead">{lead}</p>
        {children}
      </div>
    </div>
  );
};

export default PageLayout;
