import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CATEGORIES, PRICE_BUCKETS, DISCOUNT_BUCKETS } from './DealsSection';
import { API_BASE_URL } from '../config';

const SECTIONS = [
  { id: 'deals-price', label: 'Deals' },
  { id: 'deals-discount', label: 'Discounts' },
  { id: 'about', label: 'About' },
];

const CONTACT_EMAIL = 'soumyasekharshee265@gmail.com';

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();
  const [openDropdown, setOpenDropdown] = useState(null); 

  const toggleDropdown = (name) => {
    setOpenDropdown((prev) => (prev === name ? null : name));
  };
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [showContactEmail, setShowContactEmail] = useState(false);
  const [reviewForm, setReviewForm] = useState({ name: '', email: '', message: '', rating: 0 });
  const [submitting, setSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null); 

      const scrollToSection = (id) => {
    const el = document.getElementById(id);
    if (!el) return;
    const navbarHeight = document.querySelector('.navbar')?.offsetHeight || 80;
    const top = el.getBoundingClientRect().top + window.scrollY - navbarHeight - 20;
    window.scrollTo({ top, behavior: 'smooth' });
  };
    const handleCategoryClick = (categoryName) => {
    setOpenDropdown(null);
    navigate(`/deals?category=${encodeURIComponent(categoryName)}`);
  };

  const handlePriceClick = (price, index) => {
    setOpenDropdown(null);
    const minPrice = index === 0 ? 0 : PRICE_BUCKETS[index - 1];
    navigate(`/deals?type=under&value=${price}&min=${minPrice}`);
  };

  const handleDiscountClick = (pct, index) => {
    setOpenDropdown(null);
    const nextPct = DISCOUNT_BUCKETS[index + 1];
    navigate(`/deals?type=discount&value=${pct}${nextPct ? `&max=${nextPct}` : ''}`);
  };

    const closePanel = () => {
    setMenuOpen(false);
    setShowReviewForm(false);
    setShowContactEmail(false);
    setSubmitStatus(null);
  };

    const handleReviewFormChange = (field) => (e) => {
    setReviewForm((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleStarClick = (n) => {
    setReviewForm((prev) => ({ ...prev, rating: n }));
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    if (reviewForm.rating === 0) {
      setSubmitStatus('error');
      return;
    }
    setSubmitting(true);
    setSubmitStatus(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reviewForm),
      });

      if (!response.ok) throw new Error('Submit failed');

      setReviewForm({ name: '', email: '', message: '', rating: 0 });
      setSubmitStatus('success');
    } catch (err) {
      setSubmitStatus('error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <nav className="navbar">
        <span className="navbar-logo">✦ PRICE TRACKER</span>

                <div className="navbar-links">
          <div className="navbar-dropdown-wrapper">
            <button
              className="navbar-link"
              onClick={() => {
                scrollToSection('deals-price');
                toggleDropdown('deals');
              }}
            >
              Deals
              <span className="navbar-link-arrow">{openDropdown === 'deals' ? '▲' : '▼'}</span>
            </button>

            {openDropdown === 'deals' && (
              <div className="navbar-dropdown">
                {PRICE_BUCKETS.map((price, i) => (
                  <button
                    key={price}
                    className="navbar-dropdown-item"
                    onClick={() => handlePriceClick(price, i)}
                  >
                    Under ₹{price.toLocaleString('en-IN')}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="navbar-dropdown-wrapper">
            <button
              className="navbar-link"
              onClick={() => {
                scrollToSection('deals-discount');
                toggleDropdown('discounts');
              }}
            >
              Discounts
              <span className="navbar-link-arrow">{openDropdown === 'discounts' ? '▲' : '▼'}</span>
            </button>

            {openDropdown === 'discounts' && (
              <div className="navbar-dropdown">
                {DISCOUNT_BUCKETS.map((pct, i) => (
                  <button
                    key={pct}
                    className="navbar-dropdown-item"
                    onClick={() => handleDiscountClick(pct, i)}
                  >
                    Min. {pct}%
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="navbar-dropdown-wrapper">
            <button
              className="navbar-link"
              onClick={() => {
                scrollToSection('deals-categories');
                toggleDropdown('categories');
              }}
            >
              Top Categories
              <span className="navbar-link-arrow">{openDropdown === 'categories' ? '▲' : '▼'}</span>
            </button>

            {openDropdown === 'categories' && (
              <div className="navbar-dropdown">
                {CATEGORIES.map((cat) => (
                  <button
                    key={cat.name}
                    className="navbar-dropdown-item"
                    onClick={() => handleCategoryClick(cat.name)}
                  >
                    {cat.name}
                  </button>
                ))}
              </div>
            )}
          </div>

                    <button
            className="navbar-link"
            onClick={() => {
              setOpenDropdown(null);
              scrollToSection('about');
            }}
          >
            About
          </button>
        </div>

        <button
          className="navbar-hamburger"
          onClick={() => setMenuOpen(true)}
          aria-label="Open menu"
        >
          ☰
        </button>
      </nav>

      {menuOpen && (
        <div className="navbar-panel-overlay" onClick={closePanel}>
          <div className="navbar-panel" onClick={(e) => e.stopPropagation()}>
            <button
              className="navbar-panel-close"
              onClick={closePanel}
              aria-label="Close menu"
            >
              ✕
            </button>

                        {!showReviewForm ? (
              <>
                <h3>Get in touch</h3>
                <button
                  className="navbar-panel-item navbar-panel-item-button"
                  onClick={() => setShowContactEmail((prev) => !prev)}
                >
                  Contact us
                </button>
                {showContactEmail && (
                  <a className="navbar-contact-email" href={`mailto:${CONTACT_EMAIL}`}>
                    {CONTACT_EMAIL}
                  </a>
                )}
                <button
                  className="navbar-panel-item navbar-panel-item-button"
                  onClick={() => setShowReviewForm(true)}
                >
                  Review &amp; Feedback
                </button>
              </>
            ) : (
              <div className="navbar-suggest-form">
                <button
                  className="navbar-suggest-back"
                  onClick={() => {
                    setShowReviewForm(false);
                    setSubmitStatus(null);
                  }}
                >
                  ← Back
                </button>
                <h3>Review &amp; Feedback</h3>
                <p className="navbar-suggest-intro">
                  Tell us what you think — your feedback helps us improve.
                </p>
                <form onSubmit={handleReviewSubmit}>
                  <label>
                    Name
                    <input
                      type="text"
                      value={reviewForm.name}
                      onChange={handleReviewFormChange('name')}
                      required
                    />
                  </label>
                  <label>
                    Email
                    <input
                      type="email"
                      value={reviewForm.email}
                      onChange={handleReviewFormChange('email')}
                      required
                    />
                  </label>
                  <label>
                    Feedback
                    <textarea
                      value={reviewForm.message}
                      onChange={handleReviewFormChange('message')}
                      rows={4}
                      required
                    />
                  </label>
                  <label>
                    Rating
                    <div className="navbar-star-input">
                      {[1, 2, 3, 4, 5].map((n) => (
                        <span
                          key={n}
                          className={n <= reviewForm.rating ? 'star-filled' : 'star-empty'}
                          onClick={() => handleStarClick(n)}
                        >
                          ★
                        </span>
                      ))}
                    </div>
                  </label>
                  <button type="submit" className="navbar-suggest-submit" disabled={submitting}>
                    {submitting ? 'Sending...' : 'Submit'}
                  </button>
                  {submitStatus === 'success' && (
                    <p className="navbar-suggest-status success">Thanks for your feedback!</p>
                  )}
                  {submitStatus === 'error' && (
                    <p className="navbar-suggest-status error">
                      {reviewForm.rating === 0 ? 'Please select a star rating.' : 'Something went wrong. Please try again.'}
                    </p>
                  )}
                </form>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}

export default Navbar;