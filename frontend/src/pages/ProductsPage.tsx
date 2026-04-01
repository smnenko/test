import { useState, useEffect, ChangeEvent } from "react";
import axios from "axios";
import { ProductsCard } from "../components/ProductCard";
import { useSearchParams } from "react-router-dom";
import { InputText } from "../components/InputText";
import { API_URL } from "../constants/api";
import { Product } from "src/types";

const CATEGORIES = ["gaming", "entertainment", "crypto", "payment"];
const LIMIT = 4

const ProductsPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [offset, setOffset] = useState(0);

  const handleSearchChange = (e: ChangeEvent<HTMLInputElement>) => {
    setSearchParams((prevParams) => {
      e.target.value === ""
        ? searchParams.delete("search")
        : prevParams.set("search", e.target.value);
      return prevParams;
    });
  };

  const handleCategoryChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setSearchParams((prevParams) => {
      e.target.value === "all"
        ? searchParams.delete("category")
        : prevParams.set("category", e.target.value);
      return prevParams;
    });
  };

  useEffect(() => {
    setLoading(true);
    let url = `${API_URL}/api/products?limit=${LIMIT}&offset=${offset}&${searchParams.toString()}`;
    axios.get(url).then((res) => {
      setProducts(res.data.items);
      setLoading(false);
    });
  }, [searchParams, offset]);

  return (
    <div>
      <h1 style={{ marginBottom: 20 }}>Каталог товаров</h1>

      <div style={{ marginBottom: 16, display: "flex", gap: 8 }}>
        <InputText
          placeholder="Поиск..."
          value={searchParams.get("search") ?? ""}
          onChange={handleSearchChange}
        />
        <select
          value={searchParams.get("category") ?? ""}
          onChange={handleCategoryChange}
          style={{
            padding: "8px 12px",
            border: "1px solid #ddd",
            borderRadius: 4,
          }}
        >
          <option value="all">Все категории</option>
          {CATEGORIES.map((cat) => (
            <option value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <p>Загрузка...</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(16rem, 1fr))",
            gap: 16,
          }}
        >
          {products.map((product) => (
            <ProductsCard key={product.id} product={product} />
          ))}
        </div>
      )}

      <div style={{display: "flex", gap: 4, marginTop: 16, justifyContent: "center"}}>
        <button disabled={!(offset >= LIMIT)} style={{
          fontSize: "16px",
          background: offset >= LIMIT ? "var(--color-primary)" : "grey",
          color: "white",
          padding: " 0.7em 1em",
          paddingLeft: " 0.9em",
          borderRadius: "16px",
          border: "none",
          cursor: "pointer",
          maxWidth: "20rem",
        }} onClick={() => setOffset(offset - LIMIT)}>Предыдущая</button>

        <div style={{
            fontSize: "16px",
            padding: " 0.7em 1em",
            paddingLeft: " 0.9em",
            borderRadius: "16px",
            border: "none",
            cursor: "pointer",
            maxWidth: "20rem",
          }}>
          Страница: {offset / LIMIT + 1}
        </div>

        <button disabled={!(products.length === LIMIT)} style={{
          fontSize: "16px",
          background: products.length === LIMIT ? "var(--color-primary)" : "grey",
          color: "white",
          padding: " 0.7em 1em",
          paddingLeft: " 0.9em",
          borderRadius: "16px",
          border: "none",
          cursor: "pointer",
          maxWidth: "20rem",
        }} onClick={() => setOffset(offset + LIMIT)}>Следующая</button>
      </div>
    </div>
  );
};

export default ProductsPage;
