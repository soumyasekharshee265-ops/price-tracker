import { useEffect, useState } from 'react';
import { API_BASE_URL } from '../config';

function IdeasSection() {
  const [ideas, setIdeas] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/suggestions?limit=30`)
      .then((res) => res.json())
      .then((data) => setIdeas(data.suggestions || []))
      .catch(() => setIdeas([]));
  }, []);

  if (ideas.length === 0) return null;

  const row = [...ideas, ...ideas];

  return (
    <section className="ideas-section">
      <h2 className="ideas-section-title">Ideas from our users</h2>

      <div className="ideas-row ideas-row-ltr">
        <div className="ideas-track">
          {row.map((idea, i) => (
            <div className="idea-card" key={`ltr-${idea.id}-${i}`}>
              <p className="idea-text">"{idea.suggestion}"</p>
              <span className="idea-name">— {idea.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="ideas-row ideas-row-rtl">
        <div className="ideas-track">
          {row.map((idea, i) => (
            <div className="idea-card" key={`rtl-${idea.id}-${i}`}>
              <p className="idea-text">"{idea.suggestion}"</p>
              <span className="idea-name">— {idea.name}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default IdeasSection;