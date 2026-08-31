const BRANDS = [
  { name: 'Amazon', logo: '/logos/amazon.png' },
  { name: 'Flipkart', logo: '/logos/flipkart.png' },
  { name: 'Myntra', logo: '/logos/myntra.png' },
  { name: 'Croma', logo: '/logos/croma.png' },
  { name: 'Ajio', logo: '/logos/ajio.png' },
  { name: 'Meesho', logo: '/logos/meesho.png' },
  { name: 'Snapdeal', logo: '/logos/snapdeal.png' },
  { name: 'Nykaa', logo: '/logos/nykaa.png' },
  { name: 'Tata Cliq', logo: '/logos/tatacliq.png' },
  { name: 'Reliance Digital', logo: '/logos/reliancedigital.png' },
  { name: 'BigBasket', logo: '/logos/bigbasket.png' },
  { name: 'JioMart', logo: '/logos/jiomart.png' },
  { name: 'FirstCry', logo: '/logos/firstcry.png' },
  { name: 'Pepperfry', logo: '/logos/pepperfry.png' },
  { name: 'Lenskart', logo: '/logos/lenskart.png' },
  { name: 'Urban Ladder', logo: '/logos/urbanladder.png' },
  { name: 'HP', logo: '/logos/hp.png' },
  { name: 'Jockey', logo: '/logos/jockey.png' },
  { name: 'Manyavar', logo: '/logos/manyavar.png' },
  { name: 'Purplle', logo: '/logos/purplle.png' },
  { name: 'Samsung', logo: '/logos/samsung.png' },
  { name: 'Tira', logo: '/logos/tira.png' },
];

function BrandsSection() {
  const row = [...BRANDS, ...BRANDS];

  return (
    <section className="brands-section">
      <h2 className="brands-section-title">We compare prices across</h2>

      <div className="brands-row">
        <div className="brands-track">
          {row.map((brand, i) => (
            <div className="brand-logo-card" key={`${brand.name}-${i}`}>
              <img
                src={brand.logo}
                alt={brand.name}
                onError={(e) => {
                  e.currentTarget.closest('.brand-logo-card').style.display = 'none';
                }}
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default BrandsSection;