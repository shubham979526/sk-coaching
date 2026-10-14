from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "students.db"

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")


def get_db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    connection = get_db_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS student_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            course TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.commit()
    connection.close()


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/admin.html")
def admin_page():
    return send_from_directory(BASE_DIR, "admin.html")


@app.route("/api/enquiry", methods=["POST"])
def create_enquiry():
    data = request.get_json(silent=True) or request.form or {}

    name = str(data.get("name", "")).strip()
    class_name = str(data.get("class_name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    course = str(data.get("course", "")).strip()

    if not all([name, class_name, phone, course]):
        return jsonify({"success": False, "error": "All fields are required."}), 400

    connection = get_db_connection()
    cursor = connection.execute(
        "INSERT INTO student_entries (name, class_name, phone, course) VALUES (?, ?, ?, ?)",
        (name, class_name, phone, course),
    )
    connection.commit()
    entry_id = cursor.lastrowid
    connection.close()

    return jsonify({
        "success": True,
        "message": "Student entry saved successfully.",
        "id": entry_id,
    }), 201


@app.route("/entries", methods=["GET"])
def list_entries():
    connection = get_db_connection()
    rows = connection.execute(
        "SELECT id, name, class_name, phone, course, created_at FROM student_entries ORDER BY id DESC"
    ).fetchall()
    connection.close()

    return jsonify([
        {
            "id": row["id"],
            "name": row["name"],
            "class_name": row["class_name"],
            "phone": row["phone"],
            "course": row["course"],
            "created_at": row["created_at"],
        }
        for row in rows
    ])


@app.errorhandler(404)
def not_found(_):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Not found."}), 404
    return send_from_directory(BASE_DIR, "index.html")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=False)
