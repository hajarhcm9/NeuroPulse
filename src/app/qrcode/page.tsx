"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { isLoggedIn, getUserName } from "@/lib/auth";

export default function QRCodePage() {
  const router = useRouter();
  const [scanned, setScanned] = useState(false);
  const [countdown, setCountdown] = useState(5);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/");
      return;
    }
  }, [router]);

  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  const handleContinue = () => {
    setScanned(true);
    router.push("/dashboard");
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-8" style={{ background: "linear-gradient(180deg, #070B2B 0%, #0D1333 50%, #070B2B 100%)" }}>
      {/* Success Icon */}
      <div className="mb-6">
        <div className="w-16 h-16 rounded-full flex items-center justify-center" style={{ background: "rgba(52,199,89,0.15)", border: "2px solid rgba(52,199,89,0.3)" }}>
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#34C759" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M20 6 9 17l-5-5"/>
          </svg>
        </div>
      </div>

      {/* Title */}
      <h1 className="text-2xl font-bold text-white mb-2">Compte verifie !</h1>
      <p className="text-sm text-center mb-8 max-w-xs" style={{ color: "rgba(255,255,255,0.5)" }}>
        Bienvenue, <span style={{ color: "#7B61FF" }}>{typeof window !== "undefined" ? getUserName() : ""}</span>.<br/>
        Scannez ce QR code pour telecharger l&apos;application sur votre telephone.
      </p>

      {/* QR Code Container */}
      <div className="p-6 rounded-3xl mb-6" style={{ background: "white", boxShadow: "0 8px 32px rgba(123,97,255,0.2)" }}>
        <div className="w-56 h-56 relative flex items-center justify-center" style={{ background: "white" }}>
          {/* QR Code Pattern - SVG Generated */}
          <svg width="224" height="224" viewBox="0 0 224 224" fill="none">
            {/* Corner squares */}
            {/* Top-left */}
            <rect x="8" y="8" width="56" height="56" rx="4" stroke="#070B2B" strokeWidth="8" fill="none"/>
            <rect x="20" y="20" width="32" height="32" rx="2" fill="#070B2B"/>
            <rect x="28" y="28" width="16" height="16" rx="1" fill="#7B61FF"/>
            
            {/* Top-right */}
            <rect x="160" y="8" width="56" height="56" rx="4" stroke="#070B2B" strokeWidth="8" fill="none"/>
            <rect x="172" y="20" width="32" height="32" rx="2" fill="#070B2B"/>
            <rect x="180" y="28" width="16" height="16" rx="1" fill="#7B61FF"/>
            
            {/* Bottom-left */}
            <rect x="8" y="160" width="56" height="56" rx="4" stroke="#070B2B" strokeWidth="8" fill="none"/>
            <rect x="20" y="172" width="32" height="32" rx="2" fill="#070B2B"/>
            <rect x="28" y="180" width="16" height="16" rx="1" fill="#7B61FF"/>

            {/* Data pattern - row by row */}
            {/* Row 1 */}
            <rect x="76" y="12" width="8" height="8" fill="#070B2B"/>
            <rect x="92" y="12" width="8" height="8" fill="#070B2B"/>
            <rect x="108" y="12" width="8" height="8" fill="#7B61FF"/>
            <rect x="124" y="12" width="8" height="8" fill="#070B2B"/>
            <rect x="140" y="12" width="8" height="8" fill="#070B2B"/>
            
            {/* Row 2 */}
            <rect x="76" y="24" width="8" height="8" fill="#7B61FF"/>
            <rect x="84" y="24" width="8" height="8" fill="#070B2B"/>
            <rect x="100" y="24" width="8" height="8" fill="#070B2B"/>
            <rect x="116" y="24" width="8" height="8" fill="#7B61FF"/>
            <rect x="132" y="24" width="8" height="8" fill="#070B2B"/>
            <rect x="148" y="24" width="8" height="8" fill="#7B61FF"/>

            {/* Row 3 */}
            <rect x="76" y="36" width="8" height="8" fill="#070B2B"/>
            <rect x="92" y="36" width="8" height="8" fill="#7B61FF"/>
            <rect x="108" y="36" width="8" height="8" fill="#070B2B"/>
            <rect x="132" y="36" width="8" height="8" fill="#070B2B"/>
            <rect x="148" y="36" width="8" height="8" fill="#070B2B"/>

            {/* Row 4 */}
            <rect x="76" y="48" width="8" height="8" fill="#7B61FF"/>
            <rect x="84" y="48" width="8" height="8" fill="#7B61FF"/>
            <rect x="100" y="48" width="8" height="8" fill="#070B2B"/>
            <rect x="116" y="48" width="8" height="8" fill="#070B2B"/>
            <rect x="124" y="48" width="8" height="8" fill="#7B61FF"/>
            <rect x="140" y="48" width="8" height="8" fill="#070B2B"/>

            {/* Middle section */}
            <rect x="12" y="76" width="8" height="8" fill="#070B2B"/>
            <rect x="28" y="76" width="8" height="8" fill="#7B61FF"/>
            <rect x="44" y="76" width="8" height="8" fill="#070B2B"/>
            <rect x="60" y="76" width="8" height="8" fill="#070B2B"/>
            <rect x="76" y="76" width="8" height="8" fill="#7B61FF"/>
            <rect x="92" y="76" width="8" height="8" fill="#070B2B"/>
            <rect x="108" y="76" width="8" height="8" fill="#7B61FF"/>
            <rect x="124" y="76" width="8" height="8" fill="#070B2B"/>
            <rect x="140" y="76" width="8" height="8" fill="#7B61FF"/>
            <rect x="156" y="76" width="8" height="8" fill="#070B2B"/>
            <rect x="172" y="76" width="8" height="8" fill="#7B61FF"/>
            <rect x="196" y="76" width="8" height="8" fill="#070B2B"/>

            <rect x="20" y="88" width="8" height="8" fill="#7B61FF"/>
            <rect x="36" y="88" width="8" height="8" fill="#070B2B"/>
            <rect x="52" y="88" width="8" height="8" fill="#7B61FF"/>
            <rect x="84" y="88" width="8" height="8" fill="#070B2B"/>
            <rect x="100" y="88" width="8" height="8" fill="#7B61FF"/>
            <rect x="132" y="88" width="8" height="8" fill="#070B2B"/>
            <rect x="148" y="88" width="8" height="8" fill="#7B61FF"/>
            <rect x="164" y="88" width="8" height="8" fill="#070B2B"/>
            <rect x="188" y="88" width="8" height="8" fill="#7B61FF"/>
            <rect x="204" y="88" width="8" height="8" fill="#070B2B"/>

            {/* Center logo area */}
            <rect x="88" y="88" width="48" height="48" rx="8" fill="white" stroke="#7B61FF" strokeWidth="2"/>
            <path d="M112 96 L112 112 M104 104 L120 104" stroke="#7B61FF" strokeWidth="3" strokeLinecap="round"/>
            <circle cx="112" cy="108" r="4" fill="#7B61FF" fillOpacity="0.3"/>

            <rect x="20" y="100" width="8" height="8" fill="#070B2B"/>
            <rect x="36" y="100" width="8" height="8" fill="#7B61FF"/>
            <rect x="52" y="100" width="8" height="8" fill="#070B2B"/>
            <rect x="148" y="100" width="8" height="8" fill="#070B2B"/>
            <rect x="164" y="100" width="8" height="8" fill="#7B61FF"/>
            <rect x="188" y="100" width="8" height="8" fill="#070B2B"/>

            <rect x="12" y="112" width="8" height="8" fill="#7B61FF"/>
            <rect x="28" y="112" width="8" height="8" fill="#070B2B"/>
            <rect x="44" y="112" width="8" height="8" fill="#7B61FF"/>
            <rect x="60" y="112" width="8" height="8" fill="#070B2B"/>
            <rect x="148" y="112" width="8" height="8" fill="#7B61FF"/>
            <rect x="172" y="112" width="8" height="8" fill="#070B2B"/>
            <rect x="196" y="112" width="8" height="8" fill="#7B61FF"/>

            <rect x="20" y="124" width="8" height="8" fill="#070B2B"/>
            <rect x="36" y="124" width="8" height="8" fill="#7B61FF"/>
            <rect x="52" y="124" width="8" height="8" fill="#070B2B"/>
            <rect x="76" y="124" width="8" height="8" fill="#7B61FF"/>
            <rect x="92" y="124" width="8" height="8" fill="#070B2B"/>
            <rect x="140" y="124" width="8" height="8" fill="#7B61FF"/>
            <rect x="164" y="124" width="8" height="8" fill="#070B2B"/>
            <rect x="188" y="124" width="8" height="8" fill="#7B61FF"/>
            <rect x="204" y="124" width="8" height="8" fill="#070B2B"/>

            {/* Bottom section */}
            <rect x="76" y="148" width="8" height="8" fill="#070B2B"/>
            <rect x="92" y="148" width="8" height="8" fill="#7B61FF"/>
            <rect x="108" y="148" width="8" height="8" fill="#070B2B"/>
            <rect x="132" y="148" width="8" height="8" fill="#070B2B"/>
            <rect x="148" y="148" width="8" height="8" fill="#7B61FF"/>

            <rect x="76" y="160" width="8" height="8" fill="#7B61FF"/>
            <rect x="84" y="160" width="8" height="8" fill="#070B2B"/>
            <rect x="100" y="160" width="8" height="8" fill="#7B61FF"/>
            <rect x="116" y="160" width="8" height="8" fill="#070B2B"/>
            <rect x="132" y="160" width="8" height="8" fill="#7B61FF"/>
            <rect x="148" y="160" width="8" height="8" fill="#070B2B"/>
            <rect x="164" y="160" width="8" height="8" fill="#7B61FF"/>
            <rect x="180" y="160" width="8" height="8" fill="#070B2B"/>
            <rect x="196" y="160" width="8" height="8" fill="#7B61FF"/>
            <rect x="204" y="160" width="8" height="8" fill="#070B2B"/>

            <rect x="76" y="172" width="8" height="8" fill="#070B2B"/>
            <rect x="92" y="172" width="8" height="8" fill="#7B61FF"/>
            <rect x="108" y="172" width="8" height="8" fill="#070B2B"/>
            <rect x="124" y="172" width="8" height="8" fill="#7B61FF"/>
            <rect x="148" y="172" width="8" height="8" fill="#070B2B"/>
            <rect x="164" y="172" width="8" height="8" fill="#7B61FF"/>
            <rect x="180" y="172" width="8" height="8" fill="#070B2B"/>
            <rect x="204" y="172" width="8" height="8" fill="#070B2B"/>

            <rect x="76" y="188" width="8" height="8" fill="#7B61FF"/>
            <rect x="84" y="188" width="8" height="8" fill="#070B2B"/>
            <rect x="100" y="188" width="8" height="8" fill="#070B2B"/>
            <rect x="116" y="188" width="8" height="8" fill="#7B61FF"/>
            <rect x="132" y="188" width="8" height="8" fill="#070B2B"/>
            <rect x="140" y="188" width="8" height="8" fill="#7B61FF"/>
            <rect x="164" y="188" width="8" height="8" fill="#070B2B"/>
            <rect x="188" y="188" width="8" height="8" fill="#7B61FF"/>

            <rect x="76" y="204" width="8" height="8" fill="#070B2B"/>
            <rect x="92" y="204" width="8" height="8" fill="#7B61FF"/>
            <rect x="108" y="204" width="8" height="8" fill="#070B2B"/>
            <rect x="124" y="204" width="8" height="8" fill="#7B61FF"/>
            <rect x="140" y="204" width="8" height="8" fill="#070B2B"/>
            <rect x="172" y="204" width="8" height="8" fill="#7B61FF"/>
            <rect x="196" y="204" width="8" height="8" fill="#070B2B"/>
          </svg>
        </div>
      </div>

      {/* Scan instruction */}
      <p className="text-sm mb-6 text-center" style={{ color: "rgba(255,255,255,0.5)" }}>
        Ouvrez l&apos;appareil photo de votre telephone<br/>et scannez ce code pour telecharger
      </p>

      {/* Download buttons */}
      <div className="flex gap-3 mb-8 w-full max-w-sm">
        <button className="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl text-white text-sm font-medium" style={{ background: "rgba(255,255,255,0.08)", border: "1px solid rgba(255,255,255,0.1)" }}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
          iOS
        </button>
        <button className="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl text-white text-sm font-medium" style={{ background: "rgba(255,255,255,0.08)", border: "1px solid rgba(255,255,255,0.1)" }}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M3.18 23.75c.55.98 1.6.98 2.15 0l2.27-3.98-2.15-3.78c-.55-.98-1.6-.98-2.15 0L.76 20.03c-.55.98.87 3.72 2.42 3.72zM17.6 15.23l-4.93-8.66c-.55-.98-1.6-.98-2.15 0L5.6 15.23c-.55.98.87 3.72 2.42 3.72h7.16c1.55 0 2.97-2.74 2.42-3.72z"/></svg>
          Android
        </button>
      </div>

      {/* Continue button */}
      <button
        onClick={handleContinue}
        className="btn-primary w-full max-w-sm flex items-center justify-center gap-2"
      >
        <span>Acceder a l&apos;application</span>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
      </button>

      {/* Auto redirect countdown */}
      {countdown > 0 && (
        <p className="mt-4 text-xs" style={{ color: "rgba(255,255,255,0.3)" }}>
          Redirection automatique dans {countdown}s
        </p>
      )}
    </div>
  );
}
