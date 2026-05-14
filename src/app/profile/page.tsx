"use client";

import { User, Settings, Bell, Shield, HelpCircle, LogOut } from "lucide-react";
import BottomNav from "@/components/BottomNav";
import { getUserName, logout } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const router = useRouter();
  const name = getUserName();
  const handleLogout = () => { logout(); router.push("/"); };

  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 100px" }} className="page-enter">
      <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Profil</h1>
      <div className="dark-card" style={{ marginTop: 20, display: "flex", alignItems: "center", gap: 16 }}>
        <div style={{ width: 60, height: 60, borderRadius: 30, background: "linear-gradient(135deg, #7B61FF, #4AA8FF)", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <User size={28} color="white" />
        </div>
        <div>
          <div style={{ fontSize: 20, fontWeight: 700, color: "white" }}>{name}</div>
          <div style={{ fontSize: 14, color: "#8D91B5", marginTop: 2 }}>Patient</div>
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 24 }}>
        {[
          { icon: Settings, label: "Parametres", color: "#7B61FF" },
          { icon: Bell, label: "Notifications", color: "#FFD43B" },
          { icon: Shield, label: "Securite", color: "#00D26A" },
          { icon: HelpCircle, label: "Aide et support", color: "#4AA8FF" },
        ].map((item) => (
          <div key={item.label} className="dark-card" style={{ display: "flex", alignItems: "center", gap: 14, cursor: "pointer" }}>
            <div style={{ width: 40, height: 40, borderRadius: 12, background: item.color + "1A", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <item.icon size={20} color={item.color} />
            </div>
            <span style={{ fontSize: 16, fontWeight: 600, color: "white" }}>{item.label}</span>
          </div>
        ))}
      </div>
      <button onClick={handleLogout} style={{ marginTop: 24, width: "100%", height: 52, borderRadius: 18, background: "rgba(255,77,109,0.1)", border: "1px solid rgba(255,77,109,0.2)", color: "#FF4D6D", fontSize: 16, fontWeight: 700, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
        <LogOut size={18} /> Deconnexion
      </button>
      <BottomNav />
    </div>
  );
}
