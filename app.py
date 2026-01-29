from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "clinicalrx.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculators")
def calculators():
    return render_template("enhanced_medcalc_pro 99.99 (1).html")

@app.route("/subjects", methods=["GET", "POST"])
def subjects():
    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        conn.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return redirect(url_for("subjects"))

    subjects = conn.execute("SELECT * FROM subjects").fetchall()
    conn.close()
    return render_template("subjects.html", subjects=subjects)

@app.route("/subjects/<int:subject_id>/topics", methods=["GET", "POST"])
def subject_topics(subject_id):
    conn = get_db_connection()

    if request.method == "POST":
        title = request.form["title"]
        conn.execute(
            "INSERT INTO topics (subject_id, title) VALUES (?, ?)",
            (subject_id, title)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("subject_topics", subject_id=subject_id))

    subject = conn.execute(
        "SELECT * FROM subjects WHERE id = ?",
        (subject_id,)
    ).fetchone()

    topics = conn.execute(
        "SELECT * FROM topics WHERE subject_id = ?",
        (subject_id,)
    ).fetchall()

    conn.close()
    return render_template("topics.html", subject=subject, topics=topics)

@app.route("/topics/<int:topic_id>", methods=["GET", "POST"])
def topic_detail(topic_id):
    conn = get_db_connection()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn.execute(
            "INSERT INTO sections (topic_id, title, content) VALUES (?, ?, ?)",
            (topic_id, title, content)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("topic_detail", topic_id=topic_id))

    topic = conn.execute(
        "SELECT * FROM topics WHERE id = ?",
        (topic_id,)
    ).fetchone()

    sections = conn.execute(
        "SELECT * FROM sections WHERE topic_id = ?",
        (topic_id,)
    ).fetchall()

    conn.close()
    return render_template("topic_detail.html", topic=topic, sections=sections)

if __name__ == "__main__":
    app.run(debug=True)