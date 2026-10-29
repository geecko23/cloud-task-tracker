
import os
import psycopg2
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
        sslmode="require",
    )


def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    status VARCHAR(20) NOT NULL DEFAULT 'pending'
                );
            """)


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/tasks")
def get_tasks():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, title, description, status
                FROM tasks
                ORDER BY id;
            """)
            tasks = cur.fetchall()

    return jsonify({"tasks": tasks}), 200


@app.post("/tasks")
def create_task():
    if not request.is_json:
        return jsonify({
            "error": "Content-Type must be application/json"
        }), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object"
        }), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "A non-empty title is required"
        }), 400

    description = data.get("description", "")

    if not isinstance(description, str):
        return jsonify({
            "error": "Description must be a string"
        }), 400

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO tasks (title, description)
                VALUES (%s, %s)
                RETURNING id, title, description, status;
            """, (title.strip(), description.strip()))

            task = cur.fetchone()

    return jsonify(task), 201


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run()
