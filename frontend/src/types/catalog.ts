export interface Game { id: number; name: string; slug: string }
export interface Category { id: number; name: string; slug: string }
export interface Item {
  id: number; name: string; price: number; image?: string | null;
  // при необходимости: quality?: number; quantity?: number;
}
export interface ItemListResponse { items: Item[]; total: number }