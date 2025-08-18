export type Quality =
  | 'exotic' | 'currency' | 'gear' | 'material'
  | 'weapon' | 'unique' | 'cosmetic'
  | 'consumable' | 'pet' | 'other';

export interface Item {
  id: number;
  name: string;
  price: number;
  image?: string | null;
  quantity?: number | null;
  quality?: Quality | null;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
}