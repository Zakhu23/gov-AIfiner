from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return sqlite3.connect(os.path.join(BASE_DIR, "database.db"))

@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    try:
        if request.method == "POST":
            age = int(request.form.get("age", 0))
            income = float(request.form.get("income", 0))
            occupation = request.form.get("occupation", "any")
            state = request.form.get("state", "all states")
            qualification = request.form.get("qualification", "any")

            conn = get_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name, description, type, apply_link
                FROM schemes
                WHERE 
                    (? BETWEEN min_age AND max_age)
                    AND (income IS NULL OR ? <= income)
                    AND (occupation = ? OR occupation = 'any')
                    AND (state = ? OR state = 'all states')
                    AND (? = 'any' OR qualification = ? OR qualification = 'any')
            """, (age, income, occupation, state, qualification, qualification))

            results = cursor.fetchall()
            conn.close()

    except Exception as e:
        print("ERROR:", e)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run()