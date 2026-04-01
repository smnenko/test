import React from "react";
import { Product } from "../../types";

type ProductsCardProps = {
  product: Product;
};

const defaultGiftCardImgUrl =
  "https://placehold.co/400x300/a8b0b3/ffffff?text=Gift%20card";

export const ProductsCard: React.FC<ProductsCardProps> = ({ product }) => (
  <div
    style={{
      border: "1px solid #ddd",
      borderRadius: 8,
      padding: 16,
      backgroundColor: "white",
    }}
  >
    <img
      src={product.image_url ?? defaultGiftCardImgUrl}
      style={{
        width: "100%",
        height: 200,
        objectFit: "cover",
        borderRadius: 4,
      }}
      alt="No img"
    />
    <h3 style={{ margin: "12px 0 4px" }}>{product.name}</h3>
    <p style={{ color: "#666", fontSize: 14, margin: 0 }}>{product.category}</p>
    <p style={{ fontWeight: "bold", fontSize: 18, margin: "8px 0 0" }}>
      ${Number(product.price).toFixed(2)}
    </p>
  </div>
);
