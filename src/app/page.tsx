"use client"

import Footer from "@/components/Footer";
import { BundleOverview } from "@/lib/bundle";
import { get_bundles } from "@/lib/endpoints";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Home() {
  const [bundles, setBundles] = useState<BundleOverview[]>([]);
  const [search, setSearch] = useState("");
  const [showSearch, setShowSearch] = useState(false);
  const router = useRouter();

  const user_id = localStorage.getItem("username");

  useEffect(() => {
    if (!user_id) {
      router.push("/login");
      return;
    }

    const fetchBundles = async () => {
      try {
        const data = await get_bundles(user_id); 
        setBundles(data);
      } catch (error) {
        console.error("Failed to fetch bundles:", error);
      }
    };

    fetchBundles();
  }, [user_id, router]);

  if (!user_id) {
    return null;
  }

  const filteredBundles = bundles.filter((b) => 
    b.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="flex flex-col w-full bg-white min-h-screen">
      <div className="flex flex-row w-full justify-between items-center py-6 bg-red-500 px-4 md:px-40 relative">
        <div className="flex flex-row items-center gap-2">
          <Image src="/logo.png" alt="logo" width={40} height={40} className="bg-white p-1 rounded-full"/>
          <p className="text-white font-extrabold text-2xl">Bundly</p>
        </div>
        <div className="flex flex-row items-center gap-3">
          {showSearch ? (
            <input 
              type="text" 
              placeholder="" 
              className="px-2 py-0.5 md:px-4 md:py-1 bg-white rounded-lg text-xs text-black focus:outline-none placeholder:text-black w-40 md:w-96"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          ) : <div></div>
          }
          <Image 
            src="/search.svg" 
            alt="search" 
            width={23} 
            height={23} 
            className="cursor-pointer"
            onClick={() => setShowSearch(!showSearch)}
          />
          <a href={`/login`}><Image src="/person.svg" alt="profile" width={23} height={23}/></a>
        </div>
      </div>
      
      <div className="flex flex-col gap-3 h-max md:px-[500px] px-4 mt-4 items-center justify-center">
        {filteredBundles.map((b: BundleOverview) => (
          <div key={b.bundle_id} className="text-black shadow border border-black/5 py-2 px-4 rounded-lg flex flex-row gap-4 w-full relative h-full">
            <div className="absolute h-full w-1.5 bg-red-600 left-0 top-0 rounded-l-lg"></div>
            
            <Image 
              src="/receita.jpg" 
              alt="receita" 
              className="w-1/3 h-32 rounded-lg ml-1" 
              width={32} 
              height={32} 
            />
            
            <div className="flex flex-col w-2/3 h-full">
              <div className="flex flex-row justify-between items-center">
                <p>{b.title}</p>
              </div>
              <div className="text-black/50 text-xs text-justify">{b.description}</div>
              <div className="flex justify-end mt-4 text-white w-full text-sm" >
                <a 
                  href={`/bundle/${b.bundle_id}`} 
                  className="cursor-pointer"
                >
                  <Image src="/chevronright.svg" alt="Ver receita" width={16} height={16}/>
                </a>
              </div>          
            </div>
          </div>
        ))}
      </div>
      <Footer/>
    </div>
  );
}
