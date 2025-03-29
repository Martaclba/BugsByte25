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
    <div className="flex flex-col w-full bg-white min-h-screen px-4">
      <div className="flex flex-row w-full justify-between items-center py-10">
        <div className="text-black/70 text-3xl">Bundly</div>
        <Image src="/logo.png" alt="logo" width={32} height={32} />
      </div>

      {/* Bundles */}
      {bundles.map((b: BundleOverview) => 
        <div key={b.bundle_id} className="text-black shadow py-2 px-4 rounded-lg flex flex-row gap-4 w-full relative">
          <div className="absolute h-full w-1.5 bg-red-600 left-0 top-0 rounded-l-lg"></div>
          
          <Image 
            src={"/receita.jpg"} 
            alt="receita" 
            className="w-1/3 h-32 rounded-lg ml-1" 
            width={32} 
            height={32} 
          />
          
          <div className="flex flex-col w-2/3">
            <div className="text-lg">{b.title}</div>
            <div className="text-black/50 text-sm text-justify">{b.description}</div>          
          </div>
        </div>
      )}

    </div>
  );
}