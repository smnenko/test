import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const categories = ['gaming', 'entertainment', 'crypto', 'payment'];

const ProductsPage = () => {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');

  useEffect(() => {
    setLoading(true);
    let url = `${API_URL}/api/products?limit=50`;
    if (category) url += `&category=${category}`;
    if (search) url += `&search=${search}`;

    axios.get(url).then((res) => {
      setProducts(res.data.items);
      setLoading(false);
    });
  }, [category, search]);

  return (
    <div>
      <h1 style={{ marginBottom: 20 }}>Каталог товаров</h1>

      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        <input
          type="text"
          placeholder="Поиск..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ padding: '8px 12px', border: '1px solid #ddd', borderRadius: 4, fontSize: 14 }}
        />
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{ padding: '8px 12px', border: '1px solid #ddd', borderRadius: 4 }}
        >
          <option value="all">Все категории</option>
          {categories.map((cat) => (
            <option value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      {loading && <p>Загрузка...</p>}

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 16,
      }}>
        {products.map((product, index) => (
          <div
            key={index}
            style={{
              border: '1px solid #ddd',
              borderRadius: 8,
              padding: 16,
              backgroundColor: 'white',
            }}
          >
            <img
              src={product.image_url}
              style={{ width: '100%', height: 200, objectFit: 'cover', borderRadius: 4 }}
            />
            <h3 style={{ margin: '12px 0 4px' }}>{product.name}</h3>
            <p style={{ color: '#666', fontSize: 14, margin: 0 }}>{product.category}</p>
            <p style={{ fontWeight: 'bold', fontSize: 18, margin: '8px 0 0' }}>
              ${Number(product.price).toFixed(2)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductsPage;
