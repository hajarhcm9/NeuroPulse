export function generateHeartRate(base = 72): number {
  return Math.max(55, base + Math.sin(Date.now() / 3000) * 8 + (Math.random() - 0.5) * 6);
}

export function generateSpO2(base = 98): number {
  return Math.min(100, Math.max(90, base + Math.sin(Date.now() / 4000) * 1.5 + (Math.random() - 0.5) * 0.8));
}

export function generateMovement(base = 0.3): number {
  return Math.max(0, base + Math.sin(Date.now() / 2000) * 0.2 + (Math.random() - 0.5) * 0.1);
}

export function generateRiskLevel() {
  const hour = new Date().getHours();
  const baseRisk = (hour >= 2 && hour <= 6) ? 35 : 18;
  const percent = baseRisk + Math.floor(Math.random() * 5);
  if (percent < 30) return { level: "Faible", percent, color: "#00D26A" };
  if (percent < 50) return { level: "Modere", percent, color: "#FFD43B" };
  if (percent < 70) return { level: "Eleve", percent, color: "#FF8A00" };
  return { level: "Critique", percent, color: "#FF3B30" };
}

export const simulatedAlerts = [
  { id: "1", type: "critical", title: "Alerte critique", description: "Risque de crise detecte", heartRate: 120, spo2: 96, time: "14:30", color: "#FF3B30" },
  { id: "2", type: "warning", title: "Risque eleve", description: "Activite cerebrale anormale", heartRate: 95, spo2: 97, time: "12:15", color: "#FF8A00" },
  { id: "3", type: "info", title: "Medicament pris", description: "Lamotrigine 100mg", heartRate: 72, spo2: 98, time: "08:00", color: "#00D26A" },
  { id: "4", type: "info", title: "Activite physique", description: "30 min marche", heartRate: 88, spo2: 99, time: "07:30", color: "#FFD43B" },
  { id: "5", type: "warning", title: "Sommeil agite", description: "Mouvements detectes", heartRate: 68, spo2: 95, time: "03:20", color: "#FF8A00" },
];

export const simulatedHistory = [
  { id: 1, type: "risk", title: "Risque eleve detecte", detail: "85%", time: "14:30", color: "#FF3B30" },
  { id: 2, type: "crises", title: "Crise detectee", detail: "2 min 34 sec", time: "12:15", color: "#FF3B30" },
  { id: 3, type: "rapports", title: "Medicament pris", detail: "Lamotrigine 100mg", time: "08:00", color: "#00D26A" },
  { id: 4, type: "evenements", title: "Activite physique", detail: "30 min", time: "07:30", color: "#FFD43B" },
  { id: 5, type: "evenements", title: "Sommeil", detail: "7h45", time: "23:00", color: "#4AA8FF" },
];

export const simulatedMedications = [
  { id: 1, name: "Lamotrigine", dosage: "100mg", time: "08:00", taken: true },
  { id: 2, name: "Valproate de sodium", dosage: "250mg", time: "14:00", taken: false },
  { id: 3, name: "Lamotrigine", dosage: "100mg", time: "20:00", taken: false },
];

export const simulatedWeeklySeizures = [
  { week: "S1", count: 1 },
  { week: "S2", count: 0 },
  { week: "S3", count: 2 },
  { week: "S4", count: 1 },
];

export const simulatedDayNight = [
  { name: "Jour", value: 65, fill: "#7B61FF" },
  { name: "Nuit", value: 35, fill: "#1A144B" },
];
