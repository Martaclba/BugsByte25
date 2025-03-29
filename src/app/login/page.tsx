"use client"

import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Login() {
    const [username, setUsername] = useState("");
    const router = useRouter();

    const handleLogin = () => {
        localStorage.setItem("username", username);
        router.push("/");
    };

    return (
        <div className="flex flex-col justify-center items-center min-h-screen w-full">
            <div className="flex flex-col w-2/3 shadow-lg h-full items-center justify-center px-4 py-10 gap-2">
                <div className="flex flex-row gap-4 items-center justify-center h-full">
                    <Image src="/logo.png" alt="logo" width={40} height={40} className="-mt-4"/>
                    <p className="text-3xl font-bold mb-6">Bundly</p>
                </div>             
                <input 
                    type="text" 
                    className="px-2 py-0.5 border border-black/40 rounded text-sm text-black focus:outline-none placeholder:text-black/40 w-full" 
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input 
                    type="password" 
                    className="px-2 py-0.5 border border-black/40 rounded text-sm text-black focus:outline-none placeholder:text-black/40 w-full" 
                    placeholder="Password"
                />
                <button 
                    className="px-2 py-0.5 text-white bg-red-500 font-bold rounded w-full"
                    onClick={handleLogin}
                >
                    Login
                </button>
            </div>
        </div>
    )
}