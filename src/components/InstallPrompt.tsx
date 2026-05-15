"use client";

import { useState, useEffect } from "react";

export default function InstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e);
      // Show prompt after 5 seconds
      setTimeout(() => setShowPrompt(true), 5000);
    };

    window.addEventListener("beforeinstallprompt", handler);

    // Check if already dismissed
    if (typeof window !== "undefined") {
      const dismissed = localStorage.getItem("smart_guardian_install_dismissed");
      if (dismissed) {
        const dismissedTime = parseInt(dismissed);
        // Show again after 24 hours
        if (Date.now() - dismissedTime < 86400000) {
          return;
        }
      }
    }

    return () => window.removeEventListener("beforeinstallprompt", handler);
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === "accepted") {
      setShowPrompt(false);
    }
    setDeferredPrompt(null);
  };

  const handleDismiss = () => {
    setShowPrompt(false);
    if (typeof window !== "undefined") {
      localStorage.setItem("smart_guardian_install_dismissed", String(Date.now()));
    }
  };

  if (!showPrompt) return null;

  return (
    <div
      style={{
        position: "fixed", bottom: 0, left: 0, right: 0,
        padding: "16px 20px", zIndex: 200,
        background: "rgba(7, 11, 43, 0.95)",
        borderTop: "1px solid rgba(123,97,255,0.2)",
        backdropFilter: "blur(20px)",
        animation: "slideInUp 0.4s ease-out"
      }}
    >
      <div style={{ maxWidth: 430, margin: "0 auto", display: "flex", alignItems: "center", gap: 14 }}>
        <div style={{
          width: 48, height: 48, borderRadius: 14, flexShrink: 0,
          background: "linear-gradient(135deg, #7B61FF, #9D8FFF)",
          display: "flex", alignItems: "center", justifyContent: "center"
        }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 14, fontWeight: 700, color: "white" }}>Installer Smart Guardian</div>
          <div style={{ fontSize: 12, color: "rgba(255,255,255,0.4)" }}>Acces rapide depuis votre ecran</div>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button
            onClick={handleDismiss}
            style={{
              padding: "8px 12px", borderRadius: 10, border: "none",
              background: "rgba(255,255,255,0.06)", color: "rgba(255,255,255,0.5)",
              fontSize: 12, cursor: "pointer"
            }}
          >
            Plus tard
          </button>
          <button
            onClick={handleInstall}
            style={{
              padding: "8px 16px", borderRadius: 10, border: "none",
              background: "#7B61FF", color: "white",
              fontSize: 12, fontWeight: 700, cursor: "pointer"
            }}
          >
            Installer
          </button>
        </div>
      </div>
    </div>
  );
}
