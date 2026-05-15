"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getUserName, logout } from "@/lib/auth";
import BottomNav from "@/components/BottomNav";

interface UserPrefs {
  notifications: boolean;
  soundAlerts: boolean;
  autoCall: boolean;
  gpsTracking: boolean;
  darkMode: boolean;
}

const defaultPrefs: UserPrefs = {
  notifications: true,
  soundAlerts: true,
  autoCall: true,
  gpsTracking: true,
  darkMode: true,
};

export default function ProfilePage() {
  const router = useRouter();
  const [prefs, setPrefs] = useState<UserPrefs>(defaultPrefs);
  const [showToast, setShowToast] = useState(false);
  const [toastMsg, setToastMsg] = useState("");

  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("smart_guardian_prefs");
      if (saved) setPrefs(JSON.parse(saved));
    }
  }, []);

  const savePrefs = (newPrefs: UserPrefs) => {
    setPrefs(newPrefs);
    if (typeof window !== "undefined") {
      localStorage.setItem("smart_guardian_prefs", JSON.stringify(newPrefs));
    }
    setToastMsg("Preferences sauvegardees");
    setShowToast(true);
    setTimeout(() => setShowToast(false), 2000);
  };

  const togglePref = (key: keyof UserPrefs) => {
    savePrefs({ ...prefs, [key]: !prefs[key] });
  };

  const handleLogout = () => {
    logout();
    router.push("/");
  };

  const Toggle = ({ value, onToggle }: { value: boolean; onToggle: () => void }) => (
    <button
      onClick={onToggle}
      style={{
        width: 48, height: 28, borderRadius: 14, border: "none",
        background: value ? "#7B61FF" : "rgba(255,255,255,0.1)",
        position: "relative", cursor: "pointer", transition: "all 0.3s ease",
        flexShrink: 0
      }}
    >
      <div style={{
        width: 22, height: 22, borderRadius: 11, background: "white",
        position: "absolute", top: 3,
        left: value ? 23 : 3,
        transition: "all 0.3s ease",
        boxShadow: "0 2px 4px rgba(0,0,0,0.2)"
      }}></div>
    </button>
  );

  const prefItems = [
    { key: "notifications" as keyof UserPrefs, label: "Notifications", desc: "Recevoir les alertes push", icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
    )},
    { key: "soundAlerts" as keyof UserPrefs, label: "Alertes sonores", desc: "Sons et vibrations dalerte", icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
    )},
    { key: "autoCall" as keyof UserPrefs, label: "Appel automatique", desc: "Appeler la famille en cas de crise", icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
    )},
    { key: "gpsTracking" as keyof UserPrefs, label: "Suivi GPS", desc: "Partager votre position en urgence", icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
    )},
    { key: "darkMode" as keyof UserPrefs, label: "Mode sombre", desc: "Theme fonce de lapplication", icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
    )},
  ];

  return (
    <div className="page-enter" style={{ minHeight: "100vh", padding: "20px 20px 100px" }}>
      {/* Toast */}
      {showToast && (
        <div style={{
          position: "fixed", top: 20, left: "50%", transform: "translateX(-50%)",
          padding: "12px 24px", borderRadius: 16, zIndex: 100,
          background: "rgba(123,97,255,0.2)", border: "1px solid rgba(123,97,255,0.3)",
          color: "#9D8FFF", fontSize: 14, fontWeight: 600,
          animation: "slideInUp 0.3s ease-out"
        }}>
          {toastMsg}
        </div>
      )}

      {/* Profile Card */}
      <div className="dark-card card-enter card-enter-1" style={{ textAlign: "center", marginBottom: 20 }}>
        <div style={{
          width: 80, height: 80, borderRadius: 40, margin: "0 auto 12px",
          background: "linear-gradient(135deg, #7B61FF, #9D8FFF)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 32, fontWeight: 800, color: "white",
          boxShadow: "0 8px 24px rgba(123,97,255,0.3)"
        }}>
          {typeof window !== "undefined" ? getUserName().charAt(0) : "U"}
        </div>
        <div style={{ fontSize: 20, fontWeight: 800, color: "white" }}>{typeof window !== "undefined" ? getUserName() : "Utilisateur"}</div>
        <div style={{ fontSize: 13, color: "rgba(255,255,255,0.4)", marginTop: 4 }}>Patient</div>
      </div>

      {/* Preferences */}
      <div className="dark-card card-enter card-enter-2" style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, color: "white", marginBottom: 16 }}>Preferences</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {prefItems.map((item) => (
            <div key={item.key} style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <div style={{ width: 40, height: 40, borderRadius: 12, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(123,97,255,0.1)", color: "#7B61FF" }}>
                {item.icon}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 14, fontWeight: 600, color: "white" }}>{item.label}</div>
                <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)", marginTop: 2 }}>{item.desc}</div>
              </div>
              <Toggle value={prefs[item.key]} onToggle={() => togglePref(item.key)} />
            </div>
          ))}
        </div>
      </div>

      {/* Quick Links */}
      <div className="dark-card card-enter card-enter-3" style={{ marginBottom: 16 }}>
        {[
          { label: "Mes contacts", page: "/sos", icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B61FF" strokeWidth="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> },
          { label: "Mes medicaments", page: "/medications", icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B61FF" strokeWidth="2"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg> },
          { label: "Mes rapports", page: "/reports", icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B61FF" strokeWidth="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg> },
          { label: "Symptomes", page: "/symptoms", icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7B61FF" strokeWidth="2"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/></svg> },
        ].map((link) => (
          <button
            key={link.label}
            onClick={() => router.push(link.page)}
            style={{
              display: "flex", alignItems: "center", gap: 14,
              padding: "14px 0", background: "none", border: "none",
              borderBottom: "1px solid rgba(255,255,255,0.06)",
              cursor: "pointer", width: "100%", textAlign: "left"
            }}
          >
            {link.icon}
            <span style={{ fontSize: 14, fontWeight: 600, color: "white", flex: 1 }}>{link.label}</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.2)" strokeWidth="2"><path d="m9 18 6-6-6-6"/></svg>
          </button>
        ))}
      </div>

      {/* Logout */}
      <button
        onClick={handleLogout}
        className="card-enter card-enter-4"
        style={{
          width: "100%", padding: "14px", borderRadius: 16,
          border: "1px solid rgba(255,59,48,0.3)", background: "rgba(255,59,48,0.08)",
          color: "#FF6B6B", fontSize: 15, fontWeight: 700, cursor: "pointer"
        }}
      >
        Deconnexion
      </button>

      <BottomNav />
    </div>
  );
}
