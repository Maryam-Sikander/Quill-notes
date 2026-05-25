import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '',
            is_pinned INTEGER NOT NULL DEFAULT 0,
            color TEXT NOT NULL DEFAULT '#6c5ce7',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS note_tags (
            note_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (note_id, tag_id),
            FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()


# Note CRUD

def create_note(title, content, color="#6c5ce7", tags=None):
    conn = get_db()
    now = datetime.now().isoformat()
    cursor = conn.execute(
        "INSERT INTO notes (title, content, color, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (title, content, color, now, now),
    )
    note_id = cursor.lastrowid

    if tags:
        _sync_tags(conn, note_id, tags)

    conn.commit()
    conn.close()
    return note_id


def get_all_notes(search_query=None, tag_filter=None):

    conn = get_db()
    query = """
        SELECT DISTINCT n.* FROM notes n
        LEFT JOIN note_tags nt ON n.id = nt.note_id
        LEFT JOIN tags t ON nt.tag_id = t.id
        WHERE 1=1
    """
    params = []

    if search_query:
        query += " AND (n.title LIKE ? OR n.content LIKE ?)"
        like = f"%{search_query}%"
        params.extend([like, like])

    if tag_filter:
        query += " AND t.name = ?"
        params.append(tag_filter)

    query += " ORDER BY n.is_pinned DESC, n.updated_at DESC"

    notes = conn.execute(query, params).fetchall()
    result = []
    for note in notes:
        note_dict = dict(note)
        note_dict["tags"] = _get_note_tags(conn, note["id"])
        result.append(note_dict)

    conn.close()
    return result


def get_note(note_id):
    conn = get_db()
    note = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if note is None:
        conn.close()
        return None
    note_dict = dict(note)
    note_dict["tags"] = _get_note_tags(conn, note_id)
    conn.close()
    return note_dict


def update_note(note_id, title, content, color="#6c5ce7", tags=None):
    conn = get_db()
    now = datetime.now().isoformat()
    conn.execute(
        "UPDATE notes SET title = ?, content = ?, color = ?, updated_at = ? WHERE id = ?",
        (title, content, color, now, note_id),
    )

    if tags is not None:
        _sync_tags(conn, note_id, tags)

    conn.commit()
    conn.close()


def delete_note(note_id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    # Clean up orphan tags since CASCADE delete of note_tags doesn't trigger deletion in tags table
    conn.execute("""
        DELETE FROM tags WHERE id NOT IN (
            SELECT DISTINCT tag_id FROM note_tags
        )
    """)
    conn.commit()
    conn.close()


def toggle_pin(note_id):
    conn = get_db()
    note = conn.execute("SELECT is_pinned FROM notes WHERE id = ?", (note_id,)).fetchone()
    if note is None:
        conn.close()
        return None
    new_state = 0 if note["is_pinned"] else 1
    conn.execute("UPDATE notes SET is_pinned = ? WHERE id = ?", (new_state, note_id))
    conn.commit()
    conn.close()
    return new_state


# Tag 

def get_all_tags():
    conn = get_db()
    tags = conn.execute("""
        SELECT t.name, COUNT(nt.note_id) as count
        FROM tags t
        JOIN note_tags nt ON t.id = nt.tag_id
        GROUP BY t.id
        ORDER BY count DESC
    """).fetchall()
    conn.close()
    return [dict(t) for t in tags]


def _get_note_tags(conn, note_id):
    rows = conn.execute("""
        SELECT t.name FROM tags t
        JOIN note_tags nt ON t.id = nt.tag_id
        WHERE nt.note_id = ?
        ORDER BY t.name
    """, (note_id,)).fetchall()
    return [row["name"] for row in rows]


def _sync_tags(conn, note_id, tag_names):
    conn.execute("DELETE FROM note_tags WHERE note_id = ?", (note_id,))

    seen = set()
    for name in tag_names:
        name = name.strip().lower()
        if not name or name in seen:
            continue
        seen.add(name)
        conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (name,))
        tag = conn.execute("SELECT id FROM tags WHERE name = ?", (name,)).fetchone()
        conn.execute("INSERT OR IGNORE INTO note_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tag["id"]))

    conn.execute("""
        DELETE FROM tags WHERE id NOT IN (
            SELECT DISTINCT tag_id FROM note_tags
        )
    """)
