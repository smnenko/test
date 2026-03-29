import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import ProductsPage from './pages/ProductsPage';
import RedeemPage from './pages/RedeemPage';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="header">
          <div className="header-content">
            <Link to="/" className="logo">
              Baxity
            </Link>
            <nav>
              <Link to="/">Каталог</Link>
              <Link to="/redeem" style={{ marginLeft: 16 }}>Гифт-карта</Link>
            </nav>
          </div>
        </header>
        <main className="main">
          <Routes>
            <Route path="/" element={<ProductsPage />} />
            <Route path="/redeem" element={<RedeemPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
