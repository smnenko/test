export interface Product {
  id: string;
  name: string;
  category: 'gaming' | 'entertainment' | 'crypto' | 'payment';
  price: number;
  currency: string;
  description: string | null;
  image_url: string | null;
  is_available: boolean;
}

export interface GiftCard {
  id: string;
  code: string;
  product_id: string;
  initial_balance: number;
  balance: number;
  currency: string;
  status: 'active' | 'redeemed' | 'expired' | 'blocked';
  expires_at: string | null;
}

// Кандидат может расширять типы по необходимости
