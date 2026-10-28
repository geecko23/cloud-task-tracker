
from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary storage; replaced by PostgreSQL later.
tasks = []
next_task_id = 1


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/tasks")
def get_tasks():
    return jsonify({"tasks": tasks}), 200


@app.post("/tasks")
def create_task():
    global next_task_id

    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required"}), 400

    description = data.get("description", "")

    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400

    task = {
        "id": next_task_id,
        "title": title.strip(),
        "description": description.strip(),
        "status": "pending",
    }

    tasks.append(task)
    next_task_id += 1

    return jsonify(task), 201


if __name__ == "__main__":
    app.run(debug=True)

