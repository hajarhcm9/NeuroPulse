"use client";

import { useState, useEffect } from "react";
import { Heart, Droplets, Move, Activity, ArrowLeft } from "lucide-react";
import { generateHeartRate, generateSpO2, generateMovement, generateRiskLevel } from "@/lib/simulation";

export default function MonitoringPage() {
  const [hr, setHr] = useState(72);
  const [spo2, setSpo2] = useState(98);
  const [move, setMove] = useState(0.3);
  const [risk, setRisk] = useState({ level: "Faible", percent: 18, color: "#00D26A" });

  useEffect(() => {
    const interval = setInterval(() => {
      setHr(Math.round(generateHeartRate()));
      setSpo2(Math.round(generateSpO2() * 10) / 10);
      setMove(Math.round(generateMovement() * 100) / 100);
      setRisk(generateRiskLevel());
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 40px" }} className="page-enter">
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <ArrowLeft size={24} color="white" />
        <h1 style={{ fontSize: 24, fontWeight: 800, color: "white" }}>Surveillance temps reel</h1>
      </div>
      <div className="dark-card" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <div style={{ fontSize: 14, color: "#8D91B5" }}>Niveau de risque</div>
          <div style={{ fontSize: 28, fontWeight: 800, color: risk.color, marginTop: 4 }}>{risk.level}</div>
        </div>
        <div style={{ width: 60, height: 60, borderRadius: 30, background: risk.color + "1A", display: "flex", alignItems: "center", justifyContent: "center", border: "3px solid " + risk.color }}>
          <span style={{ fontSize: 18, fontWeight: 800, color: risk.color }}>{risk.percent}%</span>
        </div>
      </div>
      <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
        <div className="vital-card">
          <Heart size={20} color="#00D26A" style={{ marginBottom: 4 }} />
          <div style={{ fontSize: 20, fontWeight: 800, color: "#00D26A" }}>{hr}</div>
          <div style={{ fontSize: 11, color: "#8D91B5" }}>bpm</div>
        </div>
        <div className="vital-card">
          <Droplets size={20} color="#4AA8FF" style={{ marginBottom: 4 }} />
          <div style={{ fontSize: 20, fontWeight: 800, color: "#4AA8FF" }}>{spo2}%</div>
          <div style={{ fontSize: 11, color: "#8D91B5" }}>SpO2</div>
        </div>
        <div className="vital-card">
          <Move size={20} color="#FFD43B" style={{ marginBottom: 4 }} />
          <div style={{ fontSize: 16, fontWeight: 700, color: "#FFD43B" }}>{move}</div>
          <div style={{ fontSize: 11, color: "#8D91B5" }}>Mouvt</div>
        </div>
      </div>
      <div className="dark-card" style={{ marginTop: 16 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
          <Activity size={18} color="#7B61FF" />
          <span style={{ fontSize: 16, fontWeight: 700, color: "white" }}>Signal EEG</span>
        </div>
        <div style={{ height: 80, background: "rgba(123,97,255,0.1)", borderRadius: 12, display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden" }}>
          <svg width="100%" height="60" viewBox="0 0 300 60">
            <path d="M0,30 Q15,10 30,30 T60,30 T90,30 T120,30 T150,30 T180,30 T210,30 T240,30 T270,30 T300,30" stroke="#7B61FF" strokeWidth="2" fill="none" opacity="0.6" />
          </svg>
        </div>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 16 }}>
        <div style={{ width: 8, height: 8, borderRadius: 4, background: "#00D26A", boxShadow: "0 0 8px #00D26A" }} />
        <span style={{ fontSize: 14, color: "#00D26A", fontWeight: 600 }}>Capteur actif</span>
        <span style={{ fontSize: 12, color: "#8D91B5", marginLeft: 8 }}>Derniere sync: il y a 2s</span>
      </div>
    </div>
  );
}
