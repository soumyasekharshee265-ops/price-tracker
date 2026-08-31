const FEATURES = [
  {
    tag: '01, MULTI-SITE',
    title: 'Compare Everywhere at Once',
    desc: 'One search pulls prices from Amazon, Flipkart, and Meesho together — no more opening a dozen tabs.',
    badge: 'ALL PLATFORMS',
  },
  {
    tag: '02, FLEXIBLE SEARCH',
    title: 'Paste a Product',
    desc: 'Drop in a product link, or just search the exact product name — either works, though a name search tends to catch more matches.',
    badge: 'LINK OR NAME',
  },
  {
    tag: '03, AI VERDICT',
    title: 'Should You Buy Now?',
    desc: 'Our AI checks the current price against its history and tells you straight — buy now, or wait it out.',
    badge: 'SMART SUGGESTION',
  },
  {
    tag: '04, PRICE HISTORY',
    title: 'See Where the Price Has Been',
    desc: 'A full price-history graph for every product, so you know if today’s "deal" is actually a deal.',
    badge: 'FULL TIMELINE',
  },
];

function FeatureHighlights() {
  return (
    <section id="features" className="features-section">
      <div className="features-section-inner">
      <div className="features-heading"></div>
        <span className="label">WHY USE US</span>
        <h2>Built to Save You From 12 Open Tabs</h2>
      </div>

      {FEATURES.map((feature, i) => (
        <div
          key={feature.title}
          className={`feature-row ${i % 2 === 1 ? 'feature-row-reverse' : ''}`}
        >
          <div className="feature-text">
            <span className="label feature-tag">{feature.tag}</span>
            <h3>{feature.title}</h3>
            <p>{feature.desc}</p>
          </div>
          <div className="feature-visual">
            <span className="feature-badge">{feature.badge}</span>
          </div>
        </div>
      ))}
    </section>
  );
}

export default FeatureHighlights;