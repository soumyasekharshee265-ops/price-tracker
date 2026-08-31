import { useNavigate } from 'react-router-dom';

const PRICE_BUCKETS = [99, 199, 299, 399, 499, 599, 799, 999, 1499, 1999, 2999, 4999];
const DISCOUNT_BUCKETS = [40, 50, 60, 70, 80];
const CATEGORIES = [
  { name: 'Smartphones', price: '14,999' },
  { name: 'Laptops', price: '34,999' },
  { name: 'Headphones', price: '999' },
  { name: 'Smart TVs', price: '6,999' },
  { name: 'Refrigerators', price: '14,999' },
  { name: 'Washing Machines', price: '16,999' },
  { name: 'Air Conditioners', price: '28,999' },
  { name: 'Water Purifiers', price: '9,999' },
  { name: 'Smart Watches', price: '1,999' },
  { name: 'Cameras', price: '19,999' },
  { name: 'Speakers', price: '1,499' },
  { name: 'Kitchen Appliances', price: '2,499' },
];

export { CATEGORIES, PRICE_BUCKETS, DISCOUNT_BUCKETS };

function DealsSection() {
  const navigate = useNavigate();

  return (
    <section id="deals" className="deals-section">
      <div className="deals-section-inner">

        <div id="deals-price" className="deals-subsection">
          <h2>Unmissable Deals</h2>
          <div className="deals-grid">
            {PRICE_BUCKETS.map((price, i) => {
              const minPrice = i === 0 ? 0 : PRICE_BUCKETS[i - 1];
              return (
                <div
                  key={price}
                  className="deal-bucket-card"
                  onClick={() => navigate(`/deals?type=under&value=${price}&min=${minPrice}`)}
                  style={{ cursor: 'pointer' }}
                >
                  <span className="label">Deals Under</span>
                  <h3>₹{price.toLocaleString('en-IN')}</h3>
                  <span className="deal-bucket-arrow">→</span>
                </div>
              );
            })}
          </div>
        </div>

        <div id="deals-discount" className="deals-subsection">
          <h2>Best Discounts &amp; Verified Steals</h2>
          <div className="deals-grid">
            {DISCOUNT_BUCKETS.map((pct, i) => {
              const nextPct = DISCOUNT_BUCKETS[i + 1];
              return (
                <div
                  key={pct}
                  className="deal-bucket-card deal-bucket-card-discount"
                  onClick={() =>
                    navigate(`/deals?type=discount&value=${pct}${nextPct ? `&max=${nextPct}` : ''}`)
                  }
                  style={{ cursor: 'pointer' }}
                >
                  <span className="label">Min.</span>
                  <h3>{pct}% off</h3>
                  <span className="deal-bucket-arrow">→</span>
                </div>
              );
            })}
          </div>
        </div>

        <div id="deals-categories" className="deals-subsection">
          <h2>Shop by Top Categories</h2>
          <div className="deals-grid deals-grid-categories">
            {CATEGORIES.map((cat) => (
              <div
                key={cat.name}
                className="category-card"
                onClick={() => navigate(`/deals?category=${encodeURIComponent(cat.name)}`)}
                style={{ cursor: 'pointer' }}
              >
                <span className="label">Starting from</span>
                <h3>₹{cat.price}</h3>
                <p>{cat.name}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}

export default DealsSection;