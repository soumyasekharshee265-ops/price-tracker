function SimilarDeals({ products }) {
  if (!products || products.length === 0) return null;

  return (
    <div className="similar-deals">
      <h2>✦ Similar Deals</h2>
      <p className="label similar-deals-subtitle">
        Found {products.length}+ similar products
      </p>

      <div className="similar-deals-grid">
        {products.map((product) => (
          <a key={product.source_url} href={product.source_url} target="_blank" rel="noopener noreferrer" className="similar-deal-card">
            <div className="similar-deal-image">
              {product.image_url ? (
                <img src={product.image_url} alt={product.name} />
              ) : (
                <span className="product-card-image-placeholder">No image</span>
              )}
            </div>
            <span className="label similar-deal-platform">{product.platform}</span>
            <p className="similar-deal-title">{product.name}</p>
            <div className="similar-deal-price-row">
              <span className="similar-deal-price">
                ₹{product.current_price.toLocaleString('en-IN')}
              </span>
              {product.original_price && (
                <span className="product-card-original-price">
                  ₹{product.original_price.toLocaleString('en-IN')}
                </span>
              )}
            </div>
            <span className="similar-deal-button">View Product →</span>
          </a>
        ))}
      </div>
    </div>
  );
}

export default SimilarDeals;