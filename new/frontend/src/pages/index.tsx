import Image from "next/image";
import Link from "next/link";

import { Button } from "@mantine/core";

import { classnames } from "../utils/utils";

export default function LandingPage() {
  return (
    <div className="container mx-auto flex w-full flex-grow flex-wrap items-center p-4">
      <div className="relative hidden h-[400px] w-1/2 lg:block">
        <Image
          src="/spline.png"
          alt="Summary"
          fill
          quality={100}
          priority
          className="object-contain"
        />
      </div>
      <div className="flex w-full flex-col items-center justify-center p-4 pb-12 lg:h-[400px] lg:w-1/2">
        <div
          className={classnames(
            "flex flex-col items-center text-2xl sm:text-4xl md:text-5xl",
            "bg-gradient-to-r from-gradientRed via-violet-500 to-gradientBlue bg-clip-text text-transparent",
          )}
        >
          <div className="mb-1">Modernizing FRC</div>
          <div className="mb-4">Data Analytics</div>
        </div>
        <div className="mb-4 text-center text-sm sm:p-4 sm:text-base xl:w-2/3">
          The <strong>Expected Points Added (EPA)</strong> metric is a highly predictive measure of
          team performance. Use our live-updating data to find actionable insights or analyze
          historical trends.
        </div>
        <div className="flex flex-row items-center justify-center">
          <Button component={Link} href="/teams" className="mr-4">
            Explore Teams
          </Button>
          <Button component={Link} href="/blog">
            Read Blog
          </Button>
        </div>
      </div>
      <div className="relative h-[400px] w-full lg:hidden">
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
