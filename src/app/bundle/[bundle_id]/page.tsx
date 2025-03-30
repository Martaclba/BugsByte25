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

function Loading({}) {
  return <div className="flex m-36 justify-center h-screen">
    <svg aria-hidden="true" className="w-48 h-48 text-gray-200 animate-spin fill-red-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
    </svg>
    <span className="sr-only">Loading...</span>
  </div>;
}

export default function BundlePage({params} : { params: Promise<{ bundle_id: string }> }) {
  const router = useRouter();
  const { bundle_id } = use(params);
  const [bundle, setBundle] = useState<Bundle|undefined>();
  const [selectedItems, setSelectedItems] = useState<number[]>([]);

  const toggleItemSelection = (productId: number) => {
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

      { bundle === undefined && <Loading /> }

      { bundle !== undefined &&
      <>
        <div className="flex flex-row w-full justify-between items-center py-2">
          <div className="text-black/70 text-2xl">{bundle?.name}</div>
        </div>
        
        <Image
          src={bundle?.image_url ?? "/image-missing.svg"}
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
                  <div className="rounded relative w-3/4 h-14">
                    <Image src={i?.product.image_url ?? "/image-missing.svg"} alt="<?>" fill objectFit="cover" className="rounded-sm"/>
                  </div>
                </td>
                <td className="w-8">{i.quantity}x</td>
                <td className="">{i.product.name}</td>
                {/*<td className="w-15">
                  <Price product={i.product}/>
                </td>*/}
              </tr>
            ))}
          </tbody>
        </table>

        <h2 className="font-bold">Confeção</h2>
        
        <div className="flex flex-col gap-1">
          {bundle?.instructions?.split('\n').map((instruction, index) => (
            instruction.trim() && (
              <p key={index} className="text-black/90 text-justify">
                {instruction.trim()}
              </p>
            )
          ))}
        </div>

        {/*<p className="mx-auto">Código: {bundle?.bundle_id}</p>*/}
        <div className="flex flex-row w-full justify-center items-center py-2">
          <button className="cursor-pointer flex rounded-full p-3 mx-4 items-center justify-center bg-gray-300">
            <Image src="/like.svg" alt="like" width={25} height={25}/>
          </button>
          <button className="cursor-pointer flex rounded-full p-3 mx-4 items-center justify-center bg-gray-300">
            <Image src="/print.svg" alt="print" width={25} height={25}/>
          </button>
        </div>
      </>
      }
      
    </div>
    <Footer />
  </div>;
}