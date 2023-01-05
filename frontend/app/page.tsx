import Image from "next/image";

export default function Home() {
  return (
    <div className="w-full flex">
      <div className="w-1/2 h-full">test</div>
      <div className="w-1/2 h-screen">
        <div className="w-full h-[500px] relative">
          <Image src="/spline.png" alt="Summary" fill quality={100} className="object-contain" />
        </div>
      </div>
    </div>
  );
}
