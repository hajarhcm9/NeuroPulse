import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Smart Guardian — Epilepsy AI",
  description: "Surveillance intelligente de crises d'épilepsie",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body>
        <div className="mobile-container">
          {children}
        </div>
      </body>
    </html>
  );
}