import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import StarBackground from '../components/StarBackground';
import SearchBar from '../components/SearchBar';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import Ticker from '../components/Ticker';
import DealsSection from '../components/DealsSection';
import AboutSection from '../components/AboutSection';
import Footer from '../components/Footer';
import BrandsSection from '../components/BrandsSection';
import ReviewsSection from '../components/ReviewsSection';

function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    document.title = 'Price Tracker — Compare. Discover. Save.';
  }, []);

  const handleSearch = (query) => {
    if (!query || !query.trim()) return;
    navigate(`/compare?q=${encodeURIComponent(query.trim())}`);
  };

  return (
    <>
      <StarBackground />
      <Navbar />
      <Hero />
      <Ticker />
       <div id="search-section" className="search-section" style={{ padding: '3rem 1.5rem 0' }}>
        <SearchBar onSearch={handleSearch} />
      </div>
            <DealsSection />
      <AboutSection />
      <ReviewsSection />
      <BrandsSection />
      <Footer />
    </>
  );
}

export default Home;