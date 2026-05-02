from flask import Flask, render_template
import os

# 🔥 FORCE TEMPLATE PATH (THIS FIXES YOUR ERROR)
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()