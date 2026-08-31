import DealGauge from './DealGauge';
import PriceHistoryCard from './PriceHistoryCard';

function FeaturedProduct({ product, dealScore }) {
  return (
    <div className="featured-product">
      <div className="featured-product-main">
        <div className="featured-product-image">
          {product.image_url ? (
            <img src={product.image_url} alt={product.name} />
          ) : (
            <span className="product-card-image-placeholder">No image</span>
          )}
        </div>

        <div className="featured-product-info">
          <span className="label featured-product-platform">{product.platform}</span>
          <h2>{product.name}</h2>

          <div className="featured-product-price-row">
            <span className="featured-product-price">
              ₹{product.current_price.toLocaleString('en-IN')}
            </span>
            {product.original_price && (
              <span className="product-card-original-price">
                ₹{product.original_price.toLocaleString('en-IN')}
              </span>
            )}
          </div>

          {product.rating && (
            <div className="product-card-rating">★ {product.rating} rating</div>
          )}

          <a href={product.source_url} target="_blank" rel="noopener noreferrer" className="product-card-button featured-product-button">
            View on {product.platform || 'site'}
          </a>
        </div>
      </div>

      <div className="featured-product-details">
        {dealScore && <DealGauge score={dealScore.deal_score} reasons={dealScore.reasons} />}
        <PriceHistoryCard productId={product.product_id} />
      </div>
    </div>
  );
}

export default FeaturedProduct;