import Image from "next/image";

import { classnames } from "../utils";

export default function Home() {
  return (
    <div className="w-full p-8 flex">
      <div className="w-1/2 h-[400px] relative">
        <Image src="/spline.png" alt="Summary" fill quality={100} className="object-contain" />
      </div>
      <div className="w-1/2 h-[400px] p-4 flex flex-col justify-center items-center text-gray-800">
        <div
          className={classnames(
            "text-5xl font-thin flex flex-col items-center",
            "text-transparent bg-clip-text bg-gradient-to-r from-gradientRed via-violet-500 to-gradientBlue"
          )}
        >
          <div className="mb-1">Modernizing FRC</div>
          <div className="mb-4">Data Analytics</div>
        </div>
        <div className="text-lg p-4">
          Our Expected Points Added (EPA) model improves upon existing metrics and is displayed
          through tables, charts, and Python API.
        </div>
      </div>
    </div>
  );
}
