'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Heart, Droplets, Move, AlertTriangle } from 'lucide-react';
import BottomNav from '@/components/BottomNav';
import RiskGauge from '@/components/RiskGauge';
import { generateHeartRate, generateSpO2, generateMovement, generateRiskLevel } from '@/lib/simulation';

export default function DashboardPage() {
  const router = useRouter();
  const [hr, setHr] = useState(72);
  const [spo2, setSpo2] = useState(98);
  const [move, setMove] = useState(0.3);
  const [risk, setRisk] = useState({ level: 'Faible', percent: 18, color: '#00D26A' });

  useEffect(() => {
    const interval = setInterval(() => {
      setHr(Math.round(generateHeartRate()));
      setSpo2(Math.round(generateSpO2() * 10) / 10);
      setMove(Math.round(generateMovement() * 100) / 100);
      setRisk(generateRiskLevel());
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ minHeight: '100vh', padding: '20px 20px 100px' }} className="page-enter">
      <h1 style={{ fontSize: 28, fontWeight: 800, color: 'white' }}>Bonjour Ahmed 👋</h1>
      <p style={{ fontSize: 15, color: '#8D91B5', marginTop: 4 }}>Restez en sécurité aujourd&apos;hui</p>

      {/* Risk Gauge Card */}
      <div className="dark-card" style={{ marginTop: 24, alignItems: 'center', display: 'flex', flexDirection: 'column' }}>
        <RiskGauge percent={risk.percent} level={risk.level} color={risk.color} />
      </div>

      {/* Status */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 20, justifyContent: 'center' }}>
        <div style={{ width: 10, height: 10, borderRadius: 5, background: '#00D26A', boxShadow: '0 0 10px #00D26A' }} />
        <span style={{ fontSize: 16, fontWeight: 600, color: '#00D26A' }}>Tout est stable</span>
      </div>

      {/* Vital Cards */}
      <div style={{ display: 'flex', gap: 12, marginTop: 20 }}>
        <div className="vital-card">
          <Heart size={22} color="#00D26A" style={{ marginBottom: 6 }} />
          <div style={{ fontSize: 22, fontWeight: 800, color: '#00D26A' }}>{hr}</div>
          <div style={{ fontSize: 11, color: '#8D91B5', marginTop: 2 }}>bpm</div>
        </div>
        <div className="vital-card">
          <Droplets size={22} color="#4AA8FF" style={{ marginBottom: 6 }} />
          <div style={{ fontSize: 22, fontWeight: 800, color: '#4AA8FF' }}>{spo2}%</div>
          <div style={{ fontSize: 11, color: '#8D91B5', marginTop: 2 }}>SpO2</div>
        </div>
        <div className="vital-card">
          <Move size={22} color="#FFD43B" style={{ marginBottom: 6 }} />
          <div style={{ fontSize: 16, fontWeight: 700, color: '#FFD43B', marginTop: 4 }}>Faible</div>
          <div style={{ fontSize: 11, color: '#8D91B5', marginTop: 2 }}>Mouvements</div>
        </div>
      </div>

      {/* Start Monitoring Button */}
      <button className="btn-primary" style={{ marginTop: 24 }} onClick={() => router.push('/monitoring')}>
        Démarrer la surveillance
      </button>

      {/* SOS FAB */}
      <button
        onClick={() => router.push('/sos')}
        style={{
          position: 'fixed', bottom: 100, right: 'calc(50% - 195px)',
          width: 56, height: 56, borderRadius: 28,
          background: 'linear-gradient(135deg, #FF375F, #FF1744)',
          border: 'none', cursor: 'pointer', display: 'flex',
          alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 0 20px rgba(255,55,95,0.5)', zIndex: 40,
        }}
      >
        <AlertTriangle size={24} color="white" />
      </button>

      <BottomNav />
    </div>
  );
}