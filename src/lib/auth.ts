const AUTH_KEY = "smart-guardian-auth";

export function login(email: string, password: string): boolean {
  if (email && password.length >= 4) {
    localStorage.setItem(AUTH_KEY, JSON.stringify({ email, loggedIn: true, name: "Ahmed" }));
    return true;
  }
  return false;
}

export function logout(): void {
  localStorage.removeItem(AUTH_KEY);
}

export function isLoggedIn(): boolean {
  if (typeof window === "undefined") return false;
  const data = localStorage.getItem(AUTH_KEY);
  if (!data) return false;
  try {
    return JSON.parse(data).loggedIn === true;
  } catch {
    return false;
  }
}

export function getUserName(): string {
  if (typeof window === "undefined") return "Ahmed";
  const data = localStorage.getItem(AUTH_KEY);
  if (!data) return "Ahmed";
  try {
    return JSON.parse(data).name || "Ahmed";
  } catch {
    return "Ahmed";
  }
}
