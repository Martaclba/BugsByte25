"use client"

import { Bundle, BundleItem, Product } from "@/lib/bundle";
import { get_bundle } from "@/lib/endpoints";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import Footer from "@/components/Footer";
import { use } from 'react';

function Price({product}: {product: Product}) {
  if (product.base_price == product.price) {
    return <p className="text-sm text-right">{product.price}€</p>;
  } else {
    return <div className="flex flex-row items-center justify-center gap-2">
      <span className="text-xs text-gray-500 line-through">{product.base_price}€</span>
      <span className="text-sm"> {product.price}€</span>
    </div>;
  }
}

export default function BundlePage({params} : { params: Promise<{ bundle_id: string }> }) {
  const router = useRouter();
  const { bundle_id } = use(params);
  const [bundle, setBundle] = useState<Bundle|undefined>();
  const [selectedItems, setSelectedItems] = useState<string[]>([]);

  const toggleItemSelection = (productId: string) => {
    setSelectedItems(prev => 
      prev.includes(productId)
        ? prev.filter(id => id !== productId) // Remove se já estiver selecionado
        : [...prev, productId] // Adiciona se não estiver selecionado
    );
  };
  
  useEffect(() => {
      const fetchBundle = async () => setBundle(await get_bundle("1234", bundle_id));
      fetchBundle();
    }, [bundle_id]);

  return <div className="flex flex-col w-full bg-white min-h-screen p-4">
    <button onClick={() => router.back()} className="cursor-pointer w-fit">
      <Image
        src="/chevronleft.svg"
        alt="back"
        width={26}
        height={26}
      />
    </button>
    {/*<h1 className="text-black/70 text-3xl">Bundly</h1>*/}

    <div className="text-black shadow my-4 py-3 px-4 rounded-lg flex flex-col gap-4 w-full relative">
      <div className="absolute top-0 left-0 bg-[#eb0203] w-full h-1.5 rounded-t-lg"></div>

      <div className="flex flex-row w-full justify-between items-center py-2">
        <div className="text-black/70 text-2xl">{bundle?.name}</div>
      </div>
      
      <Image
        src={"/receita.jpg"}
        alt="receita"
        className="w-2/3 rounded-lg mx-auto"
        width={128}
        height={128}
      />

      <p className="text-black/50 text-justify">{bundle?.description}</p>

      <table className="table-fixed border-separate border-spacing-y-3">
        <tbody>
          {bundle?.items.map((i: BundleItem) => (
            <tr 
              key={i.product.product_id}
              onClick={() => toggleItemSelection(i.product.product_id)}
              className={`
                transition-all duration-200
                ${selectedItems.includes(i.product.product_id) ? 
                  'opacity-50' : 
                  'hover:bg-black/5 hover:shadow-sm hover:border hover:border-black/5'}
                cursor-pointer
              `}
            >
              <td className="w-20">
                <div className="rounded relative w-3/4 h-14 bg-black">
                  <Image src={i?.product.image_url ?? "/image-missing.svg"} alt="<?>" fill objectFit="cover" className="rounded-sm"/>
                </div>
              </td>
              <td className="w-6">{i.quantity}x</td>
              <td className="">{i.product.name}</td>
              <td className="w-15">
                <Price product={i.product}/>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <div className="flex flex-col gap-1">
        {bundle?.instructions?.split('\n').map((instruction, index) => (
          instruction.trim() && (
            <p key={index} className="text-black/90 text-justify">
              {instruction.trim()}
            </p>
          )
        ))}
      </div>

      <p className="mx-auto">Código: {bundle?.bundle_id}</p>
      <div className="flex flex-row w-full justify-center items-center py-2">
        <button onClick={() => console.log("ola")} className="cursor-pointer flex rounded-full p-3 mx-4 items-center justify-center bg-gray-300">
          <Image src="/like.svg" alt="like" width={25} height={25}/>
        </button>
        <button className="cursor-pointer flex rounded-full p-3 mx-4 items-center justify-center bg-gray-300">
          <Image src="/print.svg" alt="print" width={25} height={25}/>
        </button>
      </div>
    </div>
    <Footer />
  </div>;
}