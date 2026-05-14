"use client";

import { useState } from "react";
import { AlertTriangle, Bell, Info } from "lucide-react";
import BottomNav from "@/components/BottomNav";
import { simulatedAlerts } from "@/lib/simulation";

const filters = ["Tous", "Critique", "Warning", "Info"];

export default function AlertsPage() {
  const [active, setActive] = useState("Tous");
  const filtered = active === "Tous" ? simulatedAlerts : simulatedAlerts.filter((a) => a.type === active.toLowerCase());

  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 100px" }} className="page-enter">
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Alertes</h1>
      <div style={{ display: "flex", gap: 8, marginTop: 16, overflowX: "auto" }}>
        {filters.map((f) => (
          <button key={f} className={"filter-pill " + (active === f ? "active" : "")} onClick={() => setActive(f)}>{f}</button>
        ))}
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 20 }}>
        {filtered.map((alert) => (
          <div key={alert.id} className="dark-card" style={{ borderLeft: "4px solid " + alert.color }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              {alert.type === "critical" ? <AlertTriangle size={18} color={alert.color} /> : alert.type === "warning" ? <Bell size={18} color={alert.color} /> : <Info size={18} color={alert.color} />}
              <span style={{ fontSize: 16, fontWeight: 700, color: "white" }}>{alert.title}</span>
            </div>
            <div style={{ fontSize: 13, color: "#C5C8E1", marginTop: 6 }}>{alert.description}</div>
            <div style={{ fontSize: 12, color: "#8D91B5", marginTop: 4 }}>{alert.time}</div>
          </div>
        ))}
      </div>
      <BottomNav />
    </div>
  );
}
