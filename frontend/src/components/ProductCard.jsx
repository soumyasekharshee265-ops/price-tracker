function ProductCard({ product, index = 0 }) {
  const handleMouseMove = (e) => {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty('--cursor-x', `${x}px`);
    card.style.setProperty('--cursor-y', `${y}px`);
  };

  return (
    <div
      className="product-card"
      style={{ animationDelay: `${index * 0.08}s` }}
      onMouseMove={handleMouseMove}
    >
      <div className="product-card-glow" />
      <div className="product-card-image">
        {product.image_url ? (
          <img src={product.image_url} alt={product.name} />
        ) : (
          <div className="product-card-image-placeholder">No Image</div>
        )}
      </div>
      <h3 className="product-card-title">{product.name}</h3>
      <div className="product-card-price-row">
        <span className="product-card-price">₹{product.current_price}</span>
        {product.original_price && (
          <span className="product-card-original-price">₹{product.original_price}</span>
        )}
      </div>
      {product.rating && (
        <div className="product-card-rating">⭐ {product.rating}</div>
      )}
      <button className="product-card-button">View Details</button>
    </div>
  );
}

export default ProductCard;