import { useEffect, useState } from 'react';
import { API_BASE_URL } from '../config';

function StarDisplay({ rating }) {
  return (
    <span className="review-stars">
      {[1, 2, 3, 4, 5].map((n) => (
        <span key={n} className={n <= rating ? 'star-filled' : 'star-empty'}>★</span>
      ))}
    </span>
  );
}

function ReviewsSection() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/reviews?limit=30`)
      .then((res) => res.json())
      .then((data) => setReviews(data.reviews || []))
      .catch(() => setReviews([]));
  }, []);

  if (reviews.length === 0) return null;

  const row = [...reviews, ...reviews];

  return (
    <section className="ideas-section">
      <h2 className="ideas-section-title">What our users say</h2>

      <div className="ideas-row ideas-row-ltr">
        <div className="ideas-track">
          {row.map((review, i) => (
            <div className="idea-card" key={`ltr-${review.id}-${i}`}>
              <StarDisplay rating={review.rating} />
              <p className="idea-text">"{review.message}"</p>
              <span className="idea-name">— {review.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="ideas-row ideas-row-rtl">
        <div className="ideas-track">
          {row.map((review, i) => (
            <div className="idea-card" key={`rtl-${review.id}-${i}`}>
              <StarDisplay rating={review.rating} />
              <p className="idea-text">"{review.message}"</p>
              <span className="idea-name">— {review.name}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default ReviewsSection;