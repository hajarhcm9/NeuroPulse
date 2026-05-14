"use client";

import { MapPin, Phone, Navigation } from "lucide-react";
import BottomNav from "@/components/BottomNav";

export default function GPSPage() {
  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 100px" }} className="page-enter">
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Localisation</h1>
      <div className="dark-card" style={{ marginTop: 20, height: 250, display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #0D1037, #1A144B)" }}>
        <div style={{ textAlign: "center" }}>
          <MapPin size={48} color="#7B61FF" style={{ marginBottom: 12 }} />
          <div style={{ fontSize: 16, color: "white", fontWeight: 600 }}>Position actuelle</div>
          <div style={{ fontSize: 13, color: "#8D91B5", marginTop: 4 }}>33.5731 N, 7.5898 W</div>
          <div style={{ fontSize: 12, color: "#00D26A", marginTop: 8 }}>En ligne</div>
        </div>
      </div>
      <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
        <button className="btn-primary" style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
          <Navigation size={18} /> Itineraire
        </button>
        <button style={{ flex: 1, height: 52, borderRadius: 18, background: "rgba(74,168,255,0.15)", border: "1px solid rgba(74,168,255,0.3)", color: "#4AA8FF", fontSize: 16, fontWeight: 700, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
          <Phone size={18} /> Appeler
        </button>
      </div>
      <div style={{ marginTop: 24 }}>
        <div style={{ fontSize: 16, fontWeight: 700, color: "white", marginBottom: 12 }}>Contacts proches</div>
        {[{ name: "Dr. Bennani", role: "Neurologue", dist: "1.2 km" }, { name: "Famille", role: "Urgence", dist: "3.5 km" }].map((c) => (
          <div key={c.name} className="dark-card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
            <div>
              <div style={{ fontSize: 15, fontWeight: 600, color: "white" }}>{c.name}</div>
              <div style={{ fontSize: 13, color: "#8D91B5" }}>{c.role}</div>
            </div>
            <div style={{ fontSize: 13, color: "#7B61FF", fontWeight: 600 }}>{c.dist}</div>
          </div>
        ))}
      </div>
      <BottomNav />
    </div>
  );
}
