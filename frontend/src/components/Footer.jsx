import { useState } from 'react';
import { API_BASE_URL } from '../config';

function Footer() {
  const [form, setForm] = useState({ name: '', email: '', suggestion: '' });
  const [submitting, setSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null); 

  const handleFormChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setSubmitStatus(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/suggestions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (!response.ok) throw new Error('Submit failed');

      setForm({ name: '', email: '', suggestion: '' });
      setSubmitStatus('success');
    } catch (err) {
      setSubmitStatus('error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <footer className="site-footer">
      <div className="footer-suggest">
        <h3>Suggest a feature</h3>
        <p className="footer-suggest-intro">
          You can suggest your idea and we'll try to implement it.
        </p>
        <form onSubmit={handleSubmit} className="footer-suggest-form">
          <label>
            Name
            <input
              type="text"
              value={form.name}
              onChange={handleFormChange('name')}
              required
            />
          </label>
          <label>
            Email
            <input
              type="email"
              value={form.email}
              onChange={handleFormChange('email')}
              required
            />
          </label>
          <label>
            Suggestion
            <textarea
              value={form.suggestion}
              onChange={handleFormChange('suggestion')}
              rows={4}
              required
            />
          </label>
          <button type="submit" className="footer-suggest-submit" disabled={submitting}>
            {submitting ? 'Sending...' : 'Submit'}
          </button>
          {submitStatus === 'success' && (
            <p className="footer-suggest-status success">Thanks! Your idea has been submitted.</p>
          )}
          {submitStatus === 'error' && (
            <p className="footer-suggest-status error">Something went wrong. Please try again.</p>
          )}
        </form>
      </div>

      <span className="footer-logo">✦ PRICE TRACKER</span>
      <p className="label">Made for smarter shopping.</p>
    </footer>
  );
}

export default Footer;