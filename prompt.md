Advanced Pomodoro Timer
HTML  •  CSS  •  JavaScript  • 

1. Context and Role
As a frontend developer working on a personal productivity tool, you are responsible for building a fully client-side Advanced Pomodoro Timer — a browser-based application with zero backend, zero frameworks, and zero external libraries. Everything runs in a single browser tab using pure HTML, CSS, and Vanilla JavaScript.

This is a personal project built to sharpen your core web development skills and create something genuinely useful for daily focused work. The app should feel polished, professional, and fast — the kind of tool you would actually use every day to manage your focus sessions and track your productivity over time.

2. Objective
Build a complete, production-ready Advanced Pomodoro Timer web application that:
●	Implements a precise, drift-corrected timer engine using setInterval and Date.now()
●	Supports three session modes — Work, Short Break, and Long Break — with automatic mode transitions
●	Includes a built-in task manager to link tasks to active timer sessions
●	Plays ambient sounds and session-end alerts using the Web Audio API
●	Renders a live productivity dashboard with Canvas-drawn charts
●	Persists all user data — settings, tasks, and session history — in localStorage with no server required
●	Works flawlessly on both mobile and desktop, with dark mode support

3. Technical Stack
Use only native browser technologies. No npm, no frameworks, no bundlers.

Layer	Technology	Purpose
Structure	HTML5	Semantic markup, Canvas element, audio tags
Styling	CSS3	Custom properties, Flexbox/Grid, animations, responsive design
Logic	Vanilla JavaScript (ES6+)	Timer engine, state management, localStorage
Audio	Web Audio API	Ambient sounds, tick SFX, session-end chime
Charts	Canvas API	Daily/weekly bar charts and ring charts
Storage	localStorage	Settings, task list, and session history — no backend
Deployment	GitHub Pages / Netlify	Static host — single HTML file or folder

4. UI and Visual Design Requirements
Timer Face
●	Large, clean countdown display in the center of the screen
●	Animated circular progress ring around the timer face using SVG or Canvas
●	Mode label clearly shown above the countdown (Work / Short Break / Long Break)
●	Active task name displayed below the countdown
●	Control buttons: Start, Pause, Resume, Reset — styled with smooth hover transitions

Settings Panel
●	Slide-in or modal panel with editable duration fields for all three session modes
●	Daily pomodoro target input
●	Auto-start toggle for breaks and work sessions
●	Notification permission request button
●	All values automatically saved to localStorage on change

Dashboard & Productivity Charts
●	Canvas-drawn bar chart showing daily pomodoro count for the last 7 days
●	Ring/donut chart showing today's progress toward the daily target
●	Three stat cards displaying: Total Focus Time, Current Streak, Best Day
●	Charts redraw automatically after each completed session

Dark Mode & Responsiveness
●	Manual dark/light mode toggle stored in localStorage
●	Automatic dark mode via prefers-color-scheme CSS media query
●	Fully responsive layout from 375px mobile to widescreen desktop
●	No horizontal scrolling at any screen size

General UI Standards
●	Rounded corners, soft shadows, and clean typography throughout
●	CSS custom properties (variables) for all colors and spacing — easy theming
●	Smooth CSS transitions on all interactive elements
●	Loading/active states visually communicated on buttons and controls

5. Core Features to Implement
Timer Engine
This is the heart of the application. Build it carefully.
●	setInterval-driven countdown that fires every 500ms for smooth UI updates
●	Drift correction using Date.now() delta — the timer must stay accurate even when the tab is backgrounded
●	Full control: Start, Pause, Resume, and Reset
●	Fires a session-complete event when countdown reaches zero

Session Modes
●	Work session: 25 minutes (default, user-configurable)
●	Short Break: 5 minutes (default, user-configurable)
●	Long Break: 15 minutes (default, user-configurable)
●	Auto-advance to the next mode when session ends
●	Long break automatically triggers after every 4 completed work sessions

Task Manager
●	Add, complete, and delete tasks from a visible task list
●	Each task tracks estimated pomodoros vs actual pomodoros completed
●	The currently selected task name is displayed on the timer face
●	Task list persisted in localStorage across page reloads

Ambient Sound Player
●	At least two ambient sound options built using Web Audio API oscillators (e.g., Rain, White Noise, Cafe, Forest)
●	Independent volume slider for ambient sounds
●	Sounds loop seamlessly and pause automatically when the timer is paused
●	No external audio files needed — all synthesized via Web Audio API

Session Alert System
●	Distinct chime synthesized via Web Audio API plays on session completion
●	Visual flash fallback if the tab is muted or audio is blocked
●	Browser Notification API integration for background tab alerts
●	Graceful permission request — never force, always ask politely

Keyboard Shortcuts
●	Space — Start / Pause the timer
●	R — Reset the current session
●	S — Open the settings panel
●	1 / 2 / 3 — Switch between Work, Short Break, and Long Break modes
●	M — Mute / unmute ambient sounds
●	? — Open a help overlay listing all keyboard shortcuts

CSV Export
●	Export the full session history as a .csv file
●	Each row includes: date, session mode, duration, and linked task name
●	Use Blob + URL.createObjectURL — no server or library required
●	Export button clearly visible in the dashboard section

6. Application Data Flow
Understanding the flow keeps the codebase clean and predictable:

1.	Page loads → reads localStorage for saved settings, tasks, and history → renders UI and charts
2.	User starts timer → TimerEngine fires setInterval every 500ms → UI updates every second via drift-corrected countdown
3.	Timer completes → plays chime, fires browser notification, auto-advances mode, logs the session
4.	Session logged → history array updated in memory, written to localStorage, charts redrawn
5.	User adds or completes a task → tasks array updated, active task displayed on timer face
6.	Export clicked → history serialized to a CSV string, Blob created, anchor click triggers file download

7. Recommended File Structure

File	Contents
index.html	Full app markup — timer face, settings panel, task list, dashboard
style.css	All styles: CSS variables, layout, animations, dark mode, responsive breakpoints
app.js	Entry point — imports and bootstraps all modules
timer.js	TimerEngine class — countdown logic, drift correction, events
settings.js	Settings read/write, localStorage persistence, form binding
tasks.js	Task CRUD, active task tracking, pomodoro count per task
audio.js	Web Audio API context, ambient oscillators, chime synthesis
charts.js	Canvas drawing — bar chart, ring chart, stat computations
export.js	CSV serialization, Blob download, history formatting
README.md	Setup guide, feature list, keyboard shortcuts, deploy steps

8. Output Requirements
The finished project must deliver all of the following:
●	Accurate, drift-corrected countdown timer with all three session modes working correctly
●	Automatic session mode transitions, including long break after 4 pomodoros
●	Fully functional settings panel with all values persisted to localStorage
●	Task manager with add, complete, delete, and estimated vs actual pomodoro tracking
●	At least two ambient sounds with volume control via Web Audio API
●	Session-end chime with visual flash fallback and browser notification support
●	Canvas productivity dashboard with 7-day bar chart, ring chart, and 3 stat cards
●	Manual dark mode toggle plus automatic system preference detection
●	All keyboard shortcuts working (Space, R, S, 1/2/3, M, ?)
●	CSV export of full session history using Blob + createObjectURL
●	Fully responsive layout from 375px mobile to desktop widescreen
●	README with setup, feature list, shortcuts, and deployment steps

9. Error Handling and Edge Cases
●	Handle Web Audio API context suspension (autoplay policy) — resume on user gesture
●	Gracefully handle localStorage quota errors — warn the user without crashing
●	Prevent timer from running negative values — clamp at zero and trigger completion
●	Handle browser notification permission denial — fall back to visual flash silently
●	Validate all settings inputs — reject non-numeric or out-of-range duration values
●	Handle CSV export in browsers that do not support createObjectURL — show a copy-paste fallback

10. Skills and Concepts Covered
This project is a comprehensive exercise in native browser development:

setInterval / clearInterval	Date.now() drift correction	Web Audio API
Canvas API	localStorage CRUD	CSS custom properties
ES6 Modules & Classes	Blob / File download	Responsive CSS Grid/Flex

11. Deployment
Since there is no backend, deployment is as simple as uploading static files:

Platform	Steps	Cost
GitHub Pages	Push to repo → Settings → Pages → Branch: main → Save. Live in ~60 seconds.	Free
Netlify	Drag and drop project folder into Netlify dashboard. Instant deploy.	Free
Any Static Host	Upload index.html and assets. No build step, no server config needed.	Free tier

12. Final Submission Checklist
Before calling the project complete, verify every item below:

✓	Timer engine — accurate countdown with Start / Pause / Resume / Reset
✓	All 3 session modes — Work, Short Break, Long Break with auto-advance
✓	Settings panel — custom durations, daily target, auto-start toggle — all persisted
✓	Task manager — Add, complete, delete tasks; active task shown on timer face
✓	Ambient sounds — at least 2 sounds via Web Audio API with volume control
✓	Productivity dashboard — Canvas bar chart (7-day) + ring chart + 3 stat cards
✓	Dark mode — manual toggle + respects system preference via media query
✓	Keyboard shortcuts — Space, R, S, 1/2/3, M, ? all working correctly
✓	CSV export — downloads a valid .csv of the full session history
✓	Responsive — works on mobile (375px) and desktop without horizontal scroll
✓	README — setup, features, shortcuts, and deployment instructions included
✓	Live URL — deployed and publicly accessible link ready to submit

Advanced Pomodoro Timer  ·  HTML · CSS · JavaScript  ·  No frameworks  ·  No backend  ·  Open source
