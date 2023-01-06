import Image from "next/image";
import Link from "next/link";

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
        <div className="text-base p-4 text-center mb-4">
          Our novel <strong>Expected Points Added (EPA)</strong> metric is a highly predictive
          measure of team performance. Use our live-updating data to find actionable insights or
          analyze historical trends.
        </div>
        <div className="flex flex-row justify-center items-center">
          <Link
            href="/teams"
            className="text-base py-2 px-6 rounded-sm bg-gray-700 hover:bg-gray-800 text-white"
          >
            Explore Teams
          </Link>
          <Link
            href="/blog"
            className="text-base py-2 px-6 ml-4 rounded-sm bg-gray-100 hover:bg-gray-200 text-gray-800"
          >
            Read Docs
          </Link>
        </div>
      </div>
    </div>
  );
}
