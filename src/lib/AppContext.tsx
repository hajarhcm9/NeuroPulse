"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface AppState {
  // User
  userName: string;
  userEmail: string;
  isVerified: boolean;
  
  // Vitals
  heartRate: number;
  spo2: number;
  movement: number;
  riskLevel: string;
  riskPercent: number;
  riskColor: string;
  
  // Sensor
  sensorConnected: boolean;
  bluetoothConnected: boolean;
  
  // Preferences
  notifications: boolean;
  soundAlerts: boolean;
  autoCall: boolean;
  gpsTracking: boolean;
  
  // Counts
  activeAlerts: number;
  medicationsTaken: number;
  medicationsTotal: number;
}

const defaultState: AppState = {
  userName: "Utilisateur",
  userEmail: "",
  isVerified: false,
  heartRate: 72,
  spo2: 98,
  movement: 12,
  riskLevel: "Faible",
  riskPercent: 15,
  riskColor: "#34C759",
  sensorConnected: true,
  bluetoothConnected: false,
  notifications: true,
  soundAlerts: true,
  autoCall: true,
  gpsTracking: true,
  activeAlerts: 0,
  medicationsTaken: 0,
  medicationsTotal: 3,
};

interface AppContextType {
  state: AppState;
  setState: (partial: Partial<AppState>) => void;
  resetState: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, setStateInternal] = useState<AppState>(defaultState);

  // Load from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("smart_guardian_state");
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          setStateInternal({ ...defaultState, ...parsed });
        } catch {}
      }
      
      // Also load user data
      const userData = localStorage.getItem("smart_guardian_user");
      if (userData) {
        try {
          const user = JSON.parse(userData);
          setStateInternal(prev => ({
            ...prev,
            userName: user.name || "Utilisateur",
            userEmail: user.email || "",
            isVerified: user.verified || false,
          }));
        } catch {}
      }
      
      // Load preferences
      const prefs = localStorage.getItem("smart_guardian_prefs");
      if (prefs) {
        try {
          const p = JSON.parse(prefs);
          setStateInternal(prev => ({
            ...prev,
            notifications: p.notifications ?? true,
            soundAlerts: p.soundAlerts ?? true,
            autoCall: p.autoCall ?? true,
            gpsTracking: p.gpsTracking ?? true,
          }));
        } catch {}
      }
    }
  }, []);

  const setState = (partial: Partial<AppState>) => {
    setStateInternal((prev) => {
      const newState = { ...prev, ...partial };
      // Persist to localStorage
      if (typeof window !== "undefined") {
        const { heartRate, spo2, movement, riskLevel, riskPercent, riskColor, ...toSave } = newState;
        localStorage.setItem("smart_guardian_state", JSON.stringify(toSave));
      }
      return newState;
    });
  };

  const resetState = () => {
    setStateInternal(defaultState);
    if (typeof window !== "undefined") {
      localStorage.removeItem("smart_guardian_state");
    }
  };

  return (
    <AppContext.Provider value={{ state, setState, resetState }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppState() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppState must be used within AppProvider");
  }
  return context;
}
