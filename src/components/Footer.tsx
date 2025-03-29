import Image from "next/image";

export default function Footer(){
    return(
        <div className="w-full px-6 mt-10">
          <div className="border-t border-black/20 py-2 flex flex-row justify-end items-center gap-2">
            <p className="text-black text-xs">Made with love</p>
            <p className="text-black text-xs">©</p>
            <a href="https://www.youtube.com/watch?v=CXEIsUPpeI4&t=732s"><Image src="/wiwiwi.png" alt="Ver receita" width={32} height={32} className="cursor-pointer"/></a>
          </div>
      </div>
    )
}