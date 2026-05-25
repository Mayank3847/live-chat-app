<div align="center">

# 💬 TARS — Live Chat App

### A real-time one-on-one messaging application built for speed, reliability, and a polished user experience.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20App-brightgreen?style=for-the-badge&logo=vercel)](https://tars-chat-app-xi.vercel.app/sign-in)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/Mayank3847/live-chat-app)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-Strict-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org)
[![Convex](https://img.shields.io/badge/Convex-Realtime-orange?style=for-the-badge)](https://convex.dev)
[![Clerk](https://img.shields.io/badge/Clerk-Auth-purple?style=for-the-badge)](https://clerk.com)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38bdf8?style=for-the-badge&logo=tailwindcss)](https://tailwindcss.com)

</div>

---

## 🌐 Live Application

> **Try it now →** [https://tars-chat-app-xi.vercel.app/sign-in](https://tars-chat-app-xi.vercel.app/sign-in)

Sign up with your email or a social account and start messaging other users instantly — no setup required.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Folder Structure](#-folder-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running Locally](#-running-locally)
- [Deployment](#-deployment)
- [Architecture Decisions](#-architecture-decisions)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧭 Overview

**TARS** is a production-grade real-time chat application that lets users sign up, discover other registered users, and exchange messages instantly. Every part of the stack — authentication, database, real-time subscriptions, and UI — is designed to feel fast and reliable under real usage conditions.

The project is built on the **Next.js App Router** with **Convex** as the reactive backend and **Clerk** handling all authentication flows. Messages, presence, and typing indicators update live across all connected clients without polling or page refreshes.

---

## ✨ Features

### Core
- 🔐 **Authentication** — Email and social login/logout via Clerk. Session persists across tabs and refreshes.
- 👥 **User Discovery** — Browse all registered users (excluding yourself) with a live search filter.
- 💬 **One-on-One Messaging** — Real-time private conversations powered by Convex subscriptions.
- 🕐 **Smart Timestamps** — Messages show time only for today, date + time for this year, full date for older messages.
- 📭 **Empty States** — Friendly, helpful messages in every empty scenario — no blank screens ever.

### Advanced
- 🟢 **Online / Offline Presence** — Green indicator for users currently in the app. Updates in real time.
- ✍️ **Typing Indicator** — Shows "[Name] is typing…" with a pulsing animation. Auto-disappears after 2 seconds of inactivity or on message send.
- 🔴 **Unread Badge** — Per-conversation unread count in the sidebar. Clears instantly when the conversation is opened.
- ⬇️ **Smart Auto-Scroll** — Auto-scrolls to the latest message when at the bottom. If you've scrolled up, shows a "↓ New messages" button instead.
- 📱 **Fully Responsive** — Desktop shows sidebar + chat side by side. Mobile shows conversation list by default; tapping opens full-screen chat with a back button.

### Quality
- ♿ **Accessible** — Semantic HTML, ARIA labels, keyboard-navigable throughout.
- 🛡️ **Input Sanitisation** — User inputs are sanitised before storage to prevent XSS.
- ⚡ **Debounced Events** — Typing indicator events are debounced to avoid flooding the Convex backend.
- 🚨 **Graceful Error Handling** — Mutation failures show actionable UI messages ("Failed to send — Retry"), never raw errors.

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Framework | Next.js 15 (App Router) | Full-stack React framework |
| Language | TypeScript (strict) | Type safety throughout |
| Styling | Tailwind CSS + shadcn/ui | Utility-first UI components |
| Backend & DB | Convex | Real-time database + serverless functions |
| Authentication | Clerk | Sign up, login, session management |
| Deployment | Vercel | Frontend hosting + CI/CD |
| Package Manager | npm | Dependency management |

---

## 📁 Folder Structure

```
live-chat-app/
│
├── app/                          # Next.js App Router
│   ├── (auth)/                   # Clerk sign-in / sign-up pages
│   │   ├── sign-in/[[...sign-in]]/page.tsx
│   │   └── sign-up/[[...sign-up]]/page.tsx
│   ├── (chat)/                   # Protected chat routes
│   │   ├── layout.tsx            # Sidebar + main layout wrapper
│   │   ├── page.tsx              # "Select a conversation" empty state
│   │   └── [id]/
│   │       └── page.tsx          # Individual conversation view
│   ├── layout.tsx                # Root layout — Clerk + Convex providers
│   └── globals.css               # Global Tailwind styles
│
├── components/
│   ├── chat/
│   │   ├── MessageList.tsx       # Scrollable message thread
│   │   ├── MessageInput.tsx      # Debounced input with send button
│   │   ├── MessageBubble.tsx     # Single message with timestamp
│   │   └── TypingIndicator.tsx   # Pulsing dots animation
│   ├── sidebar/
│   │   ├── ConversationList.tsx  # List of active conversations
│   │   ├── ConversationItem.tsx  # Single conversation with preview + badge
│   │   └── UserSearch.tsx        # Search panel for new conversations
│   └── ui/                       # shadcn/ui base components
│
├── convex/                       # Convex backend (runs on Convex cloud)
│   ├── schema.ts                 # Database schema — all tables + indexes
│   ├── users.ts                  # User creation, sync, listing
│   ├── conversations.ts          # Create/fetch conversations
│   ├── messages.ts               # Send, fetch, mark as read
│   └── presence.ts               # Online status + typing indicators
│
├── lib/
│   ├── utils.ts                  # cn() helper + timestamp formatting
│   └── debounce.ts               # Reusable debounce utility
│
├── public/                       # Static assets
│
├── middleware.ts                 # Clerk route protection
├── next.config.ts                # Next.js configuration
├── tailwind.config.ts            # Tailwind configuration
├── tsconfig.json                 # TypeScript configuration
├── components.json               # shadcn/ui configuration
└── .env.local                    # Environment variables (never committed)
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Node.js** v18 or higher — [Download](https://nodejs.org)
- **npm** v9 or higher (comes with Node.js)
- A **Convex** account — [Sign up free](https://convex.dev)
- A **Clerk** account — [Sign up free](https://clerk.com)

---

## 🔑 Environment Variables

Create a `.env.local` file in the root of the project. **Never commit this file.**

```env
# ─── Convex ────────────────────────────────────────────────
# Get this from: https://dashboard.convex.dev → your project → Settings
NEXT_PUBLIC_CONVEX_URL=https://your-project-name.convex.cloud

# ─── Clerk ─────────────────────────────────────────────────
# Get these from: https://dashboard.clerk.com → your app → API Keys
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxx
CLERK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxx

# ─── Clerk Redirect URLs (optional but recommended) ────────
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/
```

> **Where to find your keys:**
> - **Convex URL** → [dashboard.convex.dev](https://dashboard.convex.dev) → Select your project → Settings → Deployment URL
> - **Clerk keys** → [dashboard.clerk.com](https://dashboard.clerk.com) → Select your app → API Keys

---

## 💻 Running Locally

**Step 1 — Clone the repository**

```bash
git clone https://github.com/Mayank3847/live-chat-app.git
cd live-chat-app
```

**Step 2 — Install dependencies**

```bash
npm install
```

**Step 3 — Set up environment variables**

Copy the template above into a new `.env.local` file and fill in your actual keys.

**Step 4 — Start the Convex backend**

Open a terminal and run:

```bash
npx convex dev
```

This will:
- Prompt you to log into your Convex account
- Create a new Convex project (first time only)
- Sync your schema and functions to the cloud
- Watch for changes and hot-reload the backend

**Step 5 — Start the Next.js dev server**

Open a second terminal and run:

```bash
npm run dev
```

**Step 6 — Open the app**

Visit [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🌍 Deployment

### Deploy to Vercel + Convex Cloud

**Step 1 — Push your code to GitHub**

```bash
git add .
git commit -m "ready for deployment"
git push origin main
```

**Step 2 — Deploy Convex to production**

```bash
npx convex deploy
```

This pushes your schema and backend functions to Convex's production environment and gives you a production deployment URL.

**Step 3 — Deploy frontend to Vercel**

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository (`Mayank3847/live-chat-app`)
3. Vercel will auto-detect Next.js — no build config needed
4. Under **Environment Variables**, add all the keys from your `.env.local`:
   - `NEXT_PUBLIC_CONVEX_URL` — use the **production** URL from `npx convex deploy`
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
   - `CLERK_SECRET_KEY`
   - `NEXT_PUBLIC_CLERK_SIGN_IN_URL` → `/sign-in`
   - `NEXT_PUBLIC_CLERK_SIGN_UP_URL` → `/sign-up`
   - `NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL` → `/`
   - `NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL` → `/`
5. Click **Deploy**

**Step 4 — Add your Vercel URL to Clerk**

1. Go to [dashboard.clerk.com](https://dashboard.clerk.com)
2. Select your app → **Domains**
3. Add your Vercel production URL (e.g. `https://tars-chat-app-xi.vercel.app`)

Your app is now live. Every `git push` to `main` will trigger an automatic Vercel redeploy.

---

## 🏗 Architecture Decisions

**Why Convex?**
Convex replaces a traditional REST API + database setup with reactive queries that push updates to all subscribed clients the moment data changes. This means real-time messaging, presence, and typing indicators work without WebSocket management, polling, or manual cache invalidation.

**Why a separate `presence` table?**
Keeping online status and typing events in a dedicated `presence` table prevents high-frequency writes from triggering re-renders on every component that subscribes to user data. The `users` table stays stable; the `presence` table handles the noise.

**Why `lastMessageId` on conversations?**
Denormalizing the last message ID onto the conversation record means the sidebar can render message previews without joining across the full `messages` table — a single read per conversation instead of a scan.

**Why Clerk?**
Clerk handles the full auth lifecycle — email verification, social OAuth, session tokens, and JWTs — without requiring any custom auth code. The `ConvexProviderWithClerk` integration means every Convex function automatically has access to the verified user identity.

**Why debounce typing events?**
Without debouncing, every keystroke would write to the Convex database. With a 300ms debounce, the backend receives at most a few writes per second per user — making typing indicators scalable even with many concurrent conversations.

---

## 📸 Screenshots

| Sign In | Conversation List | Live Chat |
|---|---|---|
| Clerk-powered sign in with email or social | Sidebar with unread badges and message previews | Real-time messages with timestamps and typing indicator |

---

## 🤝 Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch — `git checkout -b feature/your-feature-name`
3. Commit your changes — `git commit -m "feat: add your feature"`
4. Push to your fork — `git push origin feature/your-feature-name`
5. Open a Pull Request

Please make sure all TypeScript types are correct and no `any` types are introduced.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ by [Mayank3847](https://github.com/Mayank3847)

⭐ If you found this useful, consider starring the repo!

[![GitHub stars](https://img.shields.io/github/stars/Mayank3847/live-chat-app?style=social)](https://github.com/Mayank3847/live-chat-app)

</div>