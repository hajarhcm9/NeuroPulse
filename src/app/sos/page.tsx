"use client";

import { Phone, AlertTriangle, MapPin, Users } from "lucide-react";

export default function SOSPage() {
  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 40px", display: "flex", flexDirection: "column", alignItems: "center" }} className="page-enter">
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "white", alignSelf: "flex-start" }}>Urgence</h1>
      <div style={{ width: 180, height: 180, borderRadius: 90, background: "linear-gradient(135deg, #FF375F, #FF1744)", display: "flex", alignItems: "center", justifyContent: "center", marginTop: 40, boxShadow: "0 0 60px rgba(255,55,95,0.5)" }}>
        <AlertTriangle size={64} color="white" />
      </div>
      <div style={{ fontSize: 24, fontWeight: 800, color: "#FF3B30", marginTop: 24 }}>APPEL D URGENCE</div>
      <div style={{ fontSize: 14, color: "#8D91B5", marginTop: 8, textAlign: "center" }}>Appuyez pour alerter vos contacts</div>
      <div style={{ display: "flex", gap: 16, marginTop: 40, width: "100%" }}>
        <button style={{ flex: 1, height: 60, borderRadius: 20, background: "rgba(0,210,106,0.15)", border: "1px solid rgba(0,210,106,0.3)", color: "#00D26A", fontSize: 16, fontWeight: 700, cursor: "pointer", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 4 }}>
          <Phone size={20} /> SAMU
        </button>
        <button style={{ flex: 1, height: 60, borderRadius: 20, background: "rgba(74,168,255,0.15)", border: "1px solid rgba(74,168,255,0.3)", color: "#4AA8FF", fontSize: 16, fontWeight: 700, cursor: "pointer", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 4 }}>
          <MapPin size={20} /> Position
        </button>
      </div>
      <div style={{ marginTop: 24, width: "100%" }}>
        <div style={{ fontSize: 16, fontWeight: 700, color: "white", marginBottom: 12 }}>Contacts d urgence</div>
        {[{ name: "Dr. Bennani", phone: "+212 6XX XXX XXX" }, { name: "Mere", phone: "+212 6YY YYY YYY" }, { name: "Urgences", phone: "15" }].map((c) => (
          <div key={c.name} className="dark-card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <Users size={20} color="#7B61FF" />
              <div>
                <div style={{ fontSize: 15, fontWeight: 600, color: "white" }}>{c.name}</div>
                <div style={{ fontSize: 13, color: "#8D91B5" }}>{c.phone}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
