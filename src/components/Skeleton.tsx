"use client";

import { useEffect, useState } from "react";

interface SkeletonProps {
  type?: "card" | "list" | "chart" | "vitals";
  count?: number;
}

export default function Skeleton({ type = "card", count = 3 }: SkeletonProps) {
  const [visible, setVisible] = useState(true);

  if (!visible) return null;

  if (type === "vitals") {
    return (
      <div style={{ display: "flex", gap: 10 }}>
        {[1, 2, 3].map((i) => (
          <div key={i} style={{ flex: 1 }} className="shimmer-loading" >
            <div style={{ height: 90, borderRadius: 16 }}></div>
          </div>
        ))}
      </div>
    );
  }

  if (type === "chart") {
    return (
      <div className="shimmer-loading" style={{ height: 200, borderRadius: 20, marginBottom: 16 }}></div>
    );
  }

  if (type === "list") {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {Array.from({ length: count }).map((_, i) => (
          <div key={i} className="skeleton-card">
            <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
              <div className="skeleton-circle"></div>
              <div style={{ flex: 1 }}>
                <div className="skeleton-line" style={{ width: "60%" }}></div>
                <div className="skeleton-line" style={{ width: "40%" }}></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  // Default card skeleton
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="skeleton-card">
          <div className="skeleton-line" style={{ width: "80%" }}></div>
          <div className="skeleton-line" style={{ width: "60%" }}></div>
          <div className="skeleton-line" style={{ width: "40%" }}></div>
        </div>
      ))}
    </div>
  );
}
