import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ComparisonResults from './pages/ComparisonResults';
import DealsPage from './pages/DealsPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/compare" element={<ComparisonResults />} />
        <Route path="/deals" element={<DealsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;