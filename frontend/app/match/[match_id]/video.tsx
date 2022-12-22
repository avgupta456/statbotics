import React from "react";

const Video = ({ video }: { video: string }) => {
  return (
    <div className="w-full lg:w-1/2">
      <div className="relative pb-[56.25%]">
        <iframe
          className="absolute top-0 left-0 w-full h-full"
          src={`https://www.youtube.com/embed/${video}`}
          title="YouTube video player"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      </div>
    </div>
  );
};

export default Video;
