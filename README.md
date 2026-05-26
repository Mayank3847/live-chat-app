# 🍅 Advanced Pomodoro Timer

A production-ready Pomodoro productivity application built using **HTML5 + CSS3 + Vanilla JavaScript**.

No frameworks. No backend. No external libraries.

Everything runs entirely in the browser.

---

# ✨ Features

## Timer System
- Drift-corrected countdown using `Date.now()`
- `setInterval(500ms)` timer updates
- Start / Pause / Resume / Reset controls
- Automatic session transitions
- Long break after every 4 completed work sessions
- Circular animated progress ring

---

## Session Modes

### Work Session
Default: 25 minutes

### Short Break
Default: 5 minutes

### Long Break
Default: 15 minutes

All durations are editable.

---

## Task Manager

- Add tasks
- Complete tasks
- Delete tasks
- Active task selection
- Estimated Pomodoros tracking
- Actual Pomodoros tracking
- Timer linked with active task
- Persistent task storage

---

## Audio System

Built entirely using Web Audio API.

Ambient Sounds:
- Rain
- White Noise

Features:
- Volume control
- Mute toggle
- Auto pause/resume
- Session completion chime
- Audio context recovery

---

## Notifications

- Browser Notification API
- Background session alerts
- Graceful permission request
- Visual flash fallback

---

## Analytics Dashboard

Canvas-based analytics.

Includes:

### Productivity Bar Chart
- Last 7 days focus sessions

### Donut Progress Chart
- Daily target completion

### Statistics
- Total Focus Time
- Current Streak
- Best Day

---

## Settings

Editable:

- Work duration
- Short break duration
- Long break duration
- Daily target
- Auto-start work
- Auto-start breaks

All values persist automatically.

---

## Export

CSV Export supported.

Includes:

- Date
- Session Mode
- Duration
- Linked Task

Uses:
- Blob
- URL.createObjectURL()

Fallback:
- Manual CSV copy

---

## Theme Support

### Manual
- Light Mode
- Dark Mode

### Automatic
- Respects system preference

---

## Keyboard Shortcuts

| Key | Action |
|------|--------|
| Space | Start / Pause |
| R | Reset |
| S | Open Settings |
| 1 | Work Mode |
| 2 | Short Break |
| 3 | Long Break |
| M | Mute Audio |
| ? | Open Help |
| ESC | Close Overlay |

---

# 📂 Project Structure

```plaintext
advanced-pomodoro/
│
├── index.html
├── style.css
├── app.js
├── timer.js
├── settings.js
├── tasks.js
├── audio.js
├── charts.js
├── export.js
├── storage.js
├── utils.js
├── help.js
│
├── assets/
│
└── README.md
```

---

# 🚀 Run Locally

Clone repository:

```bash
git clone <repository-url>
```

Open:

```plaintext
index.html
```

No installation.

No npm.

No build step.

---

# 🌍 Deployment

## GitHub Pages

### Step 1

Create repository.

### Step 2

Push project.

```bash
git init

git add .

git commit -m "Initial Commit"

git branch -M main

git remote add origin YOUR_REPO_URL

git push -u origin main
```

### Step 3

Open:

Settings → Pages

### Step 4

Select:

```plaintext
Deploy from Branch
```

Branch:

```plaintext
main
```

Folder:

```plaintext
/
```

### Step 5

Save.

Live in approximately 1 minute.

---

## Netlify

### Option 1

Drag and drop project folder.

### Option 2

Connect GitHub repository.

Publish directory:

```plaintext
/
```

Build command:

```plaintext
(empty)
```

---

# 💾 Data Storage

Uses:

```plaintext
localStorage
```

Stored:

- Settings
- Tasks
- Active Task
- Analytics
- Session History
- Theme

No external database.

No server.

---

# 📱 Responsive Support

Supported:

- Mobile (375px+)
- Tablet
- Laptop
- Desktop
- Wide screens

No horizontal scrolling.

---

# ♿ Accessibility

Includes:

- Keyboard navigation
- Focus states
- Responsive text
- Accessible buttons
- Contrast-friendly UI

---

# 🧪 Browser Support

Tested for:

- Chrome
- Edge
- Firefox
- Safari

---

# 🛡 Error Handling

Handled cases:

- Audio autoplay restrictions
- Notification denial
- Storage quota exceeded
- Invalid settings
- Negative timer prevention
- CSV export fallback

---

# 📈 Future Improvements

- Cloud sync
- Multi-device support
- Weekly reports
- Focus music presets
- PWA support
- Offline install
- Authentication

---

# ✅ Final Checklist

- Accurate Timer
- Three Session Modes
- Task Manager
- Audio Engine
- Notifications
- Analytics Dashboard
- CSV Export
- Dark Mode
- Keyboard Shortcuts
- Responsive Layout
- Deployment Ready

---

Built using:

HTML • CSS • JavaScript • Canvas • Web Audio API • localStorage