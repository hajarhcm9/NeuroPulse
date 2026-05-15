"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { verifyCode, needsVerification, getUserName } from "@/lib/auth";

export default function VerifyPage() {
  const router = useRouter();
  const [codes, setCodes] = useState<string[]>(["", "", "", "", "", ""]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [resendTimer, setResendTimer] = useState(30);
  const [email, setEmail] = useState("votre@email.com");
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    if (!needsVerification()) {
      router.push("/dashboard");
      return;
    }
    
    const stored = typeof window !== "undefined" ? localStorage.getItem("smart_guardian_user") : null;
    if (stored) {
      const userData = JSON.parse(stored);
      setEmail(userData.email || "votre@email.com");
    }
  }, [router]);

  useEffect(() => {
    if (resendTimer > 0) {
      const timer = setTimeout(() => setResendTimer(resendTimer - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [resendTimer]);

  const handleChange = (index: number, value: string) => {
    if (value.length > 1) return;
    
    const newCodes = [...codes];
    newCodes[index] = value;
    setCodes(newCodes);
    setError("");

    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }

    if (newCodes.every(c => c !== "")) {
      handleVerify(newCodes.join(""));
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === "Backspace" && !codes[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const paste = e.clipboardData.getData("text").slice(0, 6);
    if (/^\d+$/.test(paste)) {
      const newCodes = paste.split("").concat(Array(6 - paste.length).fill(""));
      setCodes(newCodes);
      if (paste.length === 6) {
        handleVerify(paste);
      }
    }
  };

  const handleVerify = async (code: string) => {
    setError("");
    setLoading(true);

    await new Promise(r => setTimeout(r, 1000));

    const result = verifyCode(code);
    
    if (result.success) {
      router.push("/qrcode");
    } else {
      setError(result.message);
      setLoading(false);
    }
  };

  const handleResend = () => {
    setResendTimer(30);
    setCodes(["", "", "", "", "", ""]);
    setError("");
    inputRefs.current[0]?.focus();
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-8" style={{ background: "linear-gradient(180deg, #070B2B 0%, #0D1333 50%, #070B2B 100%)" }}>
      {/* Icon */}
      <div className="mb-6">
        <div className="w-16 h-16 rounded-2xl flex items-center justify-center" style={{ background: "rgba(123,97,255,0.15)", border: "1px solid rgba(123,97,255,0.3)" }}>
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7B61FF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect width="20" height="16" x="2" y="4" rx="2"/>
            <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
          </svg>
        </div>
      </div>

      {/* Title */}
      <h1 className="text-2xl font-bold text-white mb-2">Verifier votre email</h1>
      <p className="text-sm text-center mb-8 max-w-xs" style={{ color: "rgba(255,255,255,0.5)" }}>
        Nous avons envoye un code de verification a<br/>
        <span style={{ color: "#7B61FF" }}>{email}</span>
      </p>

      {/* Code Inputs */}
      <div className="flex gap-3 mb-4" onPaste={handlePaste}>
        {codes.map((code, index) => (
          <input
            key={index}
            ref={(el) => { inputRefs.current[index] = el; }}
            type="text"
            inputMode="numeric"
            maxLength={1}
            value={code}
            onChange={(e) => handleChange(index, e.target.value.replace(/\D/g, ""))}
            onKeyDown={(e) => handleKeyDown(index, e)}
            className="w-12 h-14 rounded-xl text-center text-xl font-bold text-white focus:outline-none focus:ring-2"
            style={{
              background: "rgba(255,255,255,0.08)",
              border: code ? "2px solid #7B61FF" : "2px solid rgba(255,255,255,0.1)",
              caretColor: "#7B61FF",
            }}
            disabled={loading}
          />
        ))}
      </div>

      {/* Hint */}
      <p className="text-xs mb-6" style={{ color: "rgba(255,255,255,0.3)" }}>
        Code de demo : <span style={{ color: "#7B61FF" }}>123456</span>
      </p>

      {/* Error */}
      {error && (
        <div className="w-full max-w-xs p-3 rounded-xl text-sm text-center mb-4" style={{ background: "rgba(255,59,48,0.15)", color: "#FF6B6B", border: "1px solid rgba(255,59,48,0.2)" }}>
          {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center gap-2 mb-4">
          <svg className="animate-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B61FF" strokeWidth="2"><circle cx="12" cy="12" r="10" strokeOpacity="0.3"/><path d="M12 2a10 10 0 0 1 10 10"/></svg>
          <span className="text-sm" style={{ color: "rgba(255,255,255,0.6)" }}>Verification en cours...</span>
        </div>
      )}

      {/* Resend */}
      <div className="mt-4 text-center">
        {resendTimer > 0 ? (
          <p className="text-xs" style={{ color: "rgba(255,255,255,0.3)" }}>
            Renvoyer le code dans <span style={{ color: "#7B61FF" }}>{resendTimer}s</span>
          </p>
        ) : (
          <button onClick={handleResend} className="text-sm font-semibold" style={{ color: "#7B61FF" }}>
            Renvoyer le code
          </button>
        )}
      </div>
    </div>
  );
}
