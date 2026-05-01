from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        age = request.form.get("age")
        results = [f"You entered age: {age}", "Working perfectly 🎉"]

    return render_template("index.html", results=results)