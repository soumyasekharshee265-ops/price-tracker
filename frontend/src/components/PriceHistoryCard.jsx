import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

const API_BASE = 'http://127.0.0.1:8000/api';

const RANGES = [
  { label: '1 Week', days: 7 },
  { label: '3 Weeks', days: 21 },
  { label: '1 Month', days: 30 },
];

function PriceHistoryCard({ productId }) {
  const [selectedDays, setSelectedDays] = useState(7);
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!productId) return;

    setLoading(true);
    fetch(`${API_BASE}/trends/${productId}?days=${selectedDays}`)
      .then((res) => res.json())
      .then(setTrends)
      .catch(() => setTrends(null))
      .finally(() => setLoading(false));
  }, [productId, selectedDays]);

  return (
    <div className="price-history-card">
      <div className="price-history-header">
        <h3>Price History</h3>
        <div className="price-history-filters">
          {RANGES.map((range) => (
            <button
              key={range.days}
              className={`price-history-filter ${selectedDays === range.days ? 'active' : ''}`}
              onClick={() => setSelectedDays(range.days)}
            >
              {range.label}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <p className="label" style={{ color: 'var(--text-secondary)' }}>Loading...</p>
      )}

      {!loading && (!trends || trends.history.length === 0) && (
        <p className="label" style={{ color: 'var(--text-secondary)' }}>
          No price history in this range yet.
        </p>
      )}

      {!loading && trends && trends.history.length === 1 && (
        <p className="label" style={{ color: 'var(--text-secondary)' }}>
          Price history just started — check back after a few more searches to see trends.
        </p>
      )}

      {!loading && trends && trends.history.length > 1 && (
        <>
          <div className="price-stats-grid">
            <div className="price-stat">
              <span className="label">Highest</span>
              <strong>₹{trends.highest_price.toLocaleString('en-IN')}</strong>
            </div>
            <div className="price-stat">
              <span className="label">Average</span>
              <strong>₹{trends.average_price.toLocaleString('en-IN')}</strong>
            </div>
            <div className="price-stat">
              <span className="label">Lowest</span>
              <strong>₹{trends.lowest_price.toLocaleString('en-IN')}</strong>
            </div>
            <div className="price-stat">
              <span className="label">Current</span>
              <strong>₹{trends.current_price.toLocaleString('en-IN')}</strong>
            </div>
          </div>

          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={trends.history.map((point) => ({
              date: new Date(point.recorded_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }),
              price: point.price,
            }))}>
              <CartesianGrid stroke="rgba(139,92,246,0.1)" />
              <XAxis dataKey="date" stroke="#8b93a7" fontSize={12} />
              <YAxis stroke="#8b93a7" fontSize={12} domain={['auto', 'auto']} />
              <Tooltip
                contentStyle={{ background: '#141a28', border: '1px solid rgba(139,92,246,0.3)', borderRadius: 8 }}
                labelStyle={{ color: '#f5f7ff' }}
              />
              <Line type="monotone" dataKey="price" stroke="#38bdf8" strokeWidth={2} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
}

export default PriceHistoryCard;