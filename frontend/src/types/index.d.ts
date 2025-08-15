import type { LucideIcon } from 'lucide-vue-next';

export interface NavItem {
    title: string;
    href: string;
    icon?: LucideIcon;
    isActive?: boolean;
}

export interface Product {
  id: number
  title: string
  price:number
  description: string
  image_url: string
  quantity?:number
}

export interface CartItem extends Product {
  quantity: number
}

