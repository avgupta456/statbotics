import React from "react";

const NotFound = ({ type }: { type: string }) => {
  return (
    <div className="w-full flex-grow flex flex-col justify-center items-center gap-2">
      <div className="text-xl lg:text-2xl">{type} not found</div>
      <div className="text-xl lg:text-2xl">¯\_(ツ)_/¯</div>
    </div>
  );
};

export default NotFound;
