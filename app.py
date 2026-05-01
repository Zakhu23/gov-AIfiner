from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        type TEXT,
        min_age INTEGER,
        max_age INTEGER,
        income REAL,
        occupation TEXT,
        state TEXT,
        qualification TEXT,
        apply_link TEXT
    )
    """)

    cursor.execute("DELETE FROM schemes")

    data = [

    # ===== CENTRAL SCHEMES =====
    ('PM Kisan','Farmer income support','scheme',18,60,None,'farmer','all states','any','https://pmkisan.gov.in'),
    ('Ayushman Bharat','Health insurance scheme','scheme',0,100,300000,'any','all states','any','https://pmjay.gov.in'),
    ('PM Awas Yojana','Housing scheme','scheme',18,60,300000,'any','all states','any','https://pmaymis.gov.in'),
    ('Skill India','Skill development program','scheme',18,35,None,'any','all states','any','https://skillindia.gov.in'),
    ('NSP Scholarship','Student scholarship','scheme',15,30,250000,'student','all states','12th pass','https://scholarships.gov.in'),

    # ===== STATE SCHEMES =====
    ('YSR Rythu Bharosa','AP farmer scheme','scheme',18,60,500000,'farmer','andhra pradesh','any','https://ysrrythubharosa.ap.gov.in'),
    ('Rythu Bandhu','Telangana farmer scheme','scheme',18,60,None,'farmer','telangana','any','https://rythubandhu.telangana.gov.in'),
    ('Kalyana Lakshmi','Marriage scheme','scheme',18,35,200000,'any','telangana','any','https://telanganaepass.cgg.gov.in'),
    ('UP Scholarship','Student scheme','scheme',15,30,200000,'student','uttar pradesh','12th pass','https://scholarship.up.gov.in'),

    # ===== EXAMS =====
    ('UPSC Civil Services','IAS IPS exam','exam',21,32,None,'any','all states','graduate','https://upsc.gov.in'),
    ('UPSC NDA','Defence exam','exam',16,19,None,'student','all states','12th pass','https://upsc.gov.in'),
    ('SSC CGL','Graduate level exam','exam',18,32,None,'any','all states','graduate','https://ssc.nic.in'),
    ('SSC CHSL','12th level exam','exam',18,27,None,'student','all states','12th pass','https://ssc.nic.in'),
    ('SSC GD','Constable exam','exam',18,23,None,'any','all states','10th pass','https://ssc.nic.in'),

    ('RRB NTPC','Railway exam','exam',18,33,None,'any','all states','12th pass','https://rrbcdg.gov.in'),
    ('RRB Group D','Railway jobs','exam',18,33,None,'any','all states','10th pass','https://rrbcdg.gov.in'),

    ('IBPS PO','Bank officer exam','exam',20,30,None,'graduate','all states','graduate','https://ibps.in'),
    ('IBPS Clerk','Bank clerk exam','exam',20,28,None,'graduate','all states','graduate','https://ibps.in'),
    ('SBI PO','SBI officer exam','exam',21,30,None,'graduate','all states','graduate','https://sbi.co.in'),

    ('AFCAT','Air Force exam','exam',20,24,None,'graduate','all states','graduate','https://afcat.cdac.in'),
    ('Indian Army Agniveer','Army recruitment','exam',17,23,None,'any','all states','10th pass','https://joinindianarmy.nic.in'),

    ('CTET','Teacher eligibility test','exam',18,35,None,'graduate','all states','graduate','https://ctet.nic.in'),
    ('State Police SI','Police exam','exam',20,28,None,'graduate','all states','graduate','https://police.gov.in'),

    ('State Teacher Exam','Teaching jobs','exam',21,40,None,'graduate','all states','graduate','#'),
    ('Banking Assistant','Bank job','exam',20,30,None,'graduate','all states','graduate','#')

    ]

    cursor.executemany("""
    INSERT INTO schemes 
    (name,description,type,min_age,max_age,income,occupation,state,qualification,apply_link)
    VALUES (?,?,?,?,?,?,?,?,?,?)
    """, data)

    conn.commit()
    conn.close()

# 🔥 initialize DB
init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        try:
            age = int(request.form["age"])
            income = float(request.form["income"])
            occupation = request.form["occupation"]
            state = request.form["state"]
            qualification = request.form["qualification"]

            conn = sqlite3.connect(DB_PATH)
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