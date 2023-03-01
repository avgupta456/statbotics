import Image from "next/image";
import Link from "next/link";

import { classnames } from "../utils";

export default function Home() {
  return (
    <div className="w-full container mx-auto flex-grow p-4 flex flex-wrap items-center">
      <div className="w-1/2 h-[400px] hidden lg:block relative">
        <Image
          src="/spline.png"
          alt="Summary"
          fill
          quality={100}
          priority
          className="object-contain"
        />
      </div>
      <div className="w-full lg:w-1/2 lg:h-[400px] p-4 pb-12 flex flex-col justify-center items-center text-gray-800">
        <div
          className={classnames(
            "text-2xl sm:text-4xl md:text-5xl font-thin flex flex-col items-center",
            "text-transparent bg-clip-text bg-gradient-to-r from-gradientRed via-violet-500 to-gradientBlue"
          )}
        >
          <div className="mb-1">Modernizing FRC</div>
          <div className="mb-4">Data Analytics</div>
        </div>
        <div className="text-sm sm:text-base sm:p-4 xl:w-2/3 text-center mb-4">
          Our novel <strong>Expected Points Added (EPA)</strong> metric is a highly predictive
          measure of team performance. Use our live-updating data to find actionable insights or
          analyze historical trends.
        </div>
        <div className="flex flex-row justify-center items-center">
          <Link
            href="/teams"
            className="text-sm sm:text-base py-2 px-4 sm:px-6 rounded-sm bg-gray-700 hover:bg-gray-800 text-white"
          >
            Explore Teams
          </Link>
          <Link
            href="/blog"
            className="text-sm sm:text-base py-2 px-4 sm:px-6 ml-4 rounded-sm bg-gray-100 hover:bg-gray-200 text-gray-800"
          >
            Read Blog
          </Link>
        </div>
      </div>
      <div className="w-full h-[400px] lg:hidden relative">
        <Image
          src="/spline.png"
          alt="Summary"
          fill
          quality={100}
          priority
          className="object-contain"
        />
      </div>
    </div>
  );
}
