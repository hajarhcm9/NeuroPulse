"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import BottomNav from "@/components/BottomNav";

interface Medication {
  id: string;
  name: string;
  dosage: string;
  frequency: string;
  time: string;
  taken: boolean;
}

const defaultMeds: Medication[] = [
  { id: "1", name: "Depakine", dosage: "500mg", frequency: "2x/jour", time: "08:00 - 20:00", taken: false },
  { id: "2", name: "Keppra", dosage: "750mg", frequency: "2x/jour", time: "08:00 - 20:00", taken: false },
  { id: "3", name: "Rivotril", dosage: "0.5mg", frequency: "1x/jour", time: "21:00", taken: false },
];

export default function MedicationsPage() {
  const router = useRouter();
  const [meds, setMeds] = useState<Medication[]>(defaultMeds);
  const [showToast, setShowToast] = useState(false);
  const [toastMsg, setToastMsg] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [newName, setNewName] = useState("");
  const [newDosage, setNewDosage] = useState("");
  const [newFreq, setNewFreq] = useState("");
  const [newTime, setNewTime] = useState("");

  // Load from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("smart_guardian_medications");
      if (saved) {
        setMeds(JSON.parse(saved));
      }
    }
  }, []);

  // Save to localStorage
  const saveMeds = (newMeds: Medication[]) => {
    setMeds(newMeds);
    if (typeof window !== "undefined") {
      localStorage.setItem("smart_guardian_medications", JSON.stringify(newMeds));
    }
  };

  const takeMed = (id: string) => {
    const updated = meds.map(m => m.id === id ? { ...m, taken: !m.taken } : m);
    saveMeds(updated);
    const med = meds.find(m => m.id === id);
    if (med) {
      const newTaken = !med.taken;
      setToastMsg(newTaken ? `${med.name} pris !` : `${med.name} marque comme non pris`);
      setShowToast(true);
      setTimeout(() => setShowToast(false), 2500);
    }
  };

  const addMed = () => {
    if (newName && newDosage) {
      const newMed: Medication = {
        id: String(Date.now()),
        name: newName,
        dosage: newDosage,
        frequency: newFreq || "1x/jour",
        time: newTime || "08:00",
        taken: false
      };
      saveMeds([...meds, newMed]);
      setNewName("");
      setNewDosage("");
      setNewFreq("");
      setNewTime("");
      setShowAdd(false);
      setToastMsg("Medicament ajoute !");
      setShowToast(true);
      setTimeout(() => setShowToast(false), 2500);
    }
  };

  const removeMed = (id: string) => {
    saveMeds(meds.filter(m => m.id !== id));
    setToastMsg("Medicament supprime");
    setShowToast(true);
    setTimeout(() => setShowToast(false), 2500);
  };

  const resetMeds = () => {
    const reset = meds.map(m => ({ ...m, taken: false }));
    saveMeds(reset);
    setToastMsg("Medicaments reinitalises");
    setShowToast(true);
    setTimeout(() => setShowToast(false), 2500);
  };

  const takenCount = meds.filter(m => m.taken).length;
  const totalCount = meds.length;

  return (
    <div className="page-enter" style={{ minHeight: "100vh", padding: "20px 20px 100px" }}>
      {/* Toast */}
      {showToast && (
        <div style={{
          position: "fixed", top: 20, left: "50%", transform: "translateX(-50%)",
          padding: "12px 24px", borderRadius: 16, zIndex: 100,
          background: "rgba(52,199,89,0.2)", border: "1px solid rgba(52,199,89,0.3)",
          color: "#34C759", fontSize: 14, fontWeight: 600,
          animation: "slideInUp 0.3s ease-out"
        }}>
          {toastMsg}
        </div>
      )}

      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <button onClick={() => router.back()} style={{ background: "none", border: "none", color: "white", cursor: "pointer" }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m15 18-6-6 6-6"/></svg>
          </button>
          <h1 style={{ fontSize: 28, fontWeight: 800, color: "white" }}>Medicaments</h1>
        </div>
        <button
          onClick={() => setShowAdd(!showAdd)}
          style={{ background: "rgba(123,97,255,0.15)", border: "1px solid rgba(123,97,255,0.3)", borderRadius: 12, padding: "8px 12px", color: "#7B61FF", fontSize: 13, fontWeight: 600, cursor: "pointer" }}
        >
          + Ajouter
        </button>
      </div>

      {/* Progress Card */}
      <div className="dark-card card-enter card-enter-1" style={{ marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
          <span style={{ fontSize: 14, fontWeight: 600, color: "white" }}>Progression du jour</span>
          <span style={{ fontSize: 24, fontWeight: 900, color: takenCount === totalCount ? "#34C759" : "#7B61FF" }}>{takenCount}/{totalCount}</span>
        </div>
        {/* Progress bar */}
        <div style={{ height: 8, borderRadius: 4, background: "rgba(255,255,255,0.06)", overflow: "hidden" }}>
          <div style={{
            height: "100%", borderRadius: 4,
            background: takenCount === totalCount ? "#34C759" : "linear-gradient(90deg, #7B61FF, #9D8FFF)",
            width: `${totalCount > 0 ? (takenCount / totalCount) * 100 : 0}%`,
            transition: "width 0.5s ease"
          }}></div>
        </div>
        {takenCount === totalCount && (
          <div style={{ marginTop: 10, fontSize: 13, color: "#34C759", fontWeight: 600, display: "flex", alignItems: "center", gap: 6 }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M20 6 9 17l-5-5"/></svg>
            Tous les medicaments sont pris !
          </div>
        )}
      </div>

      {/* Add Medication Form */}
      {showAdd && (
        <div className="dark-card card-enter" style={{ marginBottom: 16, border: "1px solid rgba(123,97,255,0.2)" }}>
          <h3 style={{ fontSize: 15, fontWeight: 700, color: "white", marginBottom: 12 }}>Nouveau medicament</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <input type="text" value={newName} onChange={(e) => setNewName(e.target.value)} placeholder="Nom du medicament" className="input-dark" />
            <input type="text" value={newDosage} onChange={(e) => setNewDosage(e.target.value)} placeholder="Dosage (ex: 500mg)" className="input-dark" />
            <input type="text" value={newFreq} onChange={(e) => setNewFreq(e.target.value)} placeholder="Frequence (ex: 2x/jour)" className="input-dark" />
            <input type="text" value={newTime} onChange={(e) => setNewTime(e.target.value)} placeholder="Heure (ex: 08:00)" className="input-dark" />
            <button onClick={addMed} className="btn-primary" style={{ fontSize: 14 }}>Ajouter</button>
          </div>
        </div>
      )}

      {/* Medication Cards */}
      <div className="stagger-list" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {meds.map((med) => (
          <div
            key={med.id}
            className="dark-card"
            style={{
              borderLeft: `4px solid ${med.taken ? "#34C759" : "#FF9500"}`,
              opacity: med.taken ? 0.7 : 1,
              transition: "all 0.3s ease"
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 16, fontWeight: 700, color: med.taken ? "rgba(255,255,255,0.5)" : "white", textDecoration: med.taken ? "line-through" : "none" }}>
                  {med.name}
                </div>
                <div style={{ fontSize: 13, color: "rgba(255,255,255,0.4)", marginTop: 4 }}>
                  {med.dosage} - {med.frequency}
                </div>
                <div style={{ fontSize: 12, color: "rgba(255,255,255,0.3)", marginTop: 2 }}>
                  {med.time}
                </div>
              </div>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <button
                  onClick={() => removeMed(med.id)}
                  style={{
                    padding: "6px 10px", borderRadius: 10, border: "none",
                    background: "rgba(255,59,48,0.1)", color: "#FF6B6B",
                    fontSize: 11, cursor: "pointer"
                  }}
                >
                  X
                </button>
                <button
                  onClick={() => takeMed(med.id)}
                  style={{
                    padding: "8px 16px", borderRadius: 12, border: "none",
                    background: med.taken ? "rgba(52,199,89,0.15)" : "rgba(123,97,255,0.15)",
                    color: med.taken ? "#34C759" : "#7B61FF",
                    fontSize: 13, fontWeight: 700, cursor: "pointer"
                  }}
                >
                  {med.taken ? "Pris" : "Prendre"}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Reset Button */}
      {takenCount > 0 && (
        <button
          onClick={resetMeds}
          style={{
            marginTop: 16, width: "100%", padding: "12px", borderRadius: 14,
            border: "1px solid rgba(255,255,255,0.1)", background: "rgba(255,255,255,0.04)",
            color: "rgba(255,255,255,0.5)", fontSize: 13, cursor: "pointer"
          }}
        >
          Reinitialiser tous les medicaments
        </button>
      )}

      <BottomNav />
    </div>
  );
}
