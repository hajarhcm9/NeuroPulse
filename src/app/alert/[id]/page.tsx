"use client";

import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, Heart, Droplets, AlertTriangle, Clock } from "lucide-react";
import { simulatedAlerts } from "@/lib/simulation";

export default function AlertDetailPage() {
  const params = useParams();
  const router = useRouter();
  const alert = simulatedAlerts.find((a) => a.id === params.id) || simulatedAlerts[0];

  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 40px" }} className="page-enter">
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <ArrowLeft size={24} color="white" onClick={() => router.back()} style={{ cursor: "pointer" }} />
        <h1 style={{ fontSize: 24, fontWeight: 800, color: "white" }}>Detail alerte</h1>
      </div>
      <div className="dark-card" style={{ borderLeft: "4px solid " + alert.color }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
          <AlertTriangle size={20} color={alert.color} />
          <span style={{ fontSize: 20, fontWeight: 800, color: alert.color }}>{alert.title}</span>
        </div>
        <div style={{ fontSize: 15, color: "#C5C8E1", marginTop: 8 }}>{alert.description}</div>
        <div style={{ display: "flex", alignItems: "center", gap: 6, marginTop: 12 }}>
          <Clock size={14} color="#8D91B5" />
          <span style={{ fontSize: 13, color: "#8D91B5" }}>{alert.time}</span>
        </div>
      </div>
      <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
        <div className="vital-card" style={{ flex: 1 }}>
          <Heart size={18} color="#00D26A" style={{ marginBottom: 4 }} />
          <div style={{ fontSize: 18, fontWeight: 800, color: "#00D26A" }}>{alert.heartRate} bpm</div>
        </div>
        <div className="vital-card" style={{ flex: 1 }}>
          <Droplets size={18} color="#4AA8FF" style={{ marginBottom: 4 }} />
          <div style={{ fontSize: 18, fontWeight: 800, color: "#4AA8FF" }}>{alert.spo2}%</div>
        </div>
      </div>
      <button className="btn-primary" style={{ marginTop: 24 }}>Voir le rapport complet</button>
    </div>
  );
}
