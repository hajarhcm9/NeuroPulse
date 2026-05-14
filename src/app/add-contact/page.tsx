"use client";

import { useState } from "react";
import { ArrowLeft, User, Phone, Mail, Save } from "lucide-react";
import { useRouter } from "next/navigation";

export default function AddContactPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");

  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 40px" }} className="page-enter">
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <ArrowLeft size={24} color="white" onClick={() => router.back()} style={{ cursor: "pointer" }} />
        <h1 style={{ fontSize: 24, fontWeight: 800, color: "white" }}>Ajouter un contact</h1>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        <div className="dark-card">
          <label style={{ fontSize: 13, color: "#8D91B5", marginBottom: 6, display: "block" }}>Nom complet</label>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <User size={18} color="#7B61FF" />
            <input className="input-dark" placeholder="Dr. Bennani" value={name} onChange={(e) => setName(e.target.value)} style={{ flex: 1 }} />
          </div>
        </div>
        <div className="dark-card">
          <label style={{ fontSize: 13, color: "#8D91B5", marginBottom: 6, display: "block" }}>Telephone</label>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <Phone size={18} color="#00D26A" />
            <input className="input-dark" placeholder="+212 6XX XXX XXX" value={phone} onChange={(e) => setPhone(e.target.value)} style={{ flex: 1 }} />
          </div>
        </div>
        <div className="dark-card">
          <label style={{ fontSize: 13, color: "#8D91B5", marginBottom: 6, display: "block" }}>Email</label>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <Mail size={18} color="#4AA8FF" />
            <input className="input-dark" placeholder="email@example.com" value={email} onChange={(e) => setEmail(e.target.value)} style={{ flex: 1 }} />
          </div>
        </div>
      </div>
      <button className="btn-primary" style={{ marginTop: 24, display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
        <Save size={18} /> Enregistrer
      </button>
    </div>
  );
}
