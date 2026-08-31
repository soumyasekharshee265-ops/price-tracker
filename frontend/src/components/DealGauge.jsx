function DealGauge({ score, reasons = [] }) {
  const clampedScore = Math.max(0, Math.min(100, score));
  const angle = (clampedScore / 100) * 180;

  let verdict = 'Wait';
  let verdictColor = 'var(--neon-pink)';
  if (clampedScore >= 70) {
    verdict = 'Go Ahead & Buy';
    verdictColor = 'var(--neon-cyan)';
  } else if (clampedScore >= 45) {
    verdict = 'Could Be Better';
    verdictColor = '#f0c419';
  }

  return (
    <div className="deal-gauge">
      <svg viewBox="0 0 200 110" className="deal-gauge-svg">
        <path d="M 10 100 A 90 90 0 0 1 190 100" fill="none" stroke="#f472b6" strokeWidth="14" strokeLinecap="round" opacity="0.5" />
        <path d="M 10 100 A 90 90 0 0 1 190 100" fill="none" stroke="#f0c419" strokeWidth="14" strokeLinecap="round" opacity="0.5"
          strokeDasharray="188.5" strokeDashoffset="94.25" />
        <path d="M 10 100 A 90 90 0 0 1 190 100" fill="none" stroke="#38bdf8" strokeWidth="14" strokeLinecap="round" opacity="0.5"
          strokeDasharray="188.5" strokeDashoffset="141.4" />
        <line
          x1="100" y1="100"
          x2={100 - 70 * Math.cos((angle * Math.PI) / 180)}
          y2={100 - 70 * Math.sin((angle * Math.PI) / 180)}
          stroke="var(--text-primary)"
          strokeWidth="3"
          strokeLinecap="round"
        />
        <circle cx="100" cy="100" r="6" fill="var(--text-primary)" />
      </svg>

      <div className="deal-gauge-verdict" style={{ color: verdictColor }}>
        {verdict}
      </div>
      <div className="deal-gauge-score label">Deal Score: {clampedScore}/100</div>

      {reasons.length > 0 && (
        <ul className="deal-gauge-reasons">
          {reasons.map((reason, i) => (
            <li key={i}>{reason}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default DealGauge;