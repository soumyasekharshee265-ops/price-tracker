const STEPS = [
  { number: '01', title: 'Search', desc: 'Type a product name, or paste a product link directly.' },
  { number: '02', title: 'Compare', desc: 'We pull prices, ratings, and images from every site we can find it on.' },
  { number: '03', title: 'Get the Verdict', desc: 'Our AI checks the price history and tells you whether to buy now or wait.' },
  { number: '04', title: 'Choose', desc: 'Pick the best deal and head straight to the site to buy.' },
];

function HowItWorks() {
  return (
    <section id="how-it-works" className="how-it-works-section">
      <div className="features-heading">
        <span className="label">THE PROCESS</span>
        <h2>How It Works</h2>
      </div>

      <div className="timeline">
        <div className="timeline-line" />
        {STEPS.map((step) => (
          <div key={step.number} className="timeline-item">
            <div className="timeline-dot" />
            <div className="timeline-card">
              <span className="label timeline-number">{step.number}</span>
              <h3>{step.title}</h3>
              <p>{step.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default HowItWorks;