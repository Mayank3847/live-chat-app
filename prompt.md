Prompt
You are a senior full-stack engineer with 2+ years of production experience in Next.js, TypeScript, real-time systems, and cloud-native architectures. You have deep expertise in Convex, Clerk authentication, and building scalable chat applications. You write clean, maintainable, fully typed code that is ready for production deployment. In this article, I will provide you with an running project prompt. I want you to do before writing a single line of code: 1. Force yourself to read through the whole prompt and before even thinking about starting any work, write down a list of all features you will implement from top priority (core → advanced → optional). 2. Design the Convex database schema first — define all tables, fields, types, and indexes — and explain your design decisions before proceeding. 3. Plan the full folder structure of the Next.js App Router project and present it clearly. 4. After this, add the project implementation feature by feature in exactly that order: Authentication → User List & Search → One-on-One Messaging→ Timestamps → Empty States Responsive Layout Online/Offline Status Typing Indicator Unread Badge Smart Auto-Scroll 5. When you create a file, write the full file — no stubs, no "// add logic here" comments and don't put incomplete sections. Every file must be production-ready. 6. After each major feature, briefly explain what you built and why you made each architectural decision. 7.At the end, provide the complete README with setup instructions, environment variable configuration, and Vercel deployment steps. Additional hard rules you must follow throughout: * Use TypeScript strictly — no any types, no type assertions unless absolutely necessary with a comment explaining why. * Every Convex query and mutation must be properly typed using v validators. * All components must be React functional components using hooks — no class components. * Handle every loading state and error state explicitly in the UI — never leave the user staring at a blank screen. * Use Tailwind CSS utility classes only — no inline styles unless dynamically computed. Mobile-first responsive design using Tailwind breakpoints. * Debounce all typing indicator events to avoid flooding the Convex backend. * Never hardcode API keys or secrets — use environment variables throughout. * Write self-documenting code — variable and function names should make intent obvious without needing comments everywhere. i also attached the word docs of the prompt.
Context and Role
As a Full-Stack Developer specialising in modern real-time web applications, you are responsible for designing and implementing a high-performance personal live chat messaging web application. The app must enable users to sign up, discover other users, and message them in real time — all with a clean, polished interface. The design of the system is smiley face'd for scalability, type safety and user experience like a clean production ready personal project. The app needs real time data sync, logging in/out users via authentication and reactive view updates. It should show how the experience is conversational, simple to chat with someone without agent assistance but feel instant (like real-time), and consistent in guiding users through a seamless sign-up process until messaging happens.
Objective
Develop a complete full-stack live chat application that:
●	Implements real-time messaging using Convex subscriptions for instant updates on both sides of a conversation.
●	Provides a modern, responsive UI with smooth transitions and thoughtful empty/loading states.
●	Includes user authentication (sign up, login, logout) via Clerk with social and email options.
●	Supports one-on-one direct messaging with a sidebar showing all active conversations.
●	Displays online/offline presence indicators and typing indicators in real time.
●	Tracks and displays unread message counts, clearing them when a conversation is opened.
●	Implements smart auto-scroll — auto-scrolling to the latest message while preserving manual scroll position.
●	Logs all backend interactions securely and handles errors gracefully with structured responses.
UI and Feature Requirements
Authentication
Set up Clerk so that:
●	Users can sign up via email or social login, log in, and log out.
●	The logged-in user's name and avatar are displayed throughout the UI.
●	User profiles are stored in Convex so that other users can discover them.
User List & Search
●	Show all registered users, excluding the currently logged-in user.
●	Include a search bar that filters users by name as the user types.
●	Clicking a user opens an existing conversation or creates a new one.
One-on-One Direct Messages
●	Users can have private conversations with any other registered user.
●	Messages appear in real time for both participants using Convex subscriptions.
●	A sidebar lists all conversations with a preview of the most recent message.
Message Timestamps
Show when each message was sent, formatted as follows:
●	Today's messages: time only (e.g. 2:34 PM).
●	Older messages: date and time (e.g. Feb 15, 2:34 PM).
●	Messages from a previous year: full date including year.
Empty States
Show helpful, friendly messages in all empty scenarios — never leave a blank screen:
●	No conversations started yet.
●	No messages in an open conversation.
●	No search results found.
Layout Requirements
The application must include:
●	A sidebar listing all active conversations with message previews and unread badges.
●	A main chat area with message history, timestamps, and a message input field.
●	A user search/discovery panel for initiating new conversations.
The layout must be:
●	Fully responsive — Desktop: sidebar + chat area side by side. Mobile: conversation list as default, tapping a conversation opens full-screen chat with a back button.
●	Accessible — ARIA labels, semantic HTML, keyboard-navigable elements.
●	Optimised for performance — minimal re-renders, efficient subscriptions.
Real-Time System Requirements
Online/Offline Status
●	Show a green indicator next to users who currently have the app open.
●	Update presence state in real time when users come online or go offline.
Typing Indicator
●	Show "[Name] is typing..." or a pulsing dots animation when the other user is actively typing.
●	Disappear automatically after approximately 2 seconds of inactivity or when the message is sent.
Unread Message Count
●	Show a badge on each conversation in the sidebar displaying the number of unread messages.
●	Clear the badge automatically when the user opens that conversation.
●	Update badge counts in real time as new messages arrive.
Smart Auto-Scroll
●	Scroll automatically to the latest message when new messages arrive.
●	If the user has manually scrolled up to read older messages, do not force-scroll — instead show a "↓ New messages" button that the user can tap to jump to the bottom.
Backend Requirements
●	Implement Convex mutations and queries to handle all data operations: user creation, message sending, conversation management, presence tracking, and typing events.
●	Securely store all user profiles and messages in Convex tables with a clean, extensible schema.
●	Use Convex real-time subscriptions (useQuery) for all data that needs to stay live.
●	Store all sensitive configuration (Clerk keys, Convex deployment URL) securely using environment variables — never hardcode credentials.
●	Apply basic rate limiting or debouncing on client-side interactions to prevent spamming events.
Data Processing Requirements
●	Sanitise all user inputs to prevent XSS and injection attacks.
●	Validate email formats on the client side with proper error messaging.
●	Ensure all Convex functions return structured, predictable responses.
●	Handle errors in mutations gracefully and surface them to the user without crashing the UI.
Output Requirements
●	A fully functional real-time chat application deployed on Vercel.
●	Clerk-based authentication that persists across sessions.
●	Instant message delivery and UI updates via Convex subscriptions.
●	Responsive layout that works seamlessly on mobile and desktop.
●	Graceful error handling when messages fail to send, with retry options.
●	Confirmation or visual feedback after all user actions.
Error Handling and Documentation
●	Handle all frontend interaction errors gracefully — never show raw error messages to users.
●	Handle Convex mutation failures and display actionable error states (e.g. "Failed to send — Retry").
●	Log backend failures appropriately within Convex function logs.
●	Document the following clearly in the project README:
○	Folder structure
○	Setup and installation instructions
○	Environment variable configuration (Clerk, Convex)
○	Deployment steps (Vercel + Convex cloud)
Performance and Scalability
●	Optimise bundle size — code-split heavy components and lazy-load where appropriate.
●	Ensure all real-time subscriptions are efficient and do not cause unnecessary re-renders.
●	Use proper debouncing for typing indicator events to avoid flooding the database.
●	Support concurrent users without causing API bottlenecks in Convex.
●	Ensure accessibility — ARIA labels, semantic HTML, keyboard navigation.
●	Apply SEO best practices for the publicly accessible pages.
Technology Stack
Use the following:
Frontend:
●	Next.js (App Router)
●	TypeScript
●	Tailwind CSS — optionally paired with shadcn/ui, Radix UI, or Headless UI
Backend:
●	Convex — backend, database, and real-time subscriptions
●	Clerk — authentication and user management
●	dotenv — environment variable configuration
Optional:
●	Extended features: message reactions, soft-delete, group chat, skeleton loaders, and message retry UI.
