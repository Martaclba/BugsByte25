"use client"

import { BundleOverview } from "@/lib/bundle";
import { get_bundles } from "@/lib/endpoints";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {

  const [bundles, setBundles] = useState<BundleOverview[]>([]);

  useEffect(() => {
    const fetchBundles = async () => {
      const data = await get_bundles("1234"); 
      setBundles(data);
    };

    fetchBundles();
  }, []);

  return (
    <div className="flex flex-col w-full bg-white min-h-screen">
      <div className="flex flex-row w-full justify-between items-center py-6 bg-red-500 px-4">
        <div className="flex flex-row items-center gap-2">
          <Image src="/logo.png" alt="logo" width={40} height={40}  className="bg-white p-1 rounded-full"/>
          <p className="text-white font-extrabold text-2xl">Bundly</p>
        </div>
      </div>
      <div className="flex flex-col gap-3 h-max px-4 mt-4">
        {/* Bundles */}
        {bundles.map((b: BundleOverview) => 
          <div key={b.bundle_id} className="text-black shadow py-2 px-4 rounded-lg flex flex-row gap-4 w-full relative h-full">
            <div className="absolute h-full w-1.5 bg-red-600 left-0 top-0 rounded-l-lg"></div>
            
            <Image 
              src={"/receita.jpg"} 
              alt="receita" 
              className="w-1/3 h-32 rounded-lg ml-1" 
              width={32} 
              height={32} 
            />
            
            <div className="flex flex-col w-2/3 h-full">
              <div className="flex flex-row justify-between items-center">
                <p>{b.title}</p>
                {/* <p className="font-extrabold text-xs text-white bg-red-600 px-1 rounded">Temporário</p> */}
              </div>
              <div className="text-black/50 text-xs text-justify">{b.description}</div>
              <div className="flex justify-end mt-4 text-white w-full text-sm" >
                <a href="https://www.youtube.com/watch?v=CXEIsUPpeI4&t=728s" className=" cursor-pointer"><Image src="/chevronright.svg" alt="Ver receita" width={16} height={16}/></a>
              </div>          
            </div>
          </div>
        )}
      </div>
    </div>
  );
}