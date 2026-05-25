# SlateNotes: Architecture & Design Decisions

Full setup and architecture: [README.md](README.md).

## 1. How to Run

### Requirements
- Python 3.7 or newer
- pip (Python package manager)

### Install Once

```bash
git clone https://github.com/Maryam-Sikander/Quill-notes
cd Quill-notes
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

Then open your browser to http://127.0.0.1:5000

---

## 2. Stack Choice


### Why Flask + SQLite

| Reason | Benefit |
|--------|---------|
| **Minimal dependencies** | Only Flask required; no ORM bloat |
| **Fast development** | Built-in routing and template rendering |
| **SQLite** | Zero-config database; perfect for personal projects |
| **Stateless design** | Easy to reset or modify the schema |


### Why Not...

| Technology | Why I Skipped It |
|------------|-----------------|
| Django | Overkill for a single-user notes app and too much boilerplate |
| React / Vue frontend | Server-side rendering with Flask templates is simpler here |
| PostgreSQL / MySQL | Requires external setup; SQLite works offline and persists locally |


### Tradeoffs

- **No offline sync**: Notes live only in `notes.db`, no cloud backup.
- **Server restart clears session**: No session store; fresh state on each app restart.

---

## 3. Edge Cases

# 3. Edge cases

These are the real edge cases that shaped the notes application and its behavior.


## A. Search Across Large Note Content

Users expect search to work naturally across both titles and note bodies. The search system checks both fields so partial phrases can still match relevant notes. This keeps the search flexible even when users do not remember exact wording.

---

## B. Pinned Notes Ordering

If multiple notes are pinned, their ordering becomes important. The app sorts pinned notes first and then orders them by most recently updated. This keeps frequently used notes naturally near the top without ordering.

---

## C. Persistence Between App Restarts
Notes are stored in SQLite so every create, update, and delete action remains available even after restarting the application or refreshing the browser.
---

## 4. AI Usage

I used **Cursor/Gemini** as a coding assistant while building Quill:

- **Where it helped**:
  1. Suggested UI improvements (glassmorphism orbs and dot-grid background alignment).
  2. Flagged the duplicate tags `IntegrityError` crash
  3. Accelerated boilerplate code and template generation.

- **What I did**:
  1. Designed the architecture, folder layout, database schema, and pipeline.
  2. Chose the stack and core design patterns (server-rendered HTML, local-first data).
  3. Reviewed all AI suggestions, removed generic solutions, and adapted code to fit the project vision.

**Bottom line**: Architecture, security decisions, and product choices are mine, AI just used to speed up implementation.

---

## 5. Honest Gaps

- **Multi-user support**: No user accounts or session management. Adding this would require auth middleware and per-user data isolation.
- **Concurrent edits**: If you open the same note in two browser tabs and edit both, the last save wins (classic CRUD behavior, no conflict resolution).
- **Performance at scale**: Search is O(n) on the table; a full-text index would help with 10,000+ notes.
- **Data recovery**: No trash bin or soft delete; deleted notes are permanently gone immediately.
- **Offline mode**: The app requires a running Flask server

---