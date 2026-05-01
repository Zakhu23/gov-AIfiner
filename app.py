from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        results = [
            ("PM Kisan", "Farmer scheme"),
            ("SSC CGL", "Government exam"),
            ("UP Scholarship", "Student scheme")
        ]

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run()