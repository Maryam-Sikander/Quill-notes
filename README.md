# SlateNotes 📝

SlateNotes is a beautiful, personal notes application designed with an Obsidian-inspired glassmorphism dark theme. Users can create, view, edit, and delete notes, each customizable with distinct color accents, titles, body content, and tags.

## Key Features

- **Full CRUD Support**: Create, Read, Update, and Delete notes.
- **Deduplicated Tagging**: Organise notes using tags. Tag filtering keeps your workspace clean, and orphan tags are cleaned up automatically.
- **Note Pinning (Beyond CRUD)**: Pin important notes to keep them anchored at the top of your list.
- **Search bar**: Find notes instantly by title or content.
- **Security-First rendering**: Note content is fully HTML-escaped to prevent Cross-Site Scripting (XSS) injection.
- **Polished Visuals**: Vibrant floating backdrop orbs, Obsidian-style dot-grid background, smooth transitions, and card entrance micro-animations.

---

## Getting Started

### Prerequisites

Make sure you have **Python 3.7+** installed on your system.

### How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Application**:
   ```bash
   python app.py
   ```

3. **Open the App**:
   Navigate to [http://localhost:5000](http://localhost:5000) in your web browser.

---

## Data Persistence

SlateNotes stores all note data in a local SQLite file named `notes.db` located at the root of the project.
- **Persistence**: Data survives application restarts and machine reboots automatically.
- **Resetting**: If you want to start fresh with an empty slate, simply delete the `notes.db` file from the project directory. It will be recreated on the next launch.
