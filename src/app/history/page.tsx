"use client";

import { useState } from "react";
import BottomNav from "@/components/BottomNav";
import { simulatedHistory } from "@/lib/simulation";

const filters = ["Evenements", "Crises", "Rapports"];

export default function HistoryPage() {
  const [active, setActive] = useState("Evenements");
  const filtered = active === "Evenements" ? simulatedHistory : simulatedHistory.filter((h) => h.type === active.toLowerCase());

  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 100px" }} className="page-enter">
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Historique</h1>
      <div style={{ display: "flex", gap: 8, marginTop: 16, overflowX: "auto" }}>
        {filters.map((f) => (
          <button key={f} className={"filter-pill " + (active === f ? "active" : "")} onClick={() => setActive(f)}>{f}</button>
        ))}
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 20 }}>
        {filtered.map((item) => (
          <div key={item.id} style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
            <div style={{ width: 10, height: 10, borderRadius: 5, background: item.color, boxShadow: "0 0 8px " + item.color, marginTop: 6, flexShrink: 0 }} />
            <div className="dark-card" style={{ flex: 1 }}>
              <div style={{ fontSize: 15, fontWeight: 700, color: "white" }}>{item.title}</div>
              <div style={{ fontSize: 13, color: "#C5C8E1", marginTop: 4 }}>{item.detail}</div>
              <div style={{ fontSize: 12, color: "#8D91B5", marginTop: 4 }}>{item.time}</div>
            </div>
          </div>
        ))}
      </div>
      <BottomNav />
    </div>
  );
}
