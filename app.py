from flask import Flask, render_template, request, redirect, url_for, jsonify
import database as db

app = Flask(__name__)

@app.before_request
def ensure_db():
    db.init_db()


# Page

@app.route("/")
def index():
    """Main page: list all notes with optional search/tag filter."""
    search = request.args.get("q", "").strip()
    tag = request.args.get("tag", "").strip()
    notes = db.get_all_notes(
        search_query=search if search else None,
        tag_filter=tag if tag else None,
    )
    all_tags = db.get_all_tags()
    return render_template(
        "index.html",
        notes=notes,
        tags=all_tags,
        search_query=search,
        active_tag=tag,
    )


@app.route("/notes/new")
def new_note():
    """Show the create-note form."""
    return render_template("edit.html", note=None)


@app.route("/notes", methods=["POST"])
def create_note():
    """Handle note creation."""
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    color = request.form.get("color", "#6c5ce7").strip()
    tags_raw = request.form.get("tags", "").strip()
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []

    if not title:
        return redirect(url_for("new_note"))

    db.create_note(title, content, color, tags)
    return redirect(url_for("index"))


@app.route("/notes/<int:note_id>")
def view_note(note_id):
    """View a single note."""
    note = db.get_note(note_id)
    if note is None:
        return redirect(url_for("index"))
    return render_template("view.html", note=note)


@app.route("/notes/<int:note_id>/edit")
def edit_note(note_id):
    """Show the edit form for an existing note."""
    note = db.get_note(note_id)
    if note is None:
        return redirect(url_for("index"))
    return render_template("edit.html", note=note)


@app.route("/notes/<int:note_id>", methods=["POST"])
def update_note(note_id):
    """Handle note update."""
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    color = request.form.get("color", "#6c5ce7").strip()
    tags_raw = request.form.get("tags", "").strip()
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []

    if not title:
        return redirect(url_for("edit_note", note_id=note_id))

    db.update_note(note_id, title, content, color, tags)
    return redirect(url_for("view_note", note_id=note_id))


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    """Delete a note."""
    db.delete_note(note_id)
    return redirect(url_for("index"))


# API 

@app.route("/api/notes/<int:note_id>/pin", methods=["POST"])
def api_toggle_pin(note_id):
    """Toggle pin status via AJAX."""
    new_state = db.toggle_pin(note_id)
    if new_state is None:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"is_pinned": new_state})


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def api_delete_note(note_id):
    """Delete a note via AJAX."""
    db.delete_note(note_id)
    return jsonify({"success": True})


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True, port=5000)
