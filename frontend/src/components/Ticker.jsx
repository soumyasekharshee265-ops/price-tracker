const TICKER_ITEMS = [
  'COMPARE PRICES',
  'REAL-TIME DEALS',
  'SMART BUY/WAIT ALERTS',
  'MULTI-SITE SEARCH',
  'PRICE HISTORY TRACKING',
  'PASTE ANY PRODUCT LINK',
];

function Ticker() {
  const items = [...TICKER_ITEMS, ...TICKER_ITEMS];

  return (
    <div className="ticker-wrapper">
      <div className="ticker-track">
        {items.map((item, i) => (
          <span key={i} className="ticker-item label">
            {item}
            <span className="ticker-dot">•</span>
          </span>
        ))}
      </div>
    </div>
  );
}

export default Ticker;