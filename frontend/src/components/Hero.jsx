import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const ALL_POPULAR_PRODUCTS = [
  'iPhone 15', 'MacBook Air', 'Sony WH-1000XM5', 'Samsung S24',
  'boAt Airdopes', 'Nike Air Max', 'PS5 Console', 'Nothing Phone',
  'Dell XPS 13', 'Fire-Boltt Smartwatch', 'OnePlus 12', 'iPad Air',
  'Adidas Ultraboost', 'Noise ColorFit', 'Redmi Note 13', 'HP Pavilion',
  'JBL Flip 6', 'Puma Running Shoes', 'Realme Narzo', 'Canon DSLR',
  'Levis Jeans', 'Titan Watch', 'Lenovo IdeaPad', 'Skullcandy Earbuds',
  'Vivo V29', 'Croma Air Fryer', 'Woodland Boots', 'Sony Bravia TV',
  'Asus ROG Laptop', 'Fossil Watch', 'Xiaomi Power Bank', 'Puma T-Shirt',
  'Samsung Galaxy Tab', 'Bose QuietComfort', 'Nike Running Shoes', 'Oppo Reno',
  'Roadster Jacket', 'Mi Band 8', 'Ray-Ban Sunglasses', 'Apple Watch SE',
];

function getDailyPopularSearches() {
  const daysSinceEpoch = Math.floor(Date.now() / (1000 * 60 * 60 * 24));
  const groupCount = Math.floor(ALL_POPULAR_PRODUCTS.length / 4);
  const groupIndex = daysSinceEpoch % groupCount;
  const startIndex = groupIndex * 4;
  return ALL_POPULAR_PRODUCTS.slice(startIndex, startIndex + 4);
}

const POPULAR_SEARCHES = getDailyPopularSearches();

const STATS = [
  { value: '1000+', label: 'Products Tracked', icon: 'box', color: 'blue' },
  { value: '5K+', label: 'Users', icon: 'users', color: 'purple' },
  { value: '20+', label: 'Stores', icon: 'store', color: 'green' },
  { value: '99.9%', label: 'Uptime', icon: 'shield', color: 'orange' },
];

const STAT_ICONS = {
  box: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21 8l-9-5-9 5 9 5 9-5z" />
      <path d="M3 8v8l9 5 9-5V8" />
      <path d="M12 13v8" />
    </svg>
  ),
  users: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="9" cy="8" r="3.5" />
      <path d="M2 20c0-3.5 3-6 7-6s7 2.5 7 6" />
      <circle cx="17" cy="8" r="3" />
      <path d="M16 14.5c2.8.4 5 2.6 5 5.5" />
    </svg>
  ),
  store: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M3 9l1.5-5h15L21 9" />
      <path d="M4 9v10h16V9" />
      <path d="M9 19v-6h6v6" />
    </svg>
  ),
  shield: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M12 2l8 3v6c0 5-3.5 8.5-8 11-4.5-2.5-8-6-8-11V5l8-3z" />
      <path d="M9 12l2 2 4-4" />
    </svg>
  ),
};

const PRICE_CARDS = [
  { platform: 'Amazon', price: '₹54,999', original: '₹59,999', discount: '9% OFF', accent: 'amazon' },
  { platform: 'Flipkart', price: '₹52,499', original: '₹58,999', discount: '11% OFF', accent: 'flipkart' },
  { platform: 'Myntra', price: '₹51,999', original: '₹57,999', discount: '12% OFF', accent: 'myntra' },
];

const textVariants = {
  hidden: { opacity: 0, x: -40 },
  visible: (i) => ({
    opacity: 1,
    x: 0,
    transition: { delay: i * 0.15, duration: 0.6, ease: 'easeOut' },
  }),
};

const cardVariants = {
  hidden: { opacity: 0, x: 40 },
  visible: (i) => ({
    opacity: 1,
    x: 0,
    transition: { delay: 0.3 + i * 0.15, duration: 0.6, ease: 'easeOut' },
  }),
};

function Hero() {
  const navigate = useNavigate();

  const scrollToSearch = () => {
    document.getElementById('search-section')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleChipClick = (term) => {
    navigate(`/compare?q=${encodeURIComponent(term)}`);
  };

  return (
    <section className="hero-section">
      <div className="hero-text">
        <motion.span
          custom={0}
          initial="hidden"
          animate="visible"
          variants={textVariants}
          className="hero-badge"
        >
          Track Prices. Save More.
        </motion.span>

        <motion.h1
          custom={1}
          initial="hidden"
          animate="visible"
          variants={textVariants}
        >
          Find your next <span className="hero-accent">best deal.</span>
        </motion.h1>

        <motion.p
          custom={2}
          initial="hidden"
          animate="visible"
          variants={textVariants}
          className="hero-subtext"
        >
          Compare prices across Amazon, Flipkart, Myntra and more: get AI insights, price history & alerts to never pay more than you should.
        </motion.p>

        <motion.button
          custom={3}
          initial="hidden"
          animate="visible"
          variants={textVariants}
          className="hero-cta-button"
          onClick={scrollToSearch}
        >
          Start Comparing ↓
        </motion.button>

        <motion.div
          custom={4}
          initial="hidden"
          animate="visible"
          variants={textVariants}
          className="hero-popular-searches"
        >
          <span className="hero-popular-label">Popular Searches:</span>
          {POPULAR_SEARCHES.map((term) => (
            <button
              key={term}
              className="hero-search-chip"
              onClick={() => handleChipClick(term)}
            >
              {term}
            </button>
          ))}
        </motion.div>
        <motion.div
          custom={5}
          initial="hidden"
          animate="visible"
          variants={textVariants}
          className="hero-stats-bar"
        >
          {STATS.map((stat) => (
            <div key={stat.label} className="hero-stat">
              <span className={`hero-stat-icon hero-stat-icon-${stat.color}`}>
                {STAT_ICONS[stat.icon]}
              </span>
              <div className="hero-stat-text">
                <span className={`hero-stat-value hero-stat-value-${stat.color}`}>{stat.value}</span>
                <span className="hero-stat-label">{stat.label}</span>
              </div>
            </div>
          ))}
        </motion.div>
      </div>

      <div className="hero-masonry">
        {PRICE_CARDS.map((card, i) => (
          <div
            key={card.platform}
            className={`hero-price-card-tilt hero-price-card-tilt-${i}`}
          >
            <motion.div
              custom={i}
              initial="hidden"
              animate="visible"
              variants={cardVariants}
              className={`hero-price-card hero-price-card-${card.accent}`}
            >
              <div className="hero-price-card-header">
                <span className={`hero-price-card-icon hero-price-card-icon-${card.accent}`}>
                  {card.platform[0]}
                </span>
                <span className="hero-price-card-platform">{card.platform}</span>
              </div>
              <div className="hero-price-card-row">
                <span className="hero-price-card-current">{card.price}</span>
                <span className="hero-price-card-original">{card.original}</span>
              </div>
              <span className="hero-price-card-badge">{card.discount}</span>
            </motion.div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Hero;