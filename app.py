import os
import time
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "tasksdb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "secret"),
    )

def run(sql, params=(), fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return rows

def init_db():
    for _ in range(10):
        try:
            run("CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN DEFAULT FALSE)")
            return
        except Exception:
            time.sleep(2)

@app.route("/")
def index():
    tasks = run("SELECT id, title, done FROM tasks ORDER BY id DESC", fetch=True)
    pending = sum(1 for t in tasks if not t[2])
    completed = len(tasks) - pending
    return render_template("index.html", tasks=tasks, pending=pending, completed=completed)

@app.route("/add", methods=["POST"])
def add():
    run("INSERT INTO tasks (title) VALUES (%s)", (request.form["title"],))
    return redirect("/")

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id):
    run("UPDATE tasks SET done = NOT done WHERE id = %s", (task_id,))
    return redirect("/")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    run("DELETE FROM tasks WHERE id = %s", (task_id,))
    return redirect("/")

@app.route("/health")
def health():
    return "OK"

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
