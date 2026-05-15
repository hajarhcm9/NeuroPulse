"use client";

import { useState, useEffect } from "react";

interface RiskGaugeProps {
  level: string;
  percent: number;
  color: string;
}

export default function RiskGauge({ level, percent, color }: RiskGaugeProps) {
  const [animatedPercent, setAnimatedPercent] = useState(0);
  const [animatedColor, setAnimatedColor] = useState("#34C759");

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedPercent(percent);
      setAnimatedColor(color);
    }, 100);
    return () => clearTimeout(timer);
  }, [percent, color]);

  const angle = (animatedPercent / 100) * 180 - 90;
  const radius = 80;
  const cx = 100;
  const cy = 95;

  const needleX = cx + radius * Math.cos((angle * Math.PI) / 180);
  const needleY = cy + radius * Math.sin((angle * Math.PI) / 180);

  // Arc path
  const startAngle = -180;
  const endAngle = 0;
  const segments = 40;
  const arcPoints = [];
  for (let i = 0; i <= segments; i++) {
    const a = startAngle + (endAngle - startAngle) * (i / segments);
    const x = cx + radius * Math.cos((a * Math.PI) / 180);
    const y = cy + radius * Math.sin((a * Math.PI) / 180);
    arcPoints.push({ x, y });
  }

  const filledSegments = Math.floor((animatedPercent / 100) * segments);

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <svg width="200" height="120" viewBox="0 0 200 120">
        {/* Background arc */}
        <path
          d={`M ${arcPoints[0].x} ${arcPoints[0].y} ${arcPoints.slice(1).map((p, i) => `L ${p.x} ${p.y}`).join(" ")}`}
          fill="none"
          stroke="rgba(255,255,255,0.08)"
          strokeWidth="10"
          strokeLinecap="round"
        />

        {/* Filled arc with gradient */}
        {filledSegments > 0 && (
          <path
            d={`M ${arcPoints[0].x} ${arcPoints[0].y} ${arcPoints.slice(1, filledSegments + 1).map((p) => `L ${p.x} ${p.y}`).join(" ")}`}
            fill="none"
            stroke={animatedColor}
            strokeWidth="10"
            strokeLinecap="round"
            style={{
              filter: `drop-shadow(0 0 8px ${animatedColor}66)`,
              transition: "all 1s ease-out",
            }}
          />
        )}

        {/* Tick marks */}
        {[0, 25, 50, 75, 100].map((tick) => {
          const a = -180 + (tick / 100) * 180;
          const outerR = radius + 14;
          const innerR = radius + 8;
          return (
            <line
              key={tick}
              x1={cx + innerR * Math.cos((a * Math.PI) / 180)}
              y1={cy + innerR * Math.sin((a * Math.PI) / 180)}
              x2={cx + outerR * Math.cos((a * Math.PI) / 180)}
              y2={cy + outerR * Math.sin((a * Math.PI) / 180)}
              stroke="rgba(255,255,255,0.15)"
              strokeWidth="2"
            />
          );
        })}

        {/* Needle */}
        <line
          x1={cx}
          y1={cy}
          x2={needleX}
          y2={needleY}
          stroke={animatedColor}
          strokeWidth="3"
          strokeLinecap="round"
          style={{
            filter: `drop-shadow(0 0 6px ${animatedColor}88)`,
            transition: "all 1s ease-out",
          }}
        />

        {/* Center dot */}
        <circle cx={cx} cy={cy} r="6" fill={animatedColor} style={{ transition: "all 1s ease-out", filter: `drop-shadow(0 0 4px ${animatedColor}66)` }} />
        <circle cx={cx} cy={cy} r="3" fill="white" />
      </svg>

      {/* Level text */}
      <div style={{ textAlign: "center", marginTop: -4 }}>
        <div
          className="number-animate"
          style={{
            fontSize: 28,
            fontWeight: 900,
            color: animatedColor,
            transition: "color 1s ease-out",
            filter: `drop-shadow(0 0 8px ${animatedColor}44)`,
          }}
        >
          {animatedPercent}%
        </div>
        <div style={{ fontSize: 13, fontWeight: 700, color: "rgba(255,255,255,0.5)", marginTop: 2, letterSpacing: 2, textTransform: "uppercase" }}>
          {level}
        </div>
      </div>
    </div>
  );
}
