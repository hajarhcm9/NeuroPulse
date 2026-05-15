"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { generateHeartRate, generateSpO2, generateMovement, generateRiskLevel } from "@/lib/simulation";
import BottomNav from "@/components/BottomNav";
import RiskGauge from "@/components/RiskGauge";

export default function DashboardPage() {
  const router = useRouter();
  const [hr, setHr] = useState(72);
  const [spo2, setSpo2] = useState(98);
  const [move, setMove] = useState(12);
  const [risk, setRisk] = useState({ level: "Faible", percent: 15, color: "#34C759" });
  const [toasts, setToasts] = useState<{ id: number; msg: string; type: string }[]>([]);
  const [showBanner, setShowBanner] = useState(false);
  const [bannerData, setBannerData] = useState({ title: "", desc: "", color: "#FF3B30" });
  const [pushNotif, setPushNotif] = useState(false);
  const [pushData, setPushData] = useState({ title: "", body: "" });

  // Toast system
  const addToast = useCallback((msg: string, type: string = "info") => {
    const id = Date.now();
    setToasts(prev => [...prev, { id, msg, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3000);
  }, []);

  // Update vitals
  useEffect(() => {
    const interval = setInterval(() => {
      const newHr = generateHeartRate();
      const newSpo2 = generateSpO2();
      const newMove = generateMovement();
      const newRisk = generateRiskLevel();

      setHr(newHr);
      setSpo2(newSpo2);
      setMove(newMove);
      setRisk(newRisk);

      // Auto-show banner for critical/elevated
      if (newRisk.level === "Critique") {
        setShowBanner(true);
        setBannerData({ title: "Alerte critique!", desc: `FC: ${newHr} bpm - SpO2: ${newSpo2}% - Mouvement: ${newMove}%`, color: "#FF3B30" });
        addToast("Niveau de risque CRITIQUE detecte!", "error");
      } else if (newRisk.level === "Eleve") {
        setBannerData({ title: "Attention", desc: `Signaux vitaux eleves - Surveillance renforcee`, color: "#FF9500" });
        setShowBanner(true);
        addToast("Risque eleve - Restez vigilant", "warning");
      } else {
        setShowBanner(false);
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [addToast]);

  // Simulated push notification after 30 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      setPushData({ title: "Smart Guardian", body: "Rappel: N'oubliez pas de prendre votre Depakine a 20:00" });
      setPushNotif(true);
      setTimeout(() => setPushNotif(false), 6000);
    }, 30000);
    return () => clearTimeout(timer);
  }, []);

  // Welcome toast
  useEffect(() => {
    const timer = setTimeout(() => {
      addToast("Bienvenue sur Smart Guardian!", "success");
    }, 1000);
    return () => clearTimeout(timer);
  }, [addToast]);

  return (
    <div className="page-enter" style={{ minHeight: "100vh", padding: "20px 20px 100px", position: "relative" }}>
      {/* ===== TOAST SYSTEM ===== */}
      <div style={{ position: "fixed", top: 16, left: "50%", transform: "translateX(-50%)", zIndex: 200, display: "flex", flexDirection: "column", gap: 8, width: "90%", maxWidth: 400 }}>
        {toasts.map((toast) => (
          <div
            key={toast.id}
            style={{
              padding: "12px 18px", borderRadius: 14, display: "flex", alignItems: "center", gap: 10,
              background: toast.type === "error" ? "rgba(255,59,48,0.2)" : toast.type === "warning" ? "rgba(255,149,0,0.2)" : toast.type === "success" ? "rgba(52,199,89,0.2)" : "rgba(123,97,255,0.2)",
              border: `1px solid ${toast.type === "error" ? "rgba(255,59,48,0.3)" : toast.type === "warning" ? "rgba(255,149,0,0.3)" : toast.type === "success" ? "rgba(52,199,89,0.3)" : "rgba(123,97,255,0.3)"}`,
              color: toast.type === "error" ? "#FF6B6B" : toast.type === "warning" ? "#FF9500" : toast.type === "success" ? "#34C759" : "#9D8FFF",
              fontSize: 13, fontWeight: 600,
              animation: "slideInUp 0.3s ease-out",
              backdropFilter: "blur(12px)"
            }}
          >
            {toast.type === "error" && <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>}
            {toast.type === "warning" && <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>}
            {toast.type === "success" && <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M20 6 9 17l-5-5"/></svg>}
            {toast.type === "info" && <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>}
            {toast.msg}
          </div>
        ))}
      </div>

      {/* ===== PUSH NOTIFICATION SIMULATION ===== */}
      {pushNotif && (
        <div
          style={{
            position: "fixed", top: 20, left: "50%", transform: "translateX(-50%)", zIndex: 300,
            width: "90%", maxWidth: 380, padding: "16px 18px", borderRadius: 20,
            background: "rgba(20, 24, 58, 0.95)", border: "1px solid rgba(123,97,255,0.3)",
            boxShadow: "0 12px 40px rgba(0,0,0,0.4)", backdropFilter: "blur(20px)",
            animation: "slideInUp 0.4s ease-out"
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
            <div style={{ width: 32, height: 32, borderRadius: 10, background: "linear-gradient(135deg, #7B61FF, #9D8FFF)", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            </div>
            <div>
              <div style={{ fontSize: 12, fontWeight: 700, color: "#7B61FF" }}>Smart Guardian</div>
              <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)" }}>Maintenant</div>
            </div>
            <button onClick={() => setPushNotif(false)} style={{ marginLeft: "auto", background: "none", border: "none", color: "rgba(255,255,255,0.3)", cursor: "pointer" }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
          <div style={{ fontSize: 14, fontWeight: 600, color: "white" }}>{pushData.title}</div>
          <div style={{ fontSize: 13, color: "rgba(255,255,255,0.5)", marginTop: 2 }}>{pushData.body}</div>
        </div>
      )}

      {/* ===== ALERT BANNER ===== */}
      {showBanner && (
        <div
          style={{
            padding: "12px 16px", borderRadius: 14, marginBottom: 16,
            background: `rgba(${bannerData.color === "#FF3B30" ? "255,59,48" : "255,149,0"},0.1)`,
            border: `1px solid ${bannerData.color}44`,
            display: "flex", alignItems: "center", gap: 10,
            animation: "slideInUp 0.3s ease-out"
          }}
        >
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: `${bannerData.color}22`,
            display: "flex", alignItems: "center", justifyContent: "center",
            color: bannerData.color
          }}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 14, fontWeight: 700, color: bannerData.color }}>{bannerData.title}</div>
            <div style={{ fontSize: 12, color: "rgba(255,255,255,0.5)", marginTop: 2 }}>{bannerData.desc}</div>
          </div>
          <button onClick={() => router.push("/sos")} style={{
            padding: "6px 12px", borderRadius: 10,
            background: `${bannerData.color}22`, border: `1px solid ${bannerData.color}44`,
            color: bannerData.color, fontSize: 12, fontWeight: 700, cursor: "pointer"
          }}>
            SOS
          </button>
        </div>
      )}

      {/* ===== HEADER ===== */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <div>
          <div style={{ fontSize: 14, color: "rgba(255,255,255,0.5)" }}>Bonjour</div>
          <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Tableau de bord</h1>
        </div>
        <button
          onClick={() => router.push("/profile")}
          style={{
            width: 42, height: 42, borderRadius: 14,
            background: "linear-gradient(135deg, #7B61FF, #9D8FFF)",
            display: "flex", alignItems: "center", justifyContent: "center",
            border: "none", cursor: "pointer",
            boxShadow: "0 4px 16px rgba(123,97,255,0.3)"
          }}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </button>
      </div>

      {/* ===== RISK GAUGE ===== */}
      <div className="dark-card card-enter card-enter-1" style={{ textAlign: "center", marginBottom: 16 }}>
        <RiskGauge level={risk.level} percent={risk.percent} color={risk.color} />
      </div>

      {/* ===== VITAL CARDS ===== */}
      <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
        <div className="vital-card card-enter card-enter-2" style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8 }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="#FF3B30" stroke="none"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
            <span style={{ fontSize: 11, color: "rgba(255,255,255,0.5)", fontWeight: 600 }}>FC</span>
          </div>
          <div className="number-animate" style={{ fontSize: 28, fontWeight: 900, color: "#FF3B30" }}>{hr}</div>
          <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)" }}>bpm</div>
        </div>
        <div className="vital-card card-enter card-enter-3" style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8 }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#007AFF" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/></svg>
            <span style={{ fontSize: 11, color: "rgba(255,255,255,0.5)", fontWeight: 600 }}>SpO2</span>
          </div>
          <div className="number-animate" style={{ fontSize: 28, fontWeight: 900, color: "#007AFF" }}>{spo2}</div>
          <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)" }}>%</div>
        </div>
        <div className="vital-card card-enter card-enter-4" style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8 }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FF9500" strokeWidth="2"><path d="M5 3v4h4"/><path d="M19 21v-4h-4"/><path d="M5 7a8 8 0 0 1 14 2"/><path d="M19 17a8 8 0 0 1-14-2"/></svg>
            <span style={{ fontSize: 11, color: "rgba(255,255,255,0.5)", fontWeight: 600 }}>Mvt</span>
          </div>
          <div className="number-animate" style={{ fontSize: 28, fontWeight: 900, color: "#FF9500" }}>{move}</div>
          <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)" }}>%</div>
        </div>
      </div>

      {/* ===== QUICK ACTIONS ===== */}
      <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
        <button
          onClick={() => router.push("/monitoring")}
          className="btn-primary card-enter card-enter-5"
          style={{ flex: 1, fontSize: 13, padding: "12px" }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          Monitoring
        </button>
        <button
          onClick={() => router.push("/symptoms")}
          className="card-enter card-enter-5"
          style={{
            flex: 1, fontSize: 13, padding: "12px", borderRadius: 14,
            background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)",
            color: "white", cursor: "pointer", fontWeight: 600,
            display: "flex", alignItems: "center", justifyContent: "center", gap: 6
          }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/></svg>
          Symptomes
        </button>
      </div>

      {/* ===== SOS FAB ===== */}
      <button
        onClick={() => router.push("/sos")}
        className="sos-pulse"
        style={{
          position: "fixed", bottom: 100, right: "50%", transform: "translateX(195px)",
          width: 60, height: 60, borderRadius: 30,
          background: "linear-gradient(135deg, #FF3B30, #CC0000)",
          border: "none", color: "white", fontSize: 16, fontWeight: 900,
          cursor: "pointer", zIndex: 50,
          boxShadow: "0 4px 24px rgba(255,59,48,0.4)",
          display: "flex", alignItems: "center", justifyContent: "center"
        }}
      >
        SOS
      </button>

      <BottomNav />
    </div>
  );
}
