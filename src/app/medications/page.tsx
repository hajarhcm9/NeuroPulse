"use client";

import { Pill, CheckCircle, Plus } from "lucide-react";
import BottomNav from "@/components/BottomNav";
import { simulatedMedications } from "@/lib/simulation";

export default function MedicationsPage() {
  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 100px" }} className="page-enter">
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Medicaments</h1>
      <div className="dark-card" style={{ marginTop: 20, display: "flex", alignItems: "center", gap: 16 }}>
        <div style={{ width: 48, height: 48, borderRadius: 14, background: "rgba(0,210,106,0.15)", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <CheckCircle size={24} color="#00D26A" />
        </div>
        <div>
          <div style={{ fontSize: 22, fontWeight: 800, color: "white" }}>1/3</div>
          <div style={{ fontSize: 13, color: "#8D91B5" }}>pris aujourd hui</div>
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 20 }}>
        {simulatedMedications.map((med) => (
          <div key={med.id} className="dark-card" style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{ width: 44, height: 44, borderRadius: 14, background: med.taken ? "rgba(0,210,106,0.15)" : "rgba(139,143,181,0.1)", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <Pill size={22} color={med.taken ? "#00D26A" : "#8D91B5"} />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 16, fontWeight: 700, color: "white" }}>{med.name}</div>
              <div style={{ fontSize: 13, color: "#8D91B5", marginTop: 2 }}>{med.dosage}</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 14, color: "#7B61FF", fontWeight: 600 }}>{med.time}</div>
              <div style={{ fontSize: 12, color: med.taken ? "#00D26A" : "#FF8A00", marginTop: 2 }}>{med.taken ? "Pris" : "A prendre"}</div>
            </div>
          </div>
        ))}
      </div>
      <button className="btn-primary" style={{ marginTop: 20, display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
        <Plus size={18} /> Ajouter un medicament
      </button>
      <BottomNav />
    </div>
  );
}
