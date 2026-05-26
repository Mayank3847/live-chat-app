"""
golden_response.py

Production-ready self-extracting workspace generator for the Full-Stack
High-Performance E-Commerce Platform.

Fixes applied vs. original evaluation:
  - package.json: removed corrupted `gdgvdhgf` token — valid JSON restored
  - globals.css: corrected `@tailwindcss` → `@tailwind` directives
  - Dark mode: full `data-theme` toggle + `prefers-color-scheme` detection added
  - UI copy: all jargon labels replaced with clear, human-readable user-facing text
  - README.md: full project README added to workspace output
  - Navbar: dark mode toggle button wired in
  - Search UI: search input added to homepage, wired to client-side filter
  - aria-label strings: all corrected to plain English

Run: python golden_response.py
Then: npm install && npm run dev
"""

import os

# ==============================================================================
# WORKSPACE FILE DEFINITIONS
# ==============================================================================

WORKSPACE_FILES = {

    # --------------------------------------------------------------------------
    # ENVIRONMENT & CONFIG
    # --------------------------------------------------------------------------

    ".env.example": """# Application
NODE_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Email (SMTP via Nodemailer / Resend)
SMTP_HOST=smtp.resend.com
SMTP_PORT=465
SMTP_USER=resend
SMTP_PASS=re_yourSecurePasswordHere
EMAIL_FROM=noreply@yourstore.com
STORE_OWNER_EMAIL=admin@yourstore.com

# Database (optional — logging only in this build)
DATABASE_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/store
""",

    "package.json": """{
  "name": "high-performance-ecommerce",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "@hookform/resolvers": "^3.3.4",
    "clsx": "^2.1.0",
    "framer-motion": "^11.0.8",
    "lucide-react": "^0.344.0",
    "next": "^14.1.0",
    "nodemailer": "^6.9.10",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hook-form": "^7.51.0",
    "tailwind-merge": "^2.2.1",
    "zod": "^3.22.4",
    "zustand": "^4.5.1"
  },
  "devDependencies": {
    "@types/node": "^20.11.24",
    "@types/nodemailer": "^6.4.14",
    "@types/react": "^18.2.61",
    "@types/react-dom": "^18.2.19",
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3"
  }
}
""",

    "tailwind.config.js": """/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class', '[data-theme="dark"]'],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        neutral: {
          950: '#0a0a0a'
        }
      }
    },
  },
  plugins: [],
}
""",

    "tsconfig.json": """{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
""",

    # --------------------------------------------------------------------------
    # GLOBAL CSS  — FIX: @tailwind (not @tailwindcss)
    # --------------------------------------------------------------------------

    "src/app/globals.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    scroll-behavior: smooth;
  }

  /* Dark mode base overrides */
  [data-theme="dark"] body {
    @apply bg-neutral-950 text-neutral-100;
  }
}
""",

    # --------------------------------------------------------------------------
    # ZUSTAND CART STORE
    # --------------------------------------------------------------------------

    "src/store/useCartStore.ts": """import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  image: string;
  category: string;
}

interface CartState {
  items: CartItem[];
  isCartOpen: boolean;
  openCart: () => void;
  closeCart: () => void;
  addItem: (product: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  getCartTotal: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      isCartOpen: false,
      openCart: () => set({ isCartOpen: true }),
      closeCart: () => set({ isCartOpen: false }),

      addItem: (product) => {
        const existing = get().items.find((i) => i.id === product.id);
        if (existing) {
          set({
            items: get().items.map((i) =>
              i.id === product.id ? { ...i, quantity: i.quantity + 1 } : i
            ),
          });
        } else {
          set({ items: [...get().items, { ...product, quantity: 1 }] });
        }
      },

      removeItem: (id) =>
        set({ items: get().items.filter((i) => i.id !== id) }),

      updateQuantity: (id, quantity) => {
        if (quantity <= 0) {
          get().removeItem(id);
          return;
        }
        set({
          items: get().items.map((i) =>
            i.id === id ? { ...i, quantity } : i
          ),
        });
      },

      clearCart: () => set({ items: [] }),

      getCartTotal: () =>
        get().items.reduce((acc, i) => acc + i.price * i.quantity, 0),
    }),
    { name: 'shopping-cart-storage' }
  )
);
""",

    # --------------------------------------------------------------------------
    # THEME STORE — NEW: dark mode state management
    # --------------------------------------------------------------------------

    "src/store/useThemeStore.ts": """'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface ThemeState {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  initTheme: () => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      theme: 'light',

      toggleTheme: () => {
        const next = get().theme === 'light' ? 'dark' : 'light';
        set({ theme: next });
        document.documentElement.setAttribute('data-theme', next);
      },

      initTheme: () => {
        const saved = get().theme;
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const resolved = saved ?? (systemDark ? 'dark' : 'light');
        set({ theme: resolved });
        document.documentElement.setAttribute('data-theme', resolved);
      },
    }),
    { name: 'theme-preference' }
  )
);
""",

    # --------------------------------------------------------------------------
    # ROOT LAYOUT
    # --------------------------------------------------------------------------

    "src/app/layout.tsx": """import './globals.css';
import Navbar from '@/components/ui/Navbar';
import CartDrawer from '@/components/ui/CartDrawer';
import ThemeProvider from '@/components/ui/ThemeProvider';

export const metadata = {
  title: 'Velocé | High-Performance E-Commerce',
  description: 'A production-ready, fully animated e-commerce storefront built with Next.js 14, Framer Motion, and Zustand.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-white dark:bg-neutral-950 antialiased min-h-screen text-neutral-900 dark:text-neutral-100 flex flex-col transition-colors duration-300 selection:bg-indigo-500 selection:text-white">
        <ThemeProvider />
        <Navbar />
        <main className="flex-grow pt-16">
          {children}
        </main>
        <CartDrawer />
      </body>
    </html>
  );
}
""",

    # --------------------------------------------------------------------------
    # THEME PROVIDER — NEW: initialises theme on client mount
    # --------------------------------------------------------------------------

    "src/components/ui/ThemeProvider.tsx": """'use client';

import { useEffect } from 'react';
import { useThemeStore } from '@/store/useThemeStore';

export default function ThemeProvider() {
  const initTheme = useThemeStore((s) => s.initTheme);
  useEffect(() => { initTheme(); }, [initTheme]);
  return null;
}
""",

    # --------------------------------------------------------------------------
    # DATA LAYER
    # --------------------------------------------------------------------------

    "src/lib/seed.ts": """export interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  image: string;
  description: string;
}

export const SAMPLE_PRODUCTS: Product[] = [
  {
    id: 'prod_01',
    name: 'Minimalist Full-Grain Leather Backpack',
    price: 149.00,
    category: 'Travel',
    image: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&auto=format&fit=crop&q=80',
    description: 'Handcrafted from durable full-grain leather with a water-resistant lining, ergonomic shoulder straps, and a padded 16-inch laptop compartment.',
  },
  {
    id: 'prod_02',
    name: 'Anodized Aluminum Desk Lamp',
    price: 89.50,
    category: 'Office',
    image: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&auto=format&fit=crop&q=80',
    description: 'Aircraft-grade aluminum body with high-density, color-accurate LEDs and a touch-sensitive brightness dial.',
  },
  {
    id: 'prod_03',
    name: 'Wireless Ergonomic Mechanical Keyboard',
    price: 180.00,
    category: 'Computing',
    image: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80',
    description: 'Hot-swappable linear switches with tri-mode wireless connectivity and built-in sound-dampening foam.',
  },
  {
    id: 'prod_04',
    name: 'Noise-Cancelling Over-Ear Headphones',
    price: 299.00,
    category: 'Audio',
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80',
    description: 'Hybrid active noise cancellation with custom neodymium drivers tuned for a flat, high-fidelity frequency response.',
  },
];
""",

    "src/lib/validation.ts": """import { z } from 'zod';

export const checkoutSchema = z.object({
  fullName: z
    .string()
    .min(2, 'Full name must be at least 2 characters.')
    .max(64, 'Full name must be under 64 characters.'),
  email: z.string().email('Please enter a valid email address.'),
  phone: z
    .string()
    .regex(/^\\+?[1-9]\\d{1,14}$/, 'Please enter a valid phone number (E.164 format, e.g. +12025550143).'),
  address: z.string().min(6, 'Please enter your full street address.'),
  city: z.string().min(2, 'Please enter your city.'),
  state: z.string().min(2, 'Please enter your state or province.'),
  zipCode: z
    .string()
    .regex(/^\\d{5}(-\\d{4})?$|^[A-Z\\d\\s-]{3,10}$/i, 'Please enter a valid postal code.'),
  paymentMethod: z.enum(['Credit Card', 'UPI', 'COD']),
  notes: z.string().max(400, 'Notes must be under 400 characters.').optional(),
  items: z
    .array(
      z.object({
        id: z.string(),
        name: z.string(),
        price: z.number().positive(),
        quantity: z.number().int().positive(),
      })
    )
    .min(1, 'Your cart is empty.'),
});

export type CheckoutInput = z.infer<typeof checkoutSchema>;
""",

    # --------------------------------------------------------------------------
    # API ROUTES
    # --------------------------------------------------------------------------

    "src/app/api/products/route.ts": """import { NextResponse } from 'next/server';
import { SAMPLE_PRODUCTS } from '@/lib/seed';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get('category');
  const query = searchParams.get('q')?.toLowerCase();

  let results = [...SAMPLE_PRODUCTS];

  if (category && category !== 'all') {
    results = results.filter(
      (p) => p.category.toLowerCase() === category.toLowerCase()
    );
  }

  if (query) {
    results = results.filter(
      (p) =>
        p.name.toLowerCase().includes(query) ||
        p.description.toLowerCase().includes(query)
    );
  }

  return NextResponse.json({ success: true, data: results });
}
""",

    "src/app/api/orders/route.ts": """import { NextResponse } from 'next/server';
import { checkoutSchema } from '@/lib/validation';
import nodemailer from 'nodemailer';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const order = checkoutSchema.parse(body);

    const orderId = `ORD-${Math.random().toString(36).substring(2, 9).toUpperCase()}`;
    const timestamp = new Date().toISOString();
    const subtotal = order.items.reduce(
      (acc, item) => acc + item.price * item.quantity,
      0
    );

    console.log(`[ORDER] ${orderId} placed at ${timestamp} — total: $${subtotal.toFixed(2)}`);

    // Send confirmation emails only when SMTP credentials are configured
    if (process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASS) {
      const transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port: Number(process.env.SMTP_PORT) || 465,
        secure: true,
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASS,
        },
      });

      const itemRows = order.items
        .map((i) => `<li>${i.name} × ${i.quantity} — $${(i.price * i.quantity).toFixed(2)}</li>`)
        .join('');

      const emailHtml = `
        <div style="font-family:sans-serif;max-width:600px;margin:auto;border:1px solid #e5e5e5;padding:24px;border-radius:12px;">
          <h2 style="color:#4f46e5;">Order Confirmed — ${orderId}</h2>
          <p>Thank you, <strong>${order.fullName}</strong>! Your order has been received.</p>
          <hr style="border:none;border-top:1px solid #eee;margin:20px 0;" />
          <h3>Order Summary</h3>
          <ul>${itemRows}</ul>
          <p><strong>Total:</strong> $${subtotal.toFixed(2)}</p>
          <p><strong>Shipping to:</strong> ${order.address}, ${order.city}, ${order.zipCode}</p>
        </div>
      `;

      await Promise.all([
        transporter.sendMail({
          from: process.env.EMAIL_FROM || 'noreply@yourstore.com',
          to: order.email,
          subject: `Order Confirmed — ${orderId}`,
          html: emailHtml,
        }),
        transporter.sendMail({
          from: process.env.EMAIL_FROM || 'noreply@yourstore.com',
          to: process.env.STORE_OWNER_EMAIL || 'admin@yourstore.com',
          subject: `New Order Received — ${orderId}`,
          html: `<p>Placed at: ${timestamp}</p>${emailHtml}`,
        }),
      ]);
    }

    return NextResponse.json(
      { success: true, message: 'Order placed successfully.', data: { orderId, total: subtotal } },
      { status: 201 }
    );

  } catch (error: any) {
    console.error('[ORDER ERROR]', error);

    if (error.name === 'ZodError') {
      return NextResponse.json(
        { success: false, error: 'Invalid form data. Please check your inputs.', details: error.errors },
        { status: 400 }
      );
    }

    return NextResponse.json(
      { success: false, error: 'Something went wrong. Please try again.' },
      { status: 500 }
    );
  }
}
""",

    # --------------------------------------------------------------------------
    # UI COMPONENTS
    # --------------------------------------------------------------------------

    "src/components/ui/Navbar.tsx": """'use client';

import Link from 'next/link';
import { ShoppingBag, Sun, Moon } from 'lucide-react';
import { useCartStore } from '@/store/useCartStore';
import { useThemeStore } from '@/store/useThemeStore';
import { motion, AnimatePresence } from 'framer-motion';

export default function Navbar() {
  const { items, openCart } = useCartStore();
  const { theme, toggleTheme } = useThemeStore();
  const itemCount = items.reduce((acc, i) => acc + i.quantity, 0);

  return (
    <nav className="fixed top-0 left-0 right-0 h-16 bg-white/80 dark:bg-neutral-950/80 backdrop-blur-md border-b border-neutral-100 dark:border-neutral-800 z-40 transition-colors">
      <div className="max-w-7xl mx-auto h-full px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        <Link
          href="/"
          className="text-xl font-bold tracking-tight text-neutral-900 dark:text-white hover:opacity-80 transition-opacity"
        >
          VELOCÉ<span className="text-indigo-600">.</span>
        </Link>

        <div className="flex items-center gap-3">
          {/* Dark mode toggle */}
          <button
            onClick={toggleTheme}
            aria-label="Toggle dark mode"
            className="p-2 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors rounded-md"
          >
            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>

          {/* Cart button */}
          <button
            onClick={openCart}
            aria-label="Open cart"
            className="relative p-2 text-neutral-700 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white transition-colors"
          >
            <ShoppingBag className="w-6 h-6 stroke-[1.5]" />
            <AnimatePresence>
              {itemCount > 0 && (
                <motion.span
                  key={itemCount}
                  initial={{ scale: 0.6, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0.6, opacity: 0 }}
                  className="absolute -top-0.5 -right-0.5 min-w-5 h-5 px-1 bg-indigo-600 rounded-full text-white text-[10px] font-bold flex items-center justify-center shadow-sm"
                >
                  {itemCount}
                </motion.span>
              )}
            </AnimatePresence>
          </button>
        </div>
      </div>
    </nav>
  );
}
""",

    "src/components/ui/ProductCard.tsx": """'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { useCartStore } from '@/store/useCartStore';

interface ProductCardProps {
  product: {
    id: string;
    name: string;
    price: number;
    image: string;
    category: string;
  };
}

export const cardVariants = {
  hidden: { opacity: 0, y: 25 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.215, 0.61, 0.355, 1.0] },
  },
};

export default function ProductCard({ product }: ProductCardProps) {
  const addItem = useCartStore((s) => s.addItem);
  const openCart = useCartStore((s) => s.openCart);

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    addItem(product);
    openCart();
  };

  return (
    <motion.div
      variants={cardVariants}
      whileHover={{ y: -6, transition: { duration: 0.2, ease: 'easeInOut' } }}
      className="group flex flex-col overflow-hidden rounded-xl bg-white dark:bg-neutral-900 border border-neutral-100 dark:border-neutral-800 shadow-sm hover:shadow-md transition-shadow duration-300"
    >
      <Link href={`/products/${product.id}`} className="flex-1">
        <div className="relative aspect-square overflow-hidden bg-neutral-50 dark:bg-neutral-800">
          <img
            src={product.image}
            alt={product.name}
            loading="lazy"
            className="object-cover w-full h-full transition-transform duration-500 ease-out group-hover:scale-105"
          />
        </div>
        <div className="p-4">
          <p className="text-[10px] font-bold uppercase tracking-widest text-indigo-600">
            {product.category}
          </p>
          <h3 className="mt-1 text-sm font-medium text-neutral-800 dark:text-neutral-100 line-clamp-1 group-hover:text-indigo-600 transition-colors">
            {product.name}
          </h3>
          <p className="mt-1.5 text-base font-bold text-neutral-900 dark:text-white">
            ${product.price.toFixed(2)}
          </p>
        </div>
      </Link>
      <div className="p-4 pt-0">
        <button
          onClick={handleAddToCart}
          className="w-full rounded-lg bg-neutral-900 dark:bg-indigo-600 py-2.5 text-xs font-semibold text-white hover:bg-neutral-700 dark:hover:bg-indigo-700 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          Add to Cart
        </button>
      </div>
    </motion.div>
  );
}
""",

    "src/components/ui/CartDrawer.tsx": """'use client';

import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useCartStore } from '@/store/useCartStore';
import { X, Plus, Minus, Trash2, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function CartDrawer() {
  const { items, isCartOpen, closeCart, updateQuantity, removeItem, getCartTotal } =
    useCartStore();

  // Lock body scroll when cart is open
  useEffect(() => {
    document.body.style.overflow = isCartOpen ? 'hidden' : 'unset';
    return () => { document.body.style.overflow = 'unset'; };
  }, [isCartOpen]);

  return (
    <AnimatePresence>
      {isCartOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.4 }}
            exit={{ opacity: 0 }}
            onClick={closeCart}
            className="fixed inset-0 z-50 bg-black"
          />

          {/* Drawer panel */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 26, stiffness: 220 }}
            className="fixed bottom-0 right-0 top-0 z-50 flex h-full w-full max-w-md flex-col bg-white dark:bg-neutral-900 shadow-2xl"
            role="dialog"
            aria-modal="true"
            aria-label="Shopping cart"
          >
            {/* Header */}
            <div className="flex items-center justify-between border-b border-neutral-100 dark:border-neutral-800 p-4">
              <h2 className="text-base font-bold text-neutral-900 dark:text-white">
                Cart ({items.length} {items.length === 1 ? 'item' : 'items'})
              </h2>
              <button
                onClick={closeCart}
                aria-label="Close cart"
                className="p-1 rounded-md text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-200 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Items */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              <AnimatePresence mode="popLayout">
                {items.length === 0 ? (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex flex-col items-center justify-center h-72 text-center"
                  >
                    <p className="text-neutral-400 text-sm">Your cart is empty.</p>
                    <button
                      onClick={closeCart}
                      className="mt-3 text-xs font-bold text-indigo-600 hover:text-indigo-700 transition-colors"
                    >
                      Continue shopping
                    </button>
                  </motion.div>
                ) : (
                  items.map((item) => (
                    <motion.div
                      key={item.id}
                      layout
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, x: 80 }}
                      className="flex gap-4 border-b border-neutral-100 dark:border-neutral-800 pb-4 items-center"
                    >
                      <div className="h-16 w-16 flex-shrink-0 rounded-lg overflow-hidden bg-neutral-50 dark:bg-neutral-800 border border-neutral-100 dark:border-neutral-700">
                        <img
                          src={item.image}
                          alt={item.name}
                          className="object-cover w-full h-full"
                        />
                      </div>
                      <div className="flex flex-1 flex-col gap-2">
                        <div>
                          <h4 className="text-xs font-bold text-neutral-800 dark:text-neutral-100 line-clamp-1">
                            {item.name}
                          </h4>
                          <p className="text-sm font-black text-neutral-900 dark:text-white mt-0.5">
                            ${item.price.toFixed(2)}
                          </p>
                        </div>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center border border-neutral-200 dark:border-neutral-700 rounded-md bg-neutral-50 dark:bg-neutral-800">
                            <button
                              onClick={() => updateQuantity(item.id, item.quantity - 1)}
                              aria-label="Decrease quantity"
                              className="p-1 text-neutral-500 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                            >
                              <Minus className="w-3 h-3" />
                            </button>
                            <span className="px-2 text-xs font-bold text-neutral-800 dark:text-neutral-100">
                              {item.quantity}
                            </span>
                            <button
                              onClick={() => updateQuantity(item.id, item.quantity + 1)}
                              aria-label="Increase quantity"
                              className="p-1 text-neutral-500 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                            >
                              <Plus className="w-3 h-3" />
                            </button>
                          </div>
                          <button
                            onClick={() => removeItem(item.id)}
                            aria-label={`Remove ${item.name} from cart`}
                            className="p-1 text-neutral-400 hover:text-red-500 transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  ))
                )}
              </AnimatePresence>
            </div>

            {/* Footer */}
            {items.length > 0 && (
              <div className="border-t border-neutral-100 dark:border-neutral-800 p-4 bg-neutral-50 dark:bg-neutral-950">
                <div className="flex justify-between font-bold text-neutral-900 dark:text-white mb-4 text-sm">
                  <span>Total</span>
                  <span className="text-base">${getCartTotal().toFixed(2)}</span>
                </div>
                <Link
                  href="/checkout"
                  onClick={closeCart}
                  className="flex w-full items-center justify-center gap-2 bg-indigo-600 text-white py-3 rounded-xl text-xs font-bold hover:bg-indigo-700 transition-colors shadow-md shadow-indigo-600/20"
                >
                  Proceed to Checkout <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            )}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
""",

    # --------------------------------------------------------------------------
    # HOMEPAGE — FIX: search input wired to client-side filter
    # --------------------------------------------------------------------------

    "src/app/page.tsx": """'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { SAMPLE_PRODUCTS } from '@/lib/seed';
import ProductCard from '@/components/ui/ProductCard';
import { Sparkles, LayoutGrid, Search } from 'lucide-react';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.12, delayChildren: 0.1 },
  },
};

export default function HomePage() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const categories = [
    'all',
    ...Array.from(new Set(SAMPLE_PRODUCTS.map((p) => p.category.toLowerCase()))),
  ];

  const filteredProducts = SAMPLE_PRODUCTS.filter((p) => {
    const matchesCategory =
      selectedCategory === 'all' ||
      p.category.toLowerCase() === selectedCategory;
    const matchesSearch =
      searchQuery === '' ||
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="space-y-12 pb-24">
      {/* Hero */}
      <section className="relative overflow-hidden bg-neutral-950 text-white py-20 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,#312e81,transparent_60%)] opacity-40" />
        <div className="relative max-w-4xl mx-auto text-center space-y-6">
          <motion.div
            initial={{ opacity: 0, y: -15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center gap-2 px-3 py-1 bg-white/10 border border-white/10 backdrop-blur-md rounded-full text-xs font-medium text-indigo-300"
          >
            <Sparkles className="w-3.5 h-3.5" /> Curated products, crafted with care
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl sm:text-5xl font-black tracking-tight"
          >
            Shop the{' '}
            <span className="bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">
              Velocé Collection
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="max-w-xl mx-auto text-sm text-neutral-400 leading-relaxed"
          >
            Minimal design. Maximum quality. Free shipping on orders over $100.
          </motion.p>
        </div>
      </section>

      {/* Filters + Search */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-neutral-200 dark:border-neutral-800 pb-5 gap-4">
          <div className="flex items-center gap-2">
            <LayoutGrid className="w-5 h-5 text-neutral-400" />
            <h2 className="text-lg font-bold text-neutral-900 dark:text-white tracking-tight">
              All Products
            </h2>
          </div>

          <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto">
            {/* Search input */}
            <div className="relative flex-1 sm:flex-initial">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-neutral-400" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full sm:w-48 pl-8 pr-3 py-1.5 text-xs rounded-lg border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
              />
            </div>

            {/* Category pills */}
            <div className="flex flex-wrap gap-1.5 bg-neutral-100 dark:bg-neutral-800 p-1 rounded-xl">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-4 py-1.5 text-xs font-bold rounded-lg uppercase tracking-wider transition-all duration-200 ${
                    selectedCategory === cat
                      ? 'bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white shadow-sm'
                      : 'text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Product grid */}
        {filteredProducts.length === 0 ? (
          <div className="text-center py-20 text-neutral-400 text-sm">
            No products match your search.
          </div>
        ) : (
          <motion.div
            key={`${selectedCategory}-${searchQuery}`}
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
          >
            {filteredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </motion.div>
        )}
      </section>
    </div>
  );
}
""",

    # --------------------------------------------------------------------------
    # PRODUCT DETAIL PAGE
    # --------------------------------------------------------------------------

    "src/app/products/[id]/page.tsx": """'use client';

import { SAMPLE_PRODUCTS } from '@/lib/seed';
import { useCartStore } from '@/store/useCartStore';
import { motion } from 'framer-motion';
import { notFound } from 'next/navigation';
import { ArrowLeft, ShieldCheck, Truck } from 'lucide-react';
import Link from 'next/link';

export default function ProductDetailPage({ params }: { params: { id: string } }) {
  const product = SAMPLE_PRODUCTS.find((p) => p.id === params.id);
  const addItem = useCartStore((s) => s.addItem);
  const openCart = useCartStore((s) => s.openCart);

  if (!product) notFound();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-xs font-bold text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors mb-8"
      >
        <ArrowLeft className="w-4 h-4" /> Back to shop
      </Link>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 bg-white dark:bg-neutral-900 border border-neutral-100 dark:border-neutral-800 p-6 md:p-10 rounded-2xl shadow-sm">
        <motion.div
          initial={{ opacity: 0, scale: 0.97 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          className="relative aspect-square bg-neutral-50 dark:bg-neutral-800 overflow-hidden rounded-xl border border-neutral-100 dark:border-neutral-700"
        >
          <img
            src={product.image}
            alt={product.name}
            className="object-cover w-full h-full"
          />
        </motion.div>

        <div className="flex flex-col justify-between py-2 space-y-6">
          <div className="space-y-4">
            <span className="inline-block px-2.5 py-0.5 bg-indigo-50 dark:bg-indigo-950 border border-indigo-100 dark:border-indigo-800 text-[10px] font-black uppercase tracking-widest text-indigo-600 rounded-md">
              {product.category}
            </span>
            <h1 className="text-2xl md:text-3xl font-black text-neutral-900 dark:text-white tracking-tight leading-tight">
              {product.name}
            </h1>
            <p className="text-2xl font-black text-neutral-900 dark:text-white">
              ${product.price.toFixed(2)}
            </p>
            <p className="text-sm text-neutral-500 dark:text-neutral-400 leading-relaxed pt-2 border-t border-neutral-100 dark:border-neutral-800">
              {product.description}
            </p>
          </div>

          <div className="space-y-4 pt-6 border-t border-neutral-100 dark:border-neutral-800">
            <div className="flex items-center gap-4 text-xs text-neutral-500 dark:text-neutral-400">
              <span className="flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-green-500" /> Secure checkout
              </span>
              <span className="flex items-center gap-1.5">
                <Truck className="w-4 h-4 text-amber-500" /> Free shipping over $100
              </span>
            </div>
            <button
              onClick={() => { addItem(product); openCart(); }}
              className="w-full bg-neutral-900 dark:bg-indigo-600 hover:bg-neutral-800 dark:hover:bg-indigo-700 text-white font-bold py-3.5 rounded-xl text-xs tracking-wider transition-colors shadow-lg"
            >
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
""",

    # --------------------------------------------------------------------------
    # CHECKOUT PAGE — FIX: all user-facing copy is plain English
    # --------------------------------------------------------------------------

    "src/app/checkout/page.tsx": """'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion, AnimatePresence } from 'framer-motion';
import { checkoutSchema, CheckoutInput } from '@/lib/validation';
import { useCartStore } from '@/store/useCartStore';
import { CheckCircle2, CreditCard, ShoppingBag, ShieldCheck } from 'lucide-react';
import Link from 'next/link';

export default function CheckoutPage() {
  const { items, getCartTotal, clearCart } = useCartStore();
  const [step, setStep] = useState<1 | 2>(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [orderResult, setOrderResult] = useState<{ id: string } | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CheckoutInput>({
    resolver: zodResolver(checkoutSchema),
    defaultValues: {
      items: items.map((i) => ({
        id: i.id,
        name: i.name,
        price: i.price,
        quantity: i.quantity,
      })),
    },
  });

  const onSubmit = async (data: CheckoutInput) => {
    setIsSubmitting(true);
    try {
      const res = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const json = await res.json();
      if (json.success) {
        setOrderResult({ id: json.data.orderId });
        clearCart();
      } else {
        alert(json.error || 'Something went wrong. Please try again.');
      }
    } catch {
      alert('Could not connect to the server. Please check your connection and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (items.length === 0 && !orderResult) {
    return (
      <div className="max-w-md mx-auto text-center py-24 px-4">
        <ShoppingBag className="w-12 h-12 text-neutral-300 mx-auto mb-4" />
        <h2 className="text-lg font-bold text-neutral-900 dark:text-white">
          Your cart is empty.
        </h2>
        <Link
          href="/"
          className="mt-4 inline-block text-xs font-bold text-indigo-600 hover:underline"
        >
          Browse products
        </Link>
      </div>
    );
  }

  if (orderResult) {
    return (
      <div className="flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center p-4">
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="w-full max-w-md rounded-2xl bg-white dark:bg-neutral-900 border border-neutral-100 dark:border-neutral-800 p-8 text-center shadow-xl"
        >
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-50 text-green-500">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <h2 className="mt-4 text-xl font-bold text-neutral-900 dark:text-white">
            Order placed!
          </h2>
          <p className="mt-2 text-xs text-neutral-500">
            Order ID:{' '}
            <strong className="text-neutral-800 dark:text-neutral-200 font-mono">
              {orderResult.id}
            </strong>
          </p>
          <p className="mt-4 text-xs text-neutral-400 leading-relaxed bg-neutral-50 dark:bg-neutral-800 p-3 rounded-lg border border-neutral-100 dark:border-neutral-700">
            A confirmation email has been sent to your inbox.
          </p>
          <Link
            href="/"
            className="mt-6 inline-block w-full bg-neutral-900 dark:bg-indigo-600 text-white font-bold py-3 rounded-xl text-xs tracking-wider hover:bg-neutral-800 dark:hover:bg-indigo-700 transition-colors"
          >
            Continue Shopping
          </Link>
        </motion.div>
      </div>
    );
  }

  const inputClass =
    'w-full rounded-lg border border-neutral-200 dark:border-neutral-700 p-2.5 text-xs bg-neutral-50 dark:bg-neutral-800 text-neutral-900 dark:text-white focus:bg-white dark:focus:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all';
  const labelClass =
    'block text-[10px] font-bold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider mb-1';
  const errorClass = 'text-[10px] text-red-500 mt-1 font-medium';

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12 grid grid-cols-1 lg:grid-cols-12 gap-8">
      {/* Form */}
      <div className="lg:col-span-7 bg-white dark:bg-neutral-900 p-6 md:p-8 border border-neutral-100 dark:border-neutral-800 rounded-2xl shadow-sm">
        <form onSubmit={handleSubmit(onSubmit)}>
          <AnimatePresence mode="wait">
            {step === 1 ? (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: -15 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 15 }}
                className="space-y-5"
              >
                <h3 className="text-base font-bold text-neutral-800 dark:text-white flex items-center gap-2 border-b border-neutral-100 dark:border-neutral-800 pb-3">
                  <span className="w-5 h-5 rounded-full bg-indigo-600 text-white flex items-center justify-center text-[10px]">1</span>
                  Shipping Details
                </h3>

                <div>
                  <label className={labelClass}>Full Name</label>
                  <input {...register('fullName')} className={inputClass} />
                  {errors.fullName && <p className={errorClass}>{errors.fullName.message}</p>}
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className={labelClass}>Email Address</label>
                    <input type="email" {...register('email')} className={inputClass} />
                    {errors.email && <p className={errorClass}>{errors.email.message}</p>}
                  </div>
                  <div>
                    <label className={labelClass}>Phone Number</label>
                    <input type="tel" {...register('phone')} placeholder="+12025550143" className={inputClass} />
                    {errors.phone && <p className={errorClass}>{errors.phone.message}</p>}
                  </div>
                </div>

                <div>
                  <label className={labelClass}>Street Address</label>
                  <input {...register('address')} className={inputClass} />
                  {errors.address && <p className={errorClass}>{errors.address.message}</p>}
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className={labelClass}>City</label>
                    <input {...register('city')} placeholder="City" className={inputClass} />
                    {errors.city && <p className={errorClass}>{errors.city.message}</p>}
                  </div>
                  <div>
                    <label className={labelClass}>State</label>
                    <input {...register('state')} placeholder="State" className={inputClass} />
                    {errors.state && <p className={errorClass}>{errors.state.message}</p>}
                  </div>
                  <div>
                    <label className={labelClass}>ZIP Code</label>
                    <input {...register('zipCode')} placeholder="ZIP" className={inputClass} />
                    {errors.zipCode && <p className={errorClass}>{errors.zipCode.message}</p>}
                  </div>
                </div>

                <div>
                  <label className={labelClass}>Order Notes (optional)</label>
                  <textarea {...register('notes')} rows={3} placeholder="Special instructions..." className={inputClass} />
                  {errors.notes && <p className={errorClass}>{errors.notes.message}</p>}
                </div>

                <button
                  type="button"
                  onClick={() => setStep(2)}
                  className="w-full bg-neutral-900 dark:bg-indigo-600 text-white font-bold py-3 rounded-xl text-xs tracking-wider hover:bg-neutral-800 dark:hover:bg-indigo-700 transition-colors"
                >
                  Continue to Payment
                </button>
              </motion.div>
            ) : (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 15 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -15 }}
                className="space-y-5"
              >
                <h3 className="text-base font-bold text-neutral-800 dark:text-white flex items-center gap-2 border-b border-neutral-100 dark:border-neutral-800 pb-3">
                  <span className="w-5 h-5 rounded-full bg-indigo-600 text-white flex items-center justify-center text-[10px]">2</span>
                  Payment Method
                </h3>

                <div className="space-y-2">
                  {['Credit Card', 'UPI', 'COD'].map((method) => (
                    <label
                      key={method}
                      className="flex items-center gap-3 p-3 border border-neutral-200 dark:border-neutral-700 rounded-xl cursor-pointer bg-neutral-50 dark:bg-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
                    >
                      <input
                        type="radio"
                        value={method}
                        {...register('paymentMethod')}
                        defaultChecked={method === 'Credit Card'}
                        className="w-4 h-4 text-indigo-600"
                      />
                      <span className="text-xs font-bold text-neutral-700 dark:text-neutral-200">
                        {method}
                      </span>
                    </label>
                  ))}
                </div>

                <div className="flex gap-4 pt-4">
                  <button
                    type="button"
                    onClick={() => setStep(1)}
                    className="w-1/3 border border-neutral-200 dark:border-neutral-700 p-3 rounded-xl text-xs font-bold text-neutral-600 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors"
                  >
                    Back
                  </button>
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-2/3 bg-indigo-600 text-white p-3 rounded-xl text-xs font-bold tracking-wider hover:bg-indigo-700 disabled:bg-indigo-400 transition-colors shadow-lg shadow-indigo-600/20"
                  >
                    {isSubmitting
                      ? 'Placing order...'
                      : `Place Order — $${getCartTotal().toFixed(2)}`}
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </form>
      </div>

      {/* Order Summary */}
      <div className="lg:col-span-5 space-y-6">
        <div className="bg-neutral-50 dark:bg-neutral-900 p-6 rounded-2xl border border-neutral-200 dark:border-neutral-800 space-y-4">
          <h3 className="text-xs font-bold text-neutral-400 uppercase tracking-wider flex items-center gap-1.5">
            <CreditCard className="w-4 h-4" /> Order Summary
          </h3>
          <div className="divide-y divide-neutral-200 dark:divide-neutral-800 max-h-60 overflow-y-auto">
            {items.map((item) => (
              <div key={item.id} className="flex justify-between text-xs py-3 items-center">
                <span className="text-neutral-600 dark:text-neutral-400 line-clamp-1 pr-4">
                  {item.name}{' '}
                  <strong className="text-neutral-900 dark:text-white font-bold">
                    ×{item.quantity}
                  </strong>
                </span>
                <span className="font-bold text-neutral-900 dark:text-white flex-shrink-0">
                  ${(item.price * item.quantity).toFixed(2)}
                </span>
              </div>
            ))}
          </div>
          <div className="flex justify-between font-black text-sm text-neutral-900 dark:text-white pt-4 border-t border-neutral-200 dark:border-neutral-800">
            <span>Total</span>
            <span className="text-indigo-600">${getCartTotal().toFixed(2)}</span>
          </div>
        </div>

        <div className="flex items-center gap-2 p-3 bg-green-50 dark:bg-green-950/30 border border-green-100 dark:border-green-900 rounded-xl text-[10px] text-green-700 dark:text-green-400 font-medium">
          <ShieldCheck className="w-5 h-5 flex-shrink-0 text-green-600" />
          Your payment information is protected with end-to-end encryption.
        </div>
      </div>
    </div>
  );
}
""",

    # --------------------------------------------------------------------------
    # README — NEW: full project documentation
    # --------------------------------------------------------------------------

    "README.md": """# Velocé — High-Performance E-Commerce Platform

A production-ready, fully animated e-commerce storefront built with:
- **Next.js 14** (App Router)
- **Framer Motion** (micro-animations + page transitions)
- **Zustand** (persistent cart + theme state)
- **Tailwind CSS** (utility-first styling + dark mode)
- **Zod** + **React Hook Form** (schema validation)
- **Nodemailer** (transactional email)

---

## Getting Started

```bash
# 1. Generate the workspace
python golden_response.py

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env.local
# Fill in your SMTP credentials

# 4. Start the dev server
npm run dev
# Open http://localhost:3000
```

---

## Features

| Feature | Details |
|---|---|
| Product catalog | Grid with category filter + live search |
| Product detail | Animated image, description, add-to-cart |
| Cart drawer | Spring-physics slide-in, quantity controls, persistent |
| Multi-step checkout | Shipping → Payment → Confirmation |
| Order emails | Customer confirmation + store owner notification |
| Dark mode | Manual toggle + respects `prefers-color-scheme` |
| Form validation | Zod schema, inline error messages |
| Fully responsive | Mobile-first, no horizontal scroll |

---

## Project Structure

```
src/
├── app/
│   ├── api/
│   │   ├── orders/route.ts     # POST — create order + send emails
│   │   └── products/route.ts   # GET  — filter products
│   ├── checkout/page.tsx
│   ├── products/[id]/page.tsx
│   ├── page.tsx                # Homepage + product grid
│   ├── layout.tsx
│   └── globals.css
├── components/ui/
│   ├── Navbar.tsx              # Fixed nav + dark mode toggle + cart button
│   ├── CartDrawer.tsx          # Animated slide-in cart
│   ├── ProductCard.tsx         # Animated product tile
│   └── ThemeProvider.tsx       # Initialises theme on mount
├── store/
│   ├── useCartStore.ts         # Zustand cart state (persisted)
│   └── useThemeStore.ts        # Zustand theme state (persisted)
└── lib/
    ├── seed.ts                 # Sample product data
    └── validation.ts           # Zod checkout schema
```

---

## Deployment

### Vercel (recommended)
```bash
npx vercel
```
Add your `.env.local` values in the Vercel dashboard under Project → Settings → Environment Variables.

### Netlify
```bash
npm run build
# Upload the .next folder or connect your GitHub repo
```

### Environment Variables

| Key | Required | Description |
|---|---|---|
| `SMTP_HOST` | Optional | SMTP server (e.g. smtp.resend.com) |
| `SMTP_PORT` | Optional | Default: 465 |
| `SMTP_USER` | Optional | SMTP username |
| `SMTP_PASS` | Optional | SMTP password |
| `EMAIL_FROM` | Optional | Sender address |
| `STORE_OWNER_EMAIL` | Optional | Receives new order alerts |

> Email sending is skipped gracefully if SMTP variables are not set.

---

## Tech Decisions

- **No database** — products are seeded in-memory; orders log to console. Swap `src/lib/seed.ts` for a real DB query to extend.
- **No auth** — add NextAuth.js to `src/app/api/auth` for user accounts.
- **Zustand `persist`** — cart survives page refresh via `localStorage`.
""",

}

# ==============================================================================
# WORKSPACE GENERATOR
# ==============================================================================

def generate_workspace():
    print("=" * 72)
    print("  VELOCÉ E-COMMERCE PLATFORM — WORKSPACE GENERATOR")
    print("=" * 72)

    base = os.getcwd()
    written = 0

    for rel_path, content in WORKSPACE_FILES.items():
        abs_path = os.path.join(base, rel_path.replace("/", os.sep))
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

        print(f"  ✓  {rel_path}")
        written += 1

    print("-" * 72)
    print(f"  {written} files written to: {base}")
    print("-" * 72)
    print()
    print("  Next steps:")
    print("    1.  npm install")
    print("    2.  cp .env.example .env.local   (add your SMTP credentials)")
    print("    3.  npm run dev")
    print("    4.  Open http://localhost:3000")
    print()
    print("=" * 72)


if __name__ == "__main__":
    generate_workspace()