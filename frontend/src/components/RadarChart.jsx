import { useMemo } from 'react';

const RadarChart = ({ scores = {} }) => {
  // 6 RIASEC dimensions
  const dimensions = [
    { key: 'Realistic', label: 'Realistic (R)' },
    { key: 'Investigative', label: 'Investigative (I)' },
    { key: 'Artistic', label: 'Artistic (A)' },
    { key: 'Social', label: 'Social (S)' },
    { key: 'Enterprising', label: 'Enterprising (E)' },
    { key: 'Conventional', label: 'Conventional (C)' }
  ];

  const size = 380;
  const center = size / 2;
  const radius = 115;
  const totalAxes = dimensions.length;
  const angleStep = (Math.PI * 2) / totalAxes;

  // Calculate polygon points for grid rings & student data
  const chartData = useMemo(() => {
    const gridRings = [0.2, 0.4, 0.6, 0.8, 1.0].map((ringPct) => {
      const points = dimensions.map((_, i) => {
        const angle = i * angleStep - Math.PI / 2;
        const r = radius * ringPct;
        const x = center + r * Math.cos(angle);
        const y = center + r * Math.sin(angle);
        return `${x},${y}`;
      }).join(' ');
      return { pct: ringPct * 100, points };
    });

    const dataPoints = dimensions.map((dim, i) => {
      const rawVal = scores[dim.key] ?? scores[`${dim.key}_Score`] ?? 50;
      const pct = Math.min(100, Math.max(10, parseFloat(rawVal)));
      const angle = i * angleStep - Math.PI / 2;
      const r = (radius * pct) / 100;
      const x = center + r * Math.cos(angle);
      const y = center + r * Math.sin(angle);

      // Label positions slightly further out
      const labelR = radius + 36;
      const lx = center + labelR * Math.cos(angle);
      const ly = center + labelR * Math.sin(angle);

      return { key: dim.key, label: dim.label, value: pct, x, y, lx, ly };
    });

    const polygonPoints = dataPoints.map((p) => `${p.x},${p.y}`).join(' ');

    return { gridRings, dataPoints, polygonPoints };
  }, [scores]);

  return (
    <div className="radar-chart-wrapper" style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
      <svg 
        width={size} 
        height={size} 
        viewBox={`0 0 ${size} ${size}`} 
        className="radar-svg"
        style={{ maxWidth: '100%', height: 'auto', overflow: 'visible' }}
      >
        <defs>
          <linearGradient id="radarGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.65" />
            <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.4" />
          </linearGradient>
        </defs>

        {/* Grid Hexagon Rings */}
        {chartData.gridRings.map((ring, idx) => (
          <polygon key={idx} points={ring.points} className="radar-grid-ring" />
        ))}

        {/* Axis Lines */}
        {chartData.dataPoints.map((dp, i) => {
          const angle = i * angleStep - Math.PI / 2;
          const ax = center + radius * Math.cos(angle);
          const ay = center + radius * Math.sin(angle);
          return (
            <line key={i} x1={center} y1={center} x2={ax} y2={ay} className="radar-axis-line" />
          );
        })}

        {/* Student Score Filled Polygon */}
        <polygon 
          points={chartData.polygonPoints} 
          fill="url(#radarGrad)" 
          stroke="#8b5cf6" 
          strokeWidth="2.5" 
          className="radar-polygon" 
        />

        {/* Data Point Nodes & High-Contrast Labels */}
        {chartData.dataPoints.map((dp, i) => (
          <g key={i}>
            <circle cx={dp.x} cy={dp.y} r="5" className="radar-node" />
            <text 
              x={dp.lx} 
              y={dp.ly} 
              textAnchor="middle" 
              dominantBaseline="middle" 
              className="radar-label"
              style={{
                fontFamily: 'var(--sans)',
                fontSize: '13px',
                fontWeight: '700',
                fill: 'var(--text-heading)'
              }}
            >
              {dp.key} ({dp.value}%)
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
};

export default RadarChart;
