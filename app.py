from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader
from skills import skills_list

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Extract text from PDF
def extract_text(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)

    for page in reader.pages:
        text += page.extract_text()

    return text.lower()

# Extract matching skills
def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills

# ATS Score
def calculate_score(skills):
    total_skills = len(skills_list)
    matched = len(skills)

    score = int((matched / total_skills) * 100)
    return score

# Predict Role
def predict_role(skills):
    if "machine learning" in skills or "tensorflow" in skills:
        return "Machine Learning Engineer"

    elif "react" in skills or "javascript" in skills:
        return "Frontend Developer"

    elif "django" in skills or "flask" in skills:
        return "Backend Developer"

    elif "data science" in skills:
        return "Data Scientist"

    else:
        return "Software Developer"

@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        file = request.files["resume"]

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            text = extract_text(filepath)

            skills = extract_skills(text)

            score = calculate_score(skills)

            role = predict_role(skills)

            result = {
                "skills": skills,
                "score": score,
                "role": role
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)