# ANSWERS.md

## 1. How to Run

### Prerequisites
Make sure you have **Python 3.7+** installed.

### Run Steps
Run the following commands from the project root directory:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the Flask development server
python app.py
```

Then open your browser and navigate to **[http://localhost:5000](http://localhost:5000)**.

*Note: Data is saved to `notes.db` in the project root. Delete this file if you want to reset the application.*

---

## 2. Stack Choice

For this project, I chose **Python 3**, **Flask**, and **SQLite**:

- **Python & Flask**: Python has a batteries-included standard library. Flask is micro, fast to set up, has no boilerplates, and allows running a full CRUD application with a single external dependency (`flask`).
- **SQLite**: A serverless, file-based database. It requires zero configuration, zero service running in the background, and persists automatically into a single file (`notes.db`). This guarantees that when the reviewer runs the app on a fresh machine, the database works instantly without DB installations or user setup.
- **Vanilla CSS + JS**: Avoids heavy frontend frameworks (like React/Vite/Next.js) which require hundreds of megabytes of `node_modules` and slow down launch times with build/compilation steps.

### What would have been a worse choice and why?
A worse choice would be **Next.js (React) + PostgreSQL**:
- Next.js requires a Node.js runtime, installing a massive dependency tree (`node_modules`), and running a production build command.
- PostgreSQL requires the reviewer to have a PostgreSQL database service running locally, configure database credentials, set up schemas, and manage local ports.
- For a small, portable, persistent mini-app, this stack introduces significant friction for the reviewer on a fresh machine with no material benefit to the user experience.

---

## 3. One Real Edge Case

### XSS (Cross-Site Scripting) Prevention in Note Content
- **Location**: [templates/view.html](file:///E:/GitHub-clone/ppc-tool/notes-app/templates/view.html#L30)
- **Code**: `{{ note.content | e | replace('\n', '<br>') | safe }}`

#### What happens without this handling?
Previously, the code was: `{{ note.content | replace('\n', '<br>') | safe }}`.
Because it piped directly to the `safe` filter, if a user saved a note with HTML or JavaScript tags (e.g., `<script>alert('hack')</script>` or `<img src=x onerror=alert(1)>`), the browser would execute the script directly. This is a severe XSS security vulnerability that allows arbitrary code execution.
By adding the `e` (escape) filter *before* replacing newlines with `<br>`, we ensure all HTML-sensitive characters are escaped, and *then* safely inject `<br>` tags to preserve formatting.

### Duplicate Tags Integrity Error
- **Location**: [database.py](file:///E:/GitHub-clone/ppc-tool/notes-app/database.py#L178-L182)
- **Code**: Deduplicating tag inputs using a Python `set` in `_sync_tags` and utilizing `INSERT OR IGNORE` in the `note_tags` junction table.

#### What happens without this handling?
If a user created/edited a note and entered duplicate tags (like `work, Work` or `urgent, urgent`), the app would loop over them and execute database inserts. Because the `note_tags` junction table defines `PRIMARY KEY (note_id, tag_id)`, attempting to insert duplicate rows would throw a `sqlite3.IntegrityError` (causing a 500 Internal Server Error) and crash the request. Our logic handles tag case-insensitivity and filters duplicate tags in-memory.

---

## 4. AI Usage

I used **Antigravity (Gemini 3.5 Flash)** to assist with this project:

- **Where it was used**:
  1. To audit the codebase against the technical assessment guidelines.
  2. To identify UI improvements (the missing background glassmorphism orbs and `.dot-grid` CSS alignment).
  3. To identify the duplicate tags `IntegrityError` crash and the XSS vulnerability in `templates/view.html`.
- **What was asked**: "Please check which things are missing from the project and do it based on the technical assessment guidelines."
- **What it gave me**: It provided an implementation plan, modified the layout, corrected the database schema inserts, escaped template outputs, and prepared the README and ANSWERS templates.
- **What I changed and why**:
  - The AI initially suggested adding a heavy markdown library to render notes as markdown. I rejected this because the guidelines value simplicity and ease of run on a fresh machine. Adding external markdown libraries would increase dependencies, bundle sizes, and open up more XSS vectors. Instead, I had the AI refine the existing newline-to-br converter with correct escaping.
  - I also noticed that when notes were deleted, orphaned tags were left in the `tags` table since the cascade deletion only cleared the junction table. I added an explicit cleanup query to `delete_note` in `database.py` to keep the database tidy.

---

## 5. Honest Gap

### Concurrency and DB Locking
- **The Gap**: Currently, the SQLite connection is opened and closed on every query using raw `sqlite3` without connection pooling or WAL (Write-Ahead Logging) enabled. While fine for a single user, if multiple requests write to the database concurrently, SQLite will throw a `database is locked` error.
- **How to fix it**: With another day, I would use **SQLAlchemy** to manage a connection pool and enable WAL mode (`PRAGMA journal_mode=WAL;`), which allows concurrent reads and writes without locking. I would also add user-facing toast notifications/validations for blank note titles instead of standard page redirects.

---

## 6. Beyond CRUD Feature

### 📌 Note Pinning
- **Implementation**: The app allows users to toggle the "pinned" status of any note. Pinned notes are styled with a distinctive yellow border, a `📌` icon, and are anchored at the top of the grid regardless of their update timestamps or active search/tag filters.
- **Defense**: In a notes app, key information (like a todo list or a quick reference guide) is frequently accessed but easily gets buried under newer notes. Pinning solves this friction by letting users bookmark important items instantly. It provides immense utility with a clean, zero-friction interface.
