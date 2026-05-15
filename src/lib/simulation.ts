"use client";

export function generateHeartRate(): number {
  return Math.floor(Math.random() * 40) + 60;
}

export function generateSpO2(): number {
  return Math.floor(Math.random() * 5) + 95;
}

export function generateMovement(): number {
  return Math.floor(Math.random() * 100);
}

export function calculateRisk(hr: number, spo2: number, movement: number): "Faible" | "Moyen" | "Eleve" | "Critique" {
  if (hr > 120 || spo2 < 90 || movement > 80) return "Critique";
  if (hr > 100 || spo2 < 93 || movement > 60) return "Eleve";
  if (hr > 85 || spo2 < 95 || movement > 30) return "Moyen";
  return "Faible";
}


export interface RiskData {
  level: string;
  percent: number;
  color: string;
}

export function generateRiskLevel(): RiskData {
  const hr = generateHeartRate();
  const spo2 = generateSpO2();
  const movement = generateMovement();
  const level = calculateRisk(hr, spo2, movement);
  let percent = 15;
  let color = "#34C759";
  if (level === "Critique") { percent = 90; color = "#FF3B30"; }
  else if (level === "Eleve") { percent = 70; color = "#FF9500"; }
  else if (level === "Moyen") { percent = 45; color = "#FFCC00"; }
  else { percent = 15; color = "#34C759"; }
  return { level, percent, color };
}

export const simulatedAlerts = [
  { id: "1", type: "Crise", severity: "Critique", title: "Crise detectee", color: "#FF3B30", time: "14:32", date: "2025-01-15", heartRate: 135, spo2: 88, movement: 92, duration: "2m 15s", description: "Tachycardie et desaturation detectees" },
  { id: "2", type: "Anomalie", severity: "Warning", title: "Anomalie cardiaque", color: "#FF9500", time: "10:15", date: "2025-01-15", heartRate: 105, spo2: 92, movement: 65, duration: "45s", description: "Rythme cardiaque eleve" },
  { id: "3", type: "Alerte", severity: "Info", title: "Alerte informative", color: "#34C759", time: "08:45", date: "2025-01-14", heartRate: 88, spo2: 96, movement: 20, duration: "10s", description: "Variation legere detectee" },
  { id: "4", type: "Crise", severity: "Critique", title: "Crise severe", color: "#FF3B30", time: "22:10", date: "2025-01-13", heartRate: 142, spo2: 85, movement: 95, duration: "3m 30s", description: "Crise tonico-clonique" },
  { id: "5", type: "Anomalie", severity: "Warning", title: "Pointes epileptiques", color: "#FF9500", time: "16:20", date: "2025-01-12", heartRate: 98, spo2: 91, movement: 55, duration: "1m 05s", description: "Activite anormale EEG" },
];

export const simulatedHistory = [
  { id: "1", type: "Crise", date: "15 Jan 2025", time: "14:32", severity: "Critique", duration: "2m 15s", notes: "Crise tonico-clonique detectee", title: "Crise tonico-clonique", detail: "Duree: 2m 15s - Tachycardie 135bpm", color: "#FF3B30" },
  { id: "2", type: "Anomalie", date: "14 Jan 2025", time: "10:15", severity: "Warning", duration: "45s", notes: "Activite anormale detectee", title: "Anomalie cardiaque", detail: "Duree: 45s - HR eleve", color: "#FF9500" },
  { id: "3", type: "Rapport", date: "13 Jan 2025", time: "09:00", severity: "Info", duration: "-", notes: "Rapport hebdomadaire genere", title: "Rapport hebdomadaire", detail: "Resume de la semaine", color: "#34C759" },
  { id: "4", type: "Crise", date: "12 Jan 2025", time: "22:10", severity: "Critique", duration: "3m 30s", notes: "Crise partielle complexe", title: "Crise partielle complexe", detail: "Duree: 3m 30s - SpO2 85%", color: "#FF3B30" },
  { id: "5", type: "Anomalie", date: "11 Jan 2025", time: "16:20", severity: "Warning", duration: "1m 05s", notes: "Pointes epileptiques detectees", title: "Pointes epileptiques", detail: "Duree: 1m 05s - EEG anormal", color: "#FF9500" },
];

export const simulatedMedications = [
  { id: "1", name: "Depakine", dosage: "500mg", frequency: "2x/jour", time: "08:00 - 20:00", taken: true },
  { id: "2", name: "Keppra", dosage: "750mg", frequency: "2x/jour", time: "08:00 - 20:00", taken: false },
  { id: "3", name: "Rivotril", dosage: "0.5mg", frequency: "1x/jour", time: "21:00", taken: false },
];

export const simulatedWeeklySeizures = [
  { day: "Lun", count: 1 },
  { day: "Mar", count: 0 },
  { day: "Mer", count: 2 },
  { day: "Jeu", count: 1 },
  { day: "Ven", count: 0 },
  { day: "Sam", count: 3 },
  { day: "Dim", count: 1 },
];

export const simulatedDayNight = [
  { name: "Jour", value: 60, fill: "#7B61FF" },
  { name: "Nuit", value: 40, fill: "#4A3AFF" },
];

export const elevatedSymptoms = [
  { id: "1", name: "Rythme cardiaque eleve", value: "135 bpm", icon: "heart", level: "Critique", description: "Tachycardie detectee - au-dessus du seuil normal" },
  { id: "2", name: "SpO2 bas", value: "88%", icon: "oxygen", level: "Critique", description: "Desaturation en oxygene - en dessous de 90%" },
  { id: "3", name: "Mouvements anormaux", value: "92%", icon: "movement", level: "Eleve", description: "Mouvements involontaires intenses detectes" },
  { id: "4", name: "Activite EEG anormale", value: "Pointes", icon: "brain", level: "Eleve", description: "Pointes epileptiques sur le signal EEG" },
  { id: "5", name: "Transpiration excessive", value: "Detectee", icon: "sweat", level: "Moyen", description: "Variation de conductivite cutanee" },
  { id: "6", name: "Temperature corporelle", value: "37.8C", icon: "temp", level: "Moyen", description: "Legere hyperthermie detectee" },
];

export const familyContacts = [
  { id: "1", name: "Maman", phone: "+212 6 12 34 56 78", relation: "Parent" },
  { id: "2", name: "Papa", phone: "+212 6 87 65 43 21", relation: "Parent" },
  { id: "3", name: "Dr. Alaoui", phone: "+212 6 55 44 33 22", relation: "Medecin" },
];
