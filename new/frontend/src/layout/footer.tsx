import Image from "next/image";
import Link from "next/link";

function Footer() {
  return (
    <footer className="w-full border-t border-gray-300 pb-2 pt-3 text-center text-gray-600">
      <p className="flex h-4 items-center justify-center gap-1 text-xs sm:h-5 sm:text-sm lg:h-6 lg:text-base">
        Powered by{" "}
        <Link
          href="https://www.thebluealliance.com/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 hover:underline"
        >
          The Blue Alliance
        </Link>
        <Link
          href="https://www.thebluealliance.com/"
          target="_blank"
          rel="noopener noreferrer"
          className="relative mx-1 h-4 w-4 sm:h-5 sm:h-5 lg:h-6 lg:w-6"
        >
          <Image src="/tba.png" alt="TBA" unoptimized fill className="object-contain" />
        </Link>
      </p>
    </footer>
  );
}

export default Footer;
