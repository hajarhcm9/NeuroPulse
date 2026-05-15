"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { AppProvider } from "@/lib/AppContext";
import InstallPrompt from "@/components/InstallPrompt";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [displayChildren, setDisplayChildren] = useState(children);
  const [transitionStage, setTransitionStage] = useState("enter");

  useEffect(() => {
    setTransitionStage("exit");
    const timeout = setTimeout(() => {
      setDisplayChildren(children);
      setTransitionStage("enter");
    }, 150);
    return () => clearTimeout(timeout);
  }, [pathname, children]);

  // Register service worker
  useEffect(() => {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/sw.js").catch(() => {
        // Service worker registration failed silently
      });
    }
  }, []);

  return (
    <html lang="fr">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
        <meta name="theme-color" content="#070B2B" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <meta name="description" content="Smart Guardian - Protection intelligente contre l'epilepsie" />
        <link rel="manifest" href="/manifest.json" />
        <link rel="apple-touch-icon" href="/icons/icon-192x192.png" />
        <title>Smart Guardian</title>
      </head>
      <body style={{ margin: 0, padding: 0, background: "#070B2B", overflowX: "hidden" }}>
        <AppProvider>
          <div
            style={{
              maxWidth: 430,
              margin: "0 auto",
              minHeight: "100vh",
              position: "relative",
              background: "#070B2B",
              transition: "opacity 0.15s ease, transform 0.15s ease",
              opacity: transitionStage === "enter" ? 1 : 0,
              transform: transitionStage === "enter" ? "translateY(0)" : "translateY(8px)",
            }}
          >
            {displayChildren}
          </div>
          <InstallPrompt />
        </AppProvider>
      </body>
    </html>
  );
}
