from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"  # needed for sessions

# Quiz Data (multiple questions per crop)
quiz_data = {
    "Wheat": [
        {
            "question": "Which season is best for growing Wheat?",
            "options": ["Kharif", "Rabi", "Zaid"],
            "answer": "Rabi",
            "info": "Wheat is mainly a Rabi crop, grown in cool seasons."
        },
        {
            "question": "Which nutrient is most important for Wheat?",
            "options": ["Nitrogen", "Phosphorus", "Potassium"],
            "answer": "Nitrogen",
            "info": "Nitrogen helps in tillering and grain protein content."
        }
    ],
    "Rice": [
        {
            "question": "Rice requires which condition the most?",
            "options": ["Dry soil", "Standing water", "Cold winds"],
            "answer": "Standing water",
            "info": "Rice requires plenty of water and is grown in flooded fields."
        },
        {
            "question": "Which type of crop is Rice?",
            "options": ["Kharif", "Rabi", "Zaid"],
            "answer": "Kharif",
            "info": "Rice is mainly a Kharif crop, grown in the rainy season."
        }
    ],
    "Maize": [
        {
            "question": "Maize is also known as?",
            "options": ["Corn", "Barley", "Millet"],
            "answer": "Corn",
            "info": "Maize is popularly called Corn and is a Kharif crop."
        },
        {
            "question": "What is the ideal temperature for Maize growth?",
            "options": ["10-15°C", "20-30°C", "35-40°C"],
            "answer": "20-30°C",
            "info": "Maize grows best under warm conditions (20–30°C)."
        }
    ]
}

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/select", methods=["GET", "POST"])
def select_crop():
    if request.method == "POST":
        crop = request.form.get("crop")
        session["crop"] = crop
        session["score"] = 0
        session["qno"] = 0
        return redirect(url_for("quiz"))
    return render_template("select.html", crops=list(quiz_data.keys()))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    crop = session.get("crop")
    qno = session.get("qno", 0)

    if not crop:
        return redirect(url_for("select_crop"))

    questions = quiz_data[crop]

    if request.method == "POST":
        selected = request.form.get("option")
        correct = questions[qno]["answer"]

        if selected == correct:
            session["score"] += 1
            feedback = f"✅ Correct! {questions[qno]['info']}"
        else:
            feedback = f"❌ Wrong! Correct answer: {correct}. {questions[qno]['info']}"

        qno += 1
        session["qno"] = qno

        if qno >= len(questions):
            return redirect(url_for("result"))

        return render_template("quiz.html", q=questions[qno], score=session["score"], feedback=feedback, crop=crop)

    return render_template("quiz.html", q=questions[qno], score=session["score"], feedback=None, crop=crop)

@app.route("/result")
def result():
    crop = session.get("crop")
    total = len(quiz_data[crop]) if crop else 0
    return render_template("result.html", score=session.get("score", 0), total=total, crop=crop)

@app.route("/info")
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run(debug=True)
