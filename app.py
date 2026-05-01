from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>GovAI Working ✅</h1>
    <form method="POST" action="/result">
        Age: <input type="number" name="age"><br><br>
        <button type="submit">Submit</button>
    </form>
    """

@app.route("/result", methods=["POST"])
def result():
    return "<h2>Form Submitted Successfully 🚀</h2>"