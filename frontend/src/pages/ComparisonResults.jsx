import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import FeaturedProduct from '../components/FeaturedProduct';
import SimilarDeals from '../components/SimilarDeals';

const API_BASE = 'http://127.0.0.1:8000/api';

const RELEVANCE_THRESHOLD = 0.6; 

function tokenize(text) {
  return new Set((text || '').toLowerCase().match(/[a-z0-9]+/g) || []);
}

function relevanceRatio(query, title) {
  const queryTokens = [...tokenize(query)];
  const titleTokens = tokenize(title);
  if (queryTokens.length === 0) return 0;

  let score = 0;
  let maxScore = 0;
  queryTokens.forEach((token) => {
    const weight = /\d/.test(token) ? 2 : 1;
    maxScore += weight;
    if (titleTokens.has(token)) score += weight;
  });

  return maxScore > 0 ? score / maxScore : 0;
}

function pickBestDeal(products, query) {
  const withRelevance = products.map((p) => ({
    ...p,
    _relevance: relevanceRatio(query, p.name),
  }));

  const relevant = withRelevance.filter((p) => p._relevance >= RELEVANCE_THRESHOLD);
  const notRelevant = withRelevance.filter((p) => p._relevance < RELEVANCE_THRESHOLD);

  const scoreDeal = (p) => {
    const discountScore = Math.min(p.discount_percent || 0, 100);
    const ratingScore = ((p.rating || 3) / 5) * 100;
    return discountScore * 0.6 + ratingScore * 0.4;
  };


  const rankedRelevant = relevant
    .map((p) => ({ ...p, _score: scoreDeal(p) }))
    .sort((a, b) => b._score - a._score);

  const rankedNotRelevant = notRelevant
    .map((p) => ({ ...p, _score: scoreDeal(p) }))
    .sort((a, b) => b._score - a._score);

  return [...rankedRelevant, ...rankedNotRelevant];
}

function ComparisonResults() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';

  const [products, setProducts] = useState([]);
  const [dealScore, setDealScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    document.title = query ? `${query} — Price Tracker` : 'Price Tracker';
    if (!query) return;

    setLoading(true);
    setError(null);
    setProducts([]);
    setDealScore(null);

    fetch(`${API_BASE}/search?query=${encodeURIComponent(query)}`)
      .then((response) => response.json())
      .then(async (data) => {
        const validProducts = (data.results || []).filter(
          (item) => !item.error && item.price && item.title
        );

        if (validProducts.length === 0) {
          setError('Enter a valid product');
          return;
        }

        const formatted = validProducts.map((item) => ({
          product_id: item.product_id,
          name: item.title,
          current_price: item.price,
          original_price: item.original_price,
          discount_percent: item.discount_percent,
          rating: item.rating,
          image_url: item.image_url,
          source_url: item.source_url,
          platform: item.platform,
        }));

        const ranked = pickBestDeal(formatted, query);
        setProducts(ranked);

        const featured = ranked[0];
        if (featured.product_id) {
          try {
            const scoreRes = await fetch(`${API_BASE}/deal-score/${featured.product_id}`);
            if (scoreRes.ok) setDealScore(await scoreRes.json());
          } catch {
          
          }
        }
      })
      .catch(() => setError('Something went wrong. Please try again.'))
      .finally(() => setLoading(false));
  }, [query]);

  const [featuredProduct, ...restProducts] = products;

  return (
    <div style={{ padding: '2rem 1.5rem' }}>
      <h1 style={{ maxWidth: 1100, margin: '0 auto 2rem' }}>Results for "{query}"</h1>

      {loading && (
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
          Searching...
        </p>
      )}

      {error && (
        <p style={{ textAlign: 'center', color: 'var(--neon-pink)' }}>
          {error}
        </p>
      )}

      {featuredProduct && (
        <FeaturedProduct product={featuredProduct} dealScore={dealScore} />
      )}

      <SimilarDeals products={restProducts} />
    </div>
  );
}

export default ComparisonResults;