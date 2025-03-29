"use client"

import { Bundle } from "@/lib/bundle"
import { get_bundle } from "@/lib/endpoints";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react"
import Image from "next/image";

import { use } from 'react';

export default function BundlePage({params} : { params: Promise<{ bundle_id: string }> }) {
  const router = useRouter();
  const { bundle_id } = use(params);
  const [bundle, setBundle] = useState<Bundle|undefined>();
  
  useEffect(() => {
      const fetchBundle = async () => setBundle(await get_bundle("1234", bundle_id));
      fetchBundle();
    }, []);

  return <div className="flex flex-col w-full bg-white min-h-screen px-4">
    <button onClick={() => router.back()}>
      &#8592;
    </button>
    {/*<h1 className="text-black/70 text-3xl">Bundly</h1>*/}

    <div className="text-black shadow my-8 py-2 px-4 rounded-lg flex flex-col gap-4 w-full relative">
      <div className="absolute top-0 left-0 bg-red-600 w-full h-1.5 rounded-t-lg"></div>

      <div className="flex flex-row w-full justify-between items-center py-2">
        <div className="text-black/70 text-2xl">{bundle?.overview.title}</div>
        {/*<input type="checkbox"/>*/}
      </div>
      
      <Image
        src={"/receita.jpg"}
        alt="receita"
        className="w-2/3 rounded-lg mx-auto"
        width={100}
        height={100}
      />

      <p className="text-black/50 text-sm text-justify">{bundle?.overview.description}</p>

      <table className="table-auto">
        <tbody>
          {bundle?.items.map((i) =>
            <tr key={i.product.product_id} className="py-2">
              <td>{i.quantity}x</td>
              <td>{i.product.name}</td>
              
              <td>{i.product.price}€</td>
            </tr>
          )}
        </tbody>
      </table>
      
      <p className="text-black/50 text-sm text-justify">{bundle?.instructions}</p>

      <p className="mx-auto">Código: TODO</p>
      <div className="flex flex-row w-full justify-center items-center py-2">
        <div className="flex rounded-full p-3 mx-4 items-center justify-center bg-gray-300">
          <Image src="/like.svg" alt="like" width={40} height={40}/>
        </div>
        <div className="flex rounded-full p-3 mx-4 items-center justify-center bg-gray-300">
          <Image src="/print.svg" alt="print" width={40} height={40}/>
        </div>
        
      </div>
    </div>
  </div>;
}