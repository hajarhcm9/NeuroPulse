"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { simulatedHistory } from "@/lib/simulation";
import BottomNav from "@/components/BottomNav";

export default function HistoryPage() {
  const router = useRouter();
  const [active, setActive] = useState("Evenements");
  const filters = ["Evenements", "Crises", "Rapports"];

  const filtered = active === "Evenements"
    ? simulatedHistory
    : active === "Crises"
    ? simulatedHistory.filter(h => h.type === "Crise")
    : simulatedHistory.filter(h => h.type === "Rapport");

  return (
    <div className="page-enter" style={{ minHeight: "100vh", padding: "20px 20px 100px" }}>
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Historique</h1>

      {/* Filter Pills */}
      <div style={{ display: "flex", gap: 8, marginTop: 16, overflowX: "auto" }}>
        {filters.map((f) => (
          <button
            key={f}
            className={"filter-pill" + (active === f ? " active" : "")}
            onClick={() => setActive(f)}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Results count */}
      <div style={{ fontSize: 12, color: "rgba(255,255,255,0.3)", marginTop: 12, marginBottom: 4 }}>
        {filtered.length} element{filtered.length > 1 ? "s" : ""}
      </div>

      {/* History List */}
      <div className="stagger-list" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {filtered.map((item) => (
          <div
            key={item.id}
            className="dark-card"
            style={{ borderLeft: `4px solid ${item.color || "#7B61FF"}` }}
          >
            <div style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
              <div style={{
                width: 10, height: 10, borderRadius: 5, marginTop: 6,
                background: item.color || "#7B61FF",
                boxShadow: `0 0 8px ${item.color || "#7B61FF"}66`
              }}></div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 15, fontWeight: 700, color: "white" }}>{item.title || item.type}</div>
                <div style={{ fontSize: 13, color: "#C5C8E1", marginTop: 4 }}>{item.detail || item.notes}</div>
                <div style={{ display: "flex", gap: 12, marginTop: 6 }}>
                  <span style={{ fontSize: 12, color: "#8D91B5" }}>{item.date}</span>
                  <span style={{ fontSize: 12, color: "#8D91B5" }}>{item.time}</span>
                  {item.duration && item.duration !== "-" && (
                    <span style={{
                      fontSize: 11, padding: "2px 8px", borderRadius: 6,
                      background: "rgba(123,97,255,0.1)", color: "#7B61FF"
                    }}>
                      {item.duration}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: 40, color: "rgba(255,255,255,0.3)" }}>
          Aucun element pour ce filtre
        </div>
      )}

      <BottomNav />
    </div>
  );
}
