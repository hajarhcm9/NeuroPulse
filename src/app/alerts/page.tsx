"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { simulatedAlerts } from "@/lib/simulation";
import BottomNav from "@/components/BottomNav";

export default function AlertsPage() {
  const router = useRouter();
  const [active, setActive] = useState("Tous");
  const filters = ["Tous", "Critique", "Warning", "Info"];

  const filtered = active === "Tous"
    ? simulatedAlerts
    : simulatedAlerts.filter((a) => a.severity === active);

  const getSeverityIcon = (severity: string) => {
    if (severity === "Critique") return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke={severity === "Critique" ? "#FF3B30" : severity === "Warning" ? "#FF9500" : "#34C759"} strokeWidth="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
    );
    if (severity === "Warning") return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF9500" strokeWidth="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
    );
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34C759" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
    );
  };

  return (
    <div className="page-enter" style={{ minHeight: "100vh", padding: "20px 20px 100px" }}>
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Alertes</h1>

      {/* Filter Pills */}
      <div style={{ display: "flex", gap: 8, marginTop: 16, overflowX: "auto" }}>
        {filters.map((f) => (
          <button
            key={f}
            className={"filter-pill" + (active === f ? " active" : "")}
            onClick={() => setActive(f)}
          >
            {f}
            {f !== "Tous" && (
              <span style={{
                marginLeft: 4, padding: "2px 6px", borderRadius: 6, fontSize: 10,
                background: active === f ? "rgba(123,97,255,0.3)" : "rgba(255,255,255,0.06)"
              }}>
                {simulatedAlerts.filter(a => a.severity === f).length}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Results count */}
      <div style={{ fontSize: 12, color: "rgba(255,255,255,0.3)", marginTop: 12, marginBottom: 4 }}>
        {filtered.length} alerte{filtered.length > 1 ? "s" : ""}
      </div>

      {/* Alerts List */}
      <div className="stagger-list" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {filtered.map((alert) => (
          <div
            key={alert.id}
            className="dark-card"
            onClick={() => router.push(`/alert/${alert.id}`)}
            style={{ borderLeft: `4px solid ${alert.color}`, cursor: "pointer" }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
              {getSeverityIcon(alert.severity)}
              <span style={{ fontSize: 16, fontWeight: 700, color: "white" }}>{alert.title || alert.type}</span>
              <span style={{
                marginLeft: "auto", padding: "3px 8px", borderRadius: 8, fontSize: 10, fontWeight: 700,
                background: alert.severity === "Critique" ? "rgba(255,59,48,0.15)" : alert.severity === "Warning" ? "rgba(255,149,0,0.15)" : "rgba(52,199,89,0.15)",
                color: alert.severity === "Critique" ? "#FF3B30" : alert.severity === "Warning" ? "#FF9500" : "#34C759"
              }}>
                {alert.severity}
              </span>
            </div>
            <div style={{ fontSize: 13, color: "#C5C8E1", marginTop: 6 }}>{alert.description || alert.type}</div>
            <div style={{ display: "flex", gap: 12, marginTop: 8 }}>
              <span style={{ fontSize: 12, color: "#8D91B5" }}>{alert.date}</span>
              <span style={{ fontSize: 12, color: "#8D91B5" }}>{alert.time}</span>
              {alert.duration && <span style={{ fontSize: 12, color: "#8D91B5" }}>{alert.duration}</span>}
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: 40, color: "rgba(255,255,255,0.3)" }}>
          Aucune alerte pour ce filtre
        </div>
      )}

      <BottomNav />
    </div>
  );
}
