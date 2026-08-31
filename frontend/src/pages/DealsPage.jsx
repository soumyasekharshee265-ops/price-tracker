import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const API_BASE = 'http://127.0.0.1:8000/api';

function DealsPage() {
  const [searchParams] = useSearchParams();
  const type = searchParams.get('type');       
  const value = searchParams.get('value');      
  const minParam = searchParams.get('min');     
  const maxParam = searchParams.get('max');     
  const categoryParam = searchParams.get('category');

  const [categories, setCategories] = useState([]);
  const [activeCategory, setActiveCategory] = useState(categoryParam || 'All');
  const [deals, setDeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [heading, setHeading] = useState('All Deals');

  useEffect(() => {
    document.title = 'Deals — Price Tracker';
    setLoading(true);

    let url;
    if (type === 'under' && value) {
      url = `${API_BASE}/deals/under/${value}${minParam ? `?min_price=${minParam}` : ''}`;
      const rangeLabel = minParam && minParam !== '0'
        ? `₹${Number(minParam).toLocaleString('en-IN')} – ₹${Number(value).toLocaleString('en-IN')}`
        : `Under ₹${Number(value).toLocaleString('en-IN')}`;
      setHeading(`Deals: ${rangeLabel}`);
    } else if (type === 'discount' && value) {
      url = `${API_BASE}/deals/discount/${value}${maxParam ? `?max_percent=${maxParam}` : ''}`;
      const rangeLabel = maxParam ? `${value}% – ${maxParam}% Off` : `${value}%+ Off`;
      setHeading(`Deals: ${rangeLabel}`);
    } else {
      url =
        activeCategory === 'All'
          ? `${API_BASE}/deals`
          : `${API_BASE}/deals?category=${encodeURIComponent(activeCategory)}`;
      setHeading(activeCategory === 'All' ? 'All Deals' : activeCategory);
    }

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setDeals(data.deals || []);
        if (data.categories) setCategories(data.categories);
      })
      .catch(() => setDeals([]))
      .finally(() => setLoading(false));
  }, [type, value, minParam, maxParam, activeCategory]);

  const showSidebar = !type; 

  return (
    <>
      <Navbar />
      <div className="deals-page">
        {showSidebar && (
          <aside className="deals-page-sidebar">
            <h3>Filter</h3>
            <p className="label">Categories</p>
            <ul className="deals-page-categories">
              <li>
                <button className={activeCategory === 'All' ? 'active' : ''} onClick={() => setActiveCategory('All')}>
                  All
                </button>
              </li>
              {categories.map((cat) => (
                <li key={cat}>
                  <button className={activeCategory === cat ? 'active' : ''} onClick={() => setActiveCategory(cat)}>
                    {cat}
                  </button>
                </li>
              ))}
            </ul>
          </aside>
        )}

        <main className="deals-page-main">
          <h2 style={{ marginBottom: '1.2rem' }}>{heading}</h2>

          {loading && <p className="label">Loading deals...</p>}

          {!loading && deals.length === 0 && (
            <p className="label" style={{ color: 'var(--text-secondary)' }}>
              No deals here yet — check back soon, we refresh deals regularly.
            </p>
          )}

          <div className="deals-page-grid">
            {deals.map((deal) => (
              <a key={deal.id} href={deal.source_url} target="_blank" rel="noopener noreferrer" className="deals-page-card">
                <div className="deals-page-card-image">
                  {deal.image_url ? (
                    <img src={deal.image_url} alt={deal.title} />
                  ) : (
                    <span className="product-card-image-placeholder">No image</span>
                  )}
                </div>
                {deal.discount_percent && (
                  <span className="deals-page-badge">{Math.round(deal.discount_percent)}% off</span>
                )}
                <span className="label deals-page-platform">{deal.platform}</span>
                <p className="deals-page-title">{deal.title}</p>
                <div className="deals-page-price-row">
                  <span className="deals-page-price">₹{deal.price.toLocaleString('en-IN')}</span>
                  {deal.original_price && (
                    <span className="product-card-original-price">
                      ₹{deal.original_price.toLocaleString('en-IN')}
                    </span>
                  )}
                </div>
                {deal.rating && <div className="product-card-rating">★ {deal.rating}</div>}
              </a>
            ))}
          </div>
        </main>
      </div>
      <Footer />
    </>
  );
}

export default DealsPage;