"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { generateHeartRate, generateSpO2, generateMovement, generateRiskLevel } from "@/lib/simulation";
import BottomNav from "@/components/BottomNav";
import RiskGauge from "@/components/RiskGauge";

export default function MonitoringPage() {
  const router = useRouter();
  const [hr, setHr] = useState(72);
  const [spo2, setSpo2] = useState(98);
  const [move, setMove] = useState(12);
  const [risk, setRisk] = useState({ level: "Faible", percent: 15, color: "#34C759" });
  const [seconds, setSeconds] = useState(0);
  const [sensorConnected, setSensorConnected] = useState(true);
  const [beepEnabled, setBeepEnabled] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const eegDataRef = useRef<number[]>([]);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const animFrameRef = useRef<number>(0);

  // Beep sound using Web Audio API
  const playBeep = useCallback((heartRate: number) => {
    if (!beepEnabled || typeof window === "undefined") return;
    try {
      if (!audioCtxRef.current) {
        audioCtxRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
      }
      const ctx = audioCtxRef.current;
      const oscillator = ctx.createOscillator();
      const gainNode = ctx.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(ctx.destination);
      
      oscillator.frequency.value = 880;
      oscillator.type = "sine";
      
      gainNode.gain.setValueAtTime(0.08, ctx.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.1);
      
      oscillator.start(ctx.currentTime);
      oscillator.stop(ctx.currentTime + 0.1);
    } catch {}
  }, [beepEnabled]);

  // Generate EEG data
  const generateEEGPoint = useCallback(() => {
    const t = Date.now() / 1000;
    const base = Math.sin(t * 3) * 20;
    const alpha = Math.sin(t * 10) * 8;
    const beta = Math.sin(t * 25) * 3;
    const spike = Math.random() > 0.95 ? (Math.random() - 0.5) * 60 : 0;
    const noise = (Math.random() - 0.5) * 5;
    return base + alpha + beta + spike + noise;
  }, []);

  // Draw EEG canvas
  const drawEEG = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;

    // Add new data point
    eegDataRef.current.push(generateEEGPoint());
    if (eegDataRef.current.length > width / 2) {
      eegDataRef.current.shift();
    }

    // Clear
    ctx.clearRect(0, 0, width, height);

    // Grid
    ctx.strokeStyle = "rgba(123, 97, 255, 0.06)";
    ctx.lineWidth = 1;
    for (let y = 0; y < height; y += 20) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
    for (let x = 0; x < width; x += 20) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }

    // Center line
    ctx.strokeStyle = "rgba(123, 97, 255, 0.15)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, height / 2);
    ctx.lineTo(width, height / 2);
    ctx.stroke();

    // EEG signal
    const data = eegDataRef.current;
    if (data.length < 2) return;

    // Glow
    ctx.strokeStyle = "rgba(123, 97, 255, 0.3)";
    ctx.lineWidth = 4;
    ctx.beginPath();
    for (let i = 0; i < data.length; i++) {
      const x = (i / data.length) * width;
      const y = height / 2 - data[i];
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Main line
    ctx.strokeStyle = "#7B61FF";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let i = 0; i < data.length; i++) {
      const x = (i / data.length) * width;
      const y = height / 2 - data[i];
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Moving dot at end
    if (data.length > 0) {
      const lastX = width;
      const lastY = height / 2 - data[data.length - 1];
      ctx.beginPath();
      ctx.arc(lastX, lastY, 3, 0, Math.PI * 2);
      ctx.fillStyle = "#7B61FF";
      ctx.fill();
      ctx.beginPath();
      ctx.arc(lastX, lastY, 6, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(123, 97, 255, 0.3)";
      ctx.fill();
    }

    animFrameRef.current = requestAnimationFrame(drawEEG);
  }, [generateEEGPoint]);

  // Update vitals every 2 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      const newHr = generateHeartRate();
      const newSpo2 = generateSpO2();
      const newMove = generateMovement();
      const newRisk = generateRiskLevel();
      
      setHr(newHr);
      setSpo2(newSpo2);
      setMove(newMove);
      setRisk(newRisk);
      setLastUpdate(new Date());
      
      // Beep on each heart beat
      playBeep(newHr);
    }, 2000);
    return () => clearInterval(interval);
  }, [playBeep]);

  // Seconds counter
  useEffect(() => {
    const timer = setInterval(() => {
      setSeconds(s => s + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Sensor connection simulation
  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() > 0.95) {
        setSensorConnected(false);
        setTimeout(() => setSensorConnected(true), 2000);
      }
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Start EEG animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      canvas.width = canvas.offsetWidth * 2;
      canvas.height = canvas.offsetHeight * 2;
      const ctx = canvas.getContext("2d");
      if (ctx) ctx.scale(2, 2);
    }
    
    animFrameRef.current = requestAnimationFrame(drawEEG);
    return () => cancelAnimationFrame(animFrameRef.current);
  }, [drawEEG]);

  const formatTime = (s: number) => {
    const min = Math.floor(s / 60);
    const sec = s % 60;
    return `${min.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
  };

  const timeSinceUpdate = Math.floor((Date.now() - lastUpdate.getTime()) / 1000);

  return (
    <div className="page-enter" style={{ minHeight: "100vh", padding: "20px 20px 100px" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <button onClick={() => router.back()} style={{ background: "none", border: "none", color: "white", cursor: "pointer" }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m15 18-6-6 6-6"/></svg>
          </button>
          <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Monitoring</h1>
        </div>
        {/* Sensor Status */}
        <div style={{ display: "flex", alignItems: "center", gap: 6, padding: "6px 12px", borderRadius: 12, background: sensorConnected ? "rgba(52,199,89,0.12)" : "rgba(255,59,48,0.12)", border: `1px solid ${sensorConnected ? "rgba(52,199,89,0.3)" : "rgba(255,59,48,0.3)"}` }}>
          <div style={{ width: 8, height: 8, borderRadius: 4, background: sensorConnected ? "#34C759" : "#FF3B30", boxShadow: sensorConnected ? "0 0 8px rgba(52,199,89,0.6)" : "0 0 8px rgba(255,59,48,0.6)", animation: sensorConnected ? "breathe 2s ease-in-out infinite" : "none" }}></div>
          <span style={{ fontSize: 11, fontWeight: 700, color: sensorConnected ? "#34C759" : "#FF3B30" }}>
            {sensorConnected ? "Capteur actif" : "Deconnecte"}
          </span>
          {/* Bluetooth icon */}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke={sensorConnected ? "#34C759" : "#FF3B30"} strokeWidth="2"><polyline points="6.5 6.5 17.5 17.5 12 23 12 1 17.5 6.5 6.5 17.5"/></svg>
        </div>
      </div>

      {/* Risk Gauge */}
      <div className="dark-card card-enter card-enter-1" style={{ textAlign: "center", marginBottom: 16 }}>
        <RiskGauge level={risk.level} percent={risk.percent} color={risk.color} />
      </div>

      {/* Vital Signs Cards */}
      <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
        <div className="vital-card card-enter card-enter-2" style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8 }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="#FF3B30" stroke="none"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
            <span style={{ fontSize: 11, color: "rgba(255,255,255,0.5)", fontWeight: 600 }}>FC</span>
          </div>
          <div className="number-animate" style={{ fontSize: 28, fontWeight: 900, color: "#FF3B30" }}>{hr}</div>
          <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)" }}>bpm</div>
        </div>

        <div className="vital-card card-enter card-enter-3" style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8 }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#007AFF" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/></svg>
            <span style={{ fontSize: 11, color: "rgba(255,255,255,0.5)", fontWeight: 600 }}>SpO2</span>
          </div>
          <div className="number-animate" style={{ fontSize: 28, fontWeight: 900, color: "#007AFF" }}>{spo2}</div>
          <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)" }}>%</div>
        </div>

        <div className="vital-card card-enter card-enter-4" style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8 }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FF9500" strokeWidth="2"><path d="M5 3v4h4"/><path d="M19 21v-4h-4"/><path d="M5 7a8 8 0 0 1 14 2"/><path d="M19 17a8 8 0 0 1-14-2"/></svg>
            <span style={{ fontSize: 11, color: "rgba(255,255,255,0.5)", fontWeight: 600 }}>Mvt</span>
          </div>
          <div className="number-animate" style={{ fontSize: 28, fontWeight: 900, color: "#FF9500" }}>{move}</div>
          <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)" }}>%</div>
        </div>
      </div>

      {/* Beep Toggle */}
      <div className="dark-card card-enter card-enter-4" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={beepEnabled ? "#7B61FF" : "rgba(255,255,255,0.3)"} strokeWidth="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
          <div>
            <div style={{ fontSize: 14, fontWeight: 600, color: "white" }}>Son cardiaque</div>
            <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)" }}>Bip a chaque battement</div>
          </div>
        </div>
        <button
          onClick={() => setBeepEnabled(!beepEnabled)}
          style={{
            width: 48, height: 28, borderRadius: 14, border: "none",
            background: beepEnabled ? "#7B61FF" : "rgba(255,255,255,0.1)",
            position: "relative", cursor: "pointer", transition: "all 0.3s ease"
          }}
        >
          <div style={{
            width: 22, height: 22, borderRadius: 11, background: "white",
            position: "absolute", top: 3,
            left: beepEnabled ? 23 : 3,
            transition: "all 0.3s ease",
            boxShadow: "0 2px 4px rgba(0,0,0,0.2)"
          }}></div>
        </button>
      </div>

      {/* EEG Signal */}
      <div className="dark-card card-enter card-enter-5" style={{ marginBottom: 16, padding: "12px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{ width: 8, height: 8, borderRadius: 4, background: "#7B61FF", boxShadow: "0 0 8px rgba(123,97,255,0.6)" }}></div>
            <span style={{ fontSize: 13, fontWeight: 700, color: "white" }}>Signal EEG</span>
          </div>
          <span style={{ fontSize: 11, color: "rgba(255,255,255,0.3)" }}>Temps reel</span>
        </div>
        <canvas
          ref={canvasRef}
          style={{
            width: "100%",
            height: 140,
            borderRadius: 12,
            background: "rgba(7, 11, 43, 0.6)",
          }}
        />
      </div>

      {/* Time Info */}
      <div className="dark-card card-enter card-enter-6" style={{ display: "flex", justifyContent: "space-between" }}>
        <div>
          <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)" }}>Duree monitoring</div>
          <div style={{ fontSize: 20, fontWeight: 800, color: "white", fontFamily: "monospace" }}>{formatTime(seconds)}</div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)" }}>Derniere MAJ</div>
          <div style={{ fontSize: 20, fontWeight: 800, color: timeSinceUpdate > 5 ? "#FF9500" : "#34C759", fontFamily: "monospace" }}>
            il y a {timeSinceUpdate}s
          </div>
        </div>
      </div>

      <BottomNav />
    </div>
  );
}
