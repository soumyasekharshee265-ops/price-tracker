const POINTS = [
  { number: '01', title: 'Why we exist', desc: "Because finding the best price shouldn't require opening 12 browser tabs." },
  { number: '02', title: 'What we do', desc: "We pull prices from multiple sites and tell you, straight up, whether it's a good time to buy." },
  { number: '03', title: "What's next", desc: 'More sites, smarter alerts, and a lot more deals worth chasing.' },
];

function AboutSection() {
  return (
    <section id="about" className="about-section">
      <div className="about-pitch">
        <span className="label">MEET YOUR DEAL SCOUT</span>
        <h2>"Hey, I'm your deal scout."</h2>
        <p>I fly around the site keeping an eye on prices, so you don't have to. Ask me anything below.</p>
      </div>

      <div className="about-points">
        {POINTS.map((point) => (
          <div key={point.number} className="about-point">
            <span className="label about-point-number">{point.number}</span>
            <div>
              <h3>{point.title}</h3>
              <p>{point.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default AboutSection;