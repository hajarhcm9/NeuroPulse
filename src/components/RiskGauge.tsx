'use client';

interface RiskGaugeProps {
  percent: number;
  level: string;
  color: string;
}

export default function RiskGauge({ percent, level, color }: RiskGaugeProps) {
  const angle = (percent / 100) * 180;
  const radius = 90;
  const cx = 100;
  const cy = 100;

  const needleX = cx + radius * 0.7 * Math.cos(((180 - angle) * Math.PI) / 180);
  const needleY = cy - radius * 0.7 * Math.sin(((180 - angle) * Math.PI) / 180);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <svg width="200" height="120" viewBox="0 0 200 120">
        {/* Background arc segments */}
        <path d="M 10 100 A 90 90 0 0 1 100 10" stroke="#00D26A" strokeWidth="12" fill="none" strokeLinecap="round" opacity="0.3" />
        <path d="M 100 10 A 90 90 0 0 1 155 35" stroke="#FFD43B" strokeWidth="12" fill="none" strokeLinecap="round" opacity="0.3" />
        <path d="M 155 35 A 90 90 0 0 1 185 80" stroke="#FF8A00" strokeWidth="12" fill="none" strokeLinecap="round" opacity="0.3" />
        <path d="M 185 80 A 90 90 0 0 1 190 100" stroke="#FF3B30" strokeWidth="12" fill="none" strokeLinecap="round" opacity="0.3" />

        {/* Active arc */}
        <path
          d="M 10 100 A 90 90 0 0 1 190 100"
          stroke={color}
          strokeWidth="12"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={`${(percent / 100) * 283} 283`}
          style={{ filter: `drop-shadow(0 0 8px ${color})` }}
        />

        {/* Needle */}
        <line x1={cx} y1={cy} x2={needleX} y2={needleY} stroke="white" strokeWidth="3" strokeLinecap="round" />
        <circle cx={cx} cy={cy} r="6" fill="white" />

        {/* Labels */}
        <text x="15" y="115" fill="#00D26A" fontSize="10" fontWeight="600">Faible</text>
        <text x="165" y="115" fill="#FF3B30" fontSize="10" fontWeight="600">Critique</text>
      </svg>

      <div style={{ textAlign: 'center', marginTop: -10 }}>
        <div style={{ fontSize: 36, fontWeight: 800, color }}>{percent}%</div>
        <div style={{ fontSize: 16, fontWeight: 600, color: '#C5C8E1' }}>{level}</div>
      </div>
      <div style={{ fontSize: 13, color: '#8D91B5', marginTop: 4 }}>Risque de crise</div>
    </div>
  );
}