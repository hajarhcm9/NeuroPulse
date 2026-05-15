"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { elevatedSymptoms } from "@/lib/simulation";
import BottomNav from "@/components/BottomNav";

export default function SymptomsPage() {
  const router = useRouter();
  const [selected, setSelected] = useState<string | null>(null);

  const getLevelColor = (level: string) => {
    if (level === "Critique") return "#FF3B30";
    if (level === "Eleve") return "#FF9500";
    if (level === "Moyen") return "#FFCC00";
    return "#34C759";
  };

  const getLevelBg = (level: string) => {
    if (level === "Critique") return "rgba(255,59,48,0.12)";
    if (level === "Eleve") return "rgba(255,149,0,0.12)";
    if (level === "Moyen") return "rgba(255,204,0,0.12)";
    return "rgba(52,199,89,0.12)";
  };

  const getIcon = (icon: string) => {
    if (icon === "heart") return (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
    );
    if (icon === "oxygen") return (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M8 12h8"/><path d="M12 8v8"/></svg>
    );
    if (icon === "movement") return (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 3v4h4"/><path d="M19 21v-4h-4"/><path d="M5 7a8 8 0 0 1 14 2"/><path d="M19 17a8 8 0 0 1-14-2"/></svg>
    );
    if (icon === "brain") return (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M19.938 10.5a4 4 0 0 1 .585.396"/><path d="M6 18a4 4 0 0 1-1.967-.516"/><path d="M19.967 17.484A4 4 0 0 1 18 18"/></svg>
    );
    if (icon === "sweat") return (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>
    );
    return (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/></svg>
    );
  };

  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 100px" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <button onClick={() => router.back()} style={{ background: "none", border: "none", color: "white", cursor: "pointer" }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Symptomes</h1>
      </div>

      {/* Summary Card */}
      <div className="dark-card" style={{ marginBottom: 20, border: "1px solid rgba(255,59,48,0.3)", background: "rgba(255,59,48,0.08)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div style={{ fontSize: 14, color: "rgba(255,255,255,0.5)" }}>Symptomes actifs</div>
            <div style={{ fontSize: 32, fontWeight: 800, color: "#FF3B30" }}>{elevatedSymptoms.filter(s => s.level === "Critique" || s.level === "Eleve").length}</div>
          </div>
          <div style={{ padding: "12px 16px", borderRadius: 16, background: "rgba(255,59,48,0.15)" }}>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#FF3B30" }}>SURVEILLANCE</span>
          </div>
        </div>
      </div>

      {/* Symptoms List */}
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {elevatedSymptoms.map((symptom) => (
          <div
            key={symptom.id}
            className="dark-card"
            onClick={() => setSelected(selected === symptom.id ? null : symptom.id)}
            style={{
              cursor: "pointer",
              borderLeft: `4px solid ${getLevelColor(symptom.level)}`,
              transition: "all 0.3s ease"
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <div style={{ width: 44, height: 44, borderRadius: 14, display: "flex", alignItems: "center", justifyContent: "center", background: getLevelBg(symptom.level), color: getLevelColor(symptom.level) }}>
                {getIcon(symptom.icon)}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 15, fontWeight: 700, color: "white" }}>{symptom.name}</div>
                <div style={{ fontSize: 13, color: "rgba(255,255,255,0.5)", marginTop: 2 }}>{symptom.value}</div>
              </div>
              <div style={{ padding: "4px 10px", borderRadius: 10, background: getLevelBg(symptom.level), fontSize: 12, fontWeight: 700, color: getLevelColor(symptom.level) }}>
                {symptom.level}
              </div>
            </div>
            {selected === symptom.id && (
              <div style={{ marginTop: 12, padding: "12px", borderRadius: 12, background: "rgba(255,255,255,0.04)", fontSize: 13, color: "rgba(255,255,255,0.6)" }}>
                {symptom.description}
              </div>
            )}
          </div>
        ))}
      </div>

      <BottomNav />
    </div>
  );
}
