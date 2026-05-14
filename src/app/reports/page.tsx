"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie } from "recharts";
import BottomNav from "@/components/BottomNav";
import { simulatedWeeklySeizures, simulatedDayNight } from "@/lib/simulation";

export default function ReportsPage() {
  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 100px" }} className="page-enter">
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Rapports</h1>
      <div className="dark-card" style={{ marginTop: 20 }}>
        <div style={{ fontSize: 16, fontWeight: 700, color: "white", marginBottom: 12 }}>Crises par semaine</div>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={simulatedWeeklySeizures}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E2356" />
            <XAxis dataKey="week" stroke="#8D91B5" fontSize={12} />
            <YAxis stroke="#8D91B5" fontSize={12} />
            <Tooltip />
            <Bar dataKey="count" fill="#7B61FF" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="dark-card" style={{ marginTop: 16, display: "flex", alignItems: "center" }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 16, fontWeight: 700, color: "white", marginBottom: 12 }}>Jour / Nuit</div>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie data={simulatedDayNight} dataKey="value" cx="50%" cy="50%" innerRadius={40} outerRadius={60} />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {simulatedDayNight.map((d) => (
            <div key={d.name} style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <div style={{ width: 10, height: 10, borderRadius: 5, background: d.fill }} />
              <span style={{ fontSize: 13, color: "white" }}>{d.name}: {d.value}%</span>
            </div>
          ))}
        </div>
      </div>
      <div className="dark-card" style={{ marginTop: 16 }}>
        <div style={{ fontSize: 16, fontWeight: 700, color: "white", marginBottom: 8 }}>Resume mensuel</div>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          {[{ label: "Crises", value: "4", color: "#FF3B30" }, { label: "Alertes", value: "12", color: "#FF8A00" }, { label: "Medicaments", value: "90%", color: "#00D26A" }].map((s) => (
            <div key={s.label} style={{ flex: 1, minWidth: 80, background: s.color + "1A", borderRadius: 14, padding: "14px 12px", textAlign: "center" }}>
              <div style={{ fontSize: 22, fontWeight: 800, color: s.color }}>{s.value}</div>
              <div style={{ fontSize: 12, color: "#8D91B5", marginTop: 2 }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>
      <BottomNav />
    </div>
  );
}
