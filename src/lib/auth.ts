"use client";

const AUTH_KEY = "smart_guardian_auth";
const USER_KEY = "smart_guardian_user";
const VERIFY_KEY = "smart_guardian_pending_verify";

export interface UserData {
  email: string;
  name: string;
  verified: boolean;
}

export function login(email: string, password: string): { success: boolean; message: string } {
  if (!email || !email.includes("@")) {
    return { success: false, message: "Veuillez entrer un email valide" };
  }
  if (!password || password.length < 6) {
    return { success: false, message: "Le mot de passe doit contenir au moins 6 caracteres" };
  }
  
  const name = email.split("@")[0].replace(/[._-]/g, " ").replace(/\b\w/g, l => l.toUpperCase());
  
  if (typeof window !== "undefined") {
    localStorage.setItem(AUTH_KEY, "true");
    localStorage.setItem(USER_KEY, JSON.stringify({ email, name, verified: false }));
    localStorage.setItem(VERIFY_KEY, "true");
  }
  
  return { success: true, message: "Connexion reussie" };
}

export function needsVerification(): boolean {
  if (typeof window === "undefined") return false;
  return localStorage.getItem(VERIFY_KEY) === "true";
}

export function verifyCode(code: string): { success: boolean; message: string } {
  const validCode = "123456";
  
  if (!code || code.length !== 6) {
    return { success: false, message: "Veuillez entrer un code a 6 chiffres" };
  }
  
  if (code !== validCode) {
    return { success: false, message: "Code invalide. Veuillez reessayer." };
  }
  
  if (typeof window !== "undefined") {
    localStorage.removeItem(VERIFY_KEY);
    const userData = JSON.parse(localStorage.getItem(USER_KEY) || "{}");
    userData.verified = true;
    localStorage.setItem(USER_KEY, JSON.stringify(userData));
  }
  
  return { success: true, message: "Verification reussie !" };
}

export function logout(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem(AUTH_KEY);
    localStorage.removeItem(USER_KEY);
    localStorage.removeItem(VERIFY_KEY);
  }
}

export function isLoggedIn(): boolean {
  if (typeof window === "undefined") return false;
  return localStorage.getItem(AUTH_KEY) === "true" && !needsVerification();
}

export function getUserData(): UserData | null {
  if (typeof window === "undefined") return null;
  const data = localStorage.getItem(USER_KEY);
  return data ? JSON.parse(data) : null;
}

export function getUserName(): string {
  const data = getUserData();
  return data?.name || "Utilisateur";
}
