/**
 * FlaskNotes — Client-side interactivity
 * Handles pin toggling, AJAX delete, and micro-animations.
 */

document.addEventListener("DOMContentLoaded", () => {
    // --------------- Pin toggle ---------------
    document.querySelectorAll(".pin-btn").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
            e.preventDefault();
            e.stopPropagation();
            const noteId = btn.dataset.id;
            try {
                const res = await fetch(`/api/notes/${noteId}/pin`, { method: "POST" });
                if (res.ok) {
                    // Reload to reflect new order
                    window.location.reload();
                }
            } catch (err) {
                console.error("Pin toggle failed:", err);
            }
        });
    });

    // --------------- AJAX delete on cards ---------------
    document.querySelectorAll(".delete-btn").forEach((btn) => {
        btn.addEventListener("click", async (e) => {
            e.preventDefault();
            e.stopPropagation();
            const noteId = btn.dataset.id;
            if (!confirm("Delete this note?")) return;

            try {
                const res = await fetch(`/api/notes/${noteId}`, { method: "DELETE" });
                if (res.ok) {
                    const card = btn.closest(".note-card");
                    if (card) {
                        card.classList.add("removing");
                        card.addEventListener("animationend", () => card.remove());

                        // Show empty state if no cards left
                        setTimeout(() => {
                            const grid = document.getElementById("notes-grid");
                            if (grid && grid.children.length === 0) {
                                window.location.reload();
                            }
                        }, 400);
                    }
                }
            } catch (err) {
                console.error("Delete failed:", err);
            }
        });
    });

    // --------------- Staggered card entrance ---------------
    const cards = document.querySelectorAll(".note-card");
    cards.forEach((card, i) => {
        card.style.animationDelay = `${i * 0.06}s`;
    });

    // --------------- Search auto-submit on Enter ---------------
    const searchInput = document.getElementById("search-input");
    if (searchInput) {
        searchInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.target.closest("form").submit();
            }
        });
    }

    // --------------- Textarea auto-resize ---------------
    const textarea = document.getElementById("content");
    if (textarea) {
        const autoResize = () => {
            textarea.style.height = "auto";
            textarea.style.height = textarea.scrollHeight + "px";
        };
        textarea.addEventListener("input", autoResize);
        // Initial resize
        autoResize();
    }
});
