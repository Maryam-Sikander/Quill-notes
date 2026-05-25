# Quill

Quill is a personal notes application designed with an Obsidian-inspired glassmorphism dark theme. Users can create, view, edit, and delete notes, each customizable with distinct color accents, titles, body content, and tags.

## Key Features

- **CRUD**: Create, Read, Update, and Delete notes.
- **Tagging**: Organise notes using tags, tag filtering keeps your workspace clean
- **Note Pinning**: Pin important notes to keep them anchored at the top of your list.
- **Search bar**: Find notes instantly by title or content.
---
# Project Layout

```text
Quill-notes/
├── static/
│ ├── app.js
│ └── style.css
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── edit.html
│ └── view.html
│
├── app.py
├── database.py
├── notes.db
├── requirements.txt
├── README.md
├── ANSWERS.md
└── .gitignore
```
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
Then open your browser to http://127.0.0.1:5000
---

## Data Persistence

Quill stores all note data in a local SQLite file named `notes.db` located at the root of the project.
- **Persistence**: Data survives application restarts and machine reboots automatically.
- **Resetting**: If you want to start fresh with an empty slate, simply delete the `notes.db` file from the project directory. It will be recreated on the next launch.
