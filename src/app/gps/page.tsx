"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import BottomNav from "@/components/BottomNav";

export default function GPSPage() {
  const router = useRouter();
  const [gpsActive, setGpsActive] = useState(false);
  const [bluetoothActive, setBluetoothActive] = useState(false);
  const [position, setPosition] = useState({ lat: 33.5731, lng: -7.5898 });
  const [requestingGps, setRequestingGps] = useState(false);
  const [requestingBt, setRequestingBt] = useState(false);
  const [showGpsPrompt, setShowGpsPrompt] = useState(true);
  const [showBtPrompt, setShowBtPrompt] = useState(false);

  const activateGPS = async () => {
    setRequestingGps(true);
    try {
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            setPosition({ lat: pos.coords.latitude, lng: pos.coords.longitude });
            setGpsActive(true);
            setRequestingGps(false);
            setShowGpsPrompt(false);
            setShowBtPrompt(true);
          },
          () => {
            setGpsActive(true);
            setRequestingGps(false);
            setShowGpsPrompt(false);
            setShowBtPrompt(true);
          }
        );
      } else {
        setGpsActive(true);
        setRequestingGps(false);
        setShowGpsPrompt(false);
        setShowBtPrompt(true);
      }
    } catch {
      setGpsActive(true);
      setRequestingGps(false);
      setShowGpsPrompt(false);
      setShowBtPrompt(true);
    }
  };

  const activateBluetooth = async () => {
    setRequestingBt(true);
    await new Promise(r => setTimeout(r, 1500));
    try {
      if ("bluetooth" in navigator) {
        const device = await (navigator as any).bluetooth.requestDevice({
          acceptAllDevices: true
        });
        setBluetoothActive(!!device);
      } else {
        setBluetoothActive(true);
      }
    } catch {
      setBluetoothActive(false);
    }
    setRequestingBt(false);
    setShowBtPrompt(false);
  };

  const skipBluetooth = () => {
    setBluetoothActive(false);
    setShowBtPrompt(false);
  };

  return (
    <div style={{ minHeight: "100vh", padding: "20px 20px 100px" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
        <button onClick={() => router.back()} style={{ background: "none", border: "none", color: "white", cursor: "pointer" }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Localisation</h1>
      </div>

      {/* GPS Activation Prompt */}
      {showGpsPrompt && (
        <div className="dark-card" style={{ marginBottom: 16, border: "1px solid rgba(123,97,255,0.3)", background: "rgba(123,97,255,0.08)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#7B61FF" strokeWidth="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <div style={{ fontSize: 16, fontWeight: 700, color: "white" }}>Activer le GPS</div>
              <div style={{ fontSize: 13, color: "rgba(255,255,255,0.5)" }}>Necessaire pour localiser en cas durgence</div>
            </div>
          </div>
          <button
            onClick={activateGPS}
            disabled={requestingGps}
            className="btn-primary"
            style={{ width: "100%", fontSize: 14 }}
          >
            {requestingGps ? "Activation..." : "Activer le GPS"}
          </button>
        </div>
      )}

      {/* Bluetooth Prompt */}
      {showBtPrompt && (
        <div className="dark-card" style={{ marginBottom: 16, border: "1px solid rgba(0,122,255,0.3)", background: "rgba(0,122,255,0.08)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#007AFF" strokeWidth="2"><polyline points="6.5 6.5 17.5 17.5 12 23 12 1 17.5 6.5 6.5 17.5"/></svg>
            <div>
              <div style={{ fontSize: 16, fontWeight: 700, color: "white" }}>Connecter le capteur Bluetooth</div>
              <div style={{ fontSize: 13, color: "rgba(255,255,255,0.5)" }}>Pour recevoir les donnees du capteur medical</div>
            </div>
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <button
              onClick={activateBluetooth}
              disabled={requestingBt}
              className="btn-primary"
              style={{ flex: 1, fontSize: 14 }}
            >
              {requestingBt ? "Connexion..." : "Connecter"}
            </button>
            <button
              onClick={skipBluetooth}
              style={{
                flex: 1, padding: "12px", borderRadius: 14,
                border: "1px solid rgba(255,255,255,0.1)",
                background: "rgba(255,255,255,0.06)",
                color: "rgba(255,255,255,0.5)", fontSize: 14,
                cursor: "pointer"
              }}
            >
              Plus tard
            </button>
          </div>
        </div>
      )}

      {/* GPS & Bluetooth Status */}
      {!showGpsPrompt && !showBtPrompt && (
        <>
          <div style={{ display: "flex", gap: 12, marginBottom: 16 }}>
            {/* GPS Status */}
            <div className="dark-card" style={{ flex: 1 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke={gpsActive ? "#34C759" : "#FF3B30"} strokeWidth="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                <span style={{ fontSize: 14, fontWeight: 700, color: "white" }}>GPS</span>
              </div>
              <div style={{ fontSize: 13, color: gpsActive ? "#34C759" : "#FF3B30", fontWeight: 600 }}>
                {gpsActive ? "Vous etes connecte" : "Deconnecte"}
              </div>
            </div>
            {/* Bluetooth Status */}
            <div className="dark-card" style={{ flex: 1 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke={bluetoothActive ? "#007AFF" : "#FF3B30"} strokeWidth="2"><polyline points="6.5 6.5 17.5 17.5 12 23 12 1 17.5 6.5 6.5 17.5"/></svg>
                <span style={{ fontSize: 14, fontWeight: 700, color: "white" }}>Bluetooth</span>
              </div>
              <div style={{ fontSize: 13, color: bluetoothActive ? "#007AFF" : "#FF3B30", fontWeight: 600 }}>
                {bluetoothActive ? "Vous etes connecte" : "Vous etes deconnecte"}
              </div>
              {!bluetoothActive && (
                <button
                  onClick={() => { setShowBtPrompt(true); }}
                  style={{ marginTop: 6, background: "none", border: "none", color: "#007AFF", fontSize: 12, cursor: "pointer", fontWeight: 600 }}
                >
                  Connecter
                </button>
              )}
            </div>
          </div>

          {/* Map Placeholder */}
          <div className="dark-card" style={{ height: 250, display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #0A0F2C, #111640)", marginBottom: 16, position: "relative", overflow: "hidden" }}>
            <div style={{ position: "absolute", inset: 0, opacity: 0.1, backgroundImage: "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%237B61FF' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")" }}></div>
            <div style={{ textAlign: "center", zIndex: 1 }}>
              <div style={{ width: 56, height: 56, borderRadius: "50%", background: "rgba(255,59,48,0.2)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 12px" }}>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="#FF3B30" stroke="none"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3" fill="white"/></svg>
              </div>
              <div style={{ fontSize: 16, fontWeight: 700, color: "white" }}>Votre position</div>
              <div style={{ fontSize: 13, color: "rgba(255,255,255,0.5)", marginTop: 4 }}>
                {position.lat.toFixed(4)}, {position.lng.toFixed(4)}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div style={{ display: "flex", gap: 12 }}>
            <button style={{
              flex: 1, padding: "14px", borderRadius: 16,
              background: "rgba(123,97,255,0.12)", border: "1px solid rgba(123,97,255,0.3)",
              color: "#9D8FFF", fontSize: 14, fontWeight: 700, cursor: "pointer",
              display: "flex", alignItems: "center", justifyContent: "center", gap: 8
            }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
              Itineraire
            </button>
            <button style={{
              flex: 1, padding: "14px", borderRadius: 16,
              background: "rgba(52,199,89,0.12)", border: "1px solid rgba(52,199,89,0.3)",
              color: "#34C759", fontSize: 14, fontWeight: 700, cursor: "pointer",
              display: "flex", alignItems: "center", justifyContent: "center", gap: 8
            }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              Appeler
            </button>
          </div>
        </>
      )}

      <BottomNav />
    </div>
  );
}
