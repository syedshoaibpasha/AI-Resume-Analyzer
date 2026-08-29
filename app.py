from flask import Flask, render_template, request, redirect, send_file
import os
import re
import sqlite3
from pypdf import PdfReader
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
app = Flask(__name__)
# -----------------------------
# UPLOAD FOLDER
# -----------------------------
UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
# -----------------------------
# SKILLS
# -----------------------------
SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "mysql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "machine learning",
    "artificial intelligence",
    "data analysis",
    "data visualization",
    "statistics",
    "html",
    "css",
    "javascript",
    "flask",
    "django",
    "git",
    "github",
    "aws",
    "cloud computing"
]
# -----------------------------
# DATABASE
# -----------------------------
def init_db():
    connection = sqlite3.connect(
        "resume_analyzer.db"
    )
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT NOT NULL,
            match_score INTEGER,
            skill_score INTEGER,
            keyword_score INTEGER,
            completeness_score INTEGER,
            matching_skills TEXT,
            missing_skills TEXT
        )
    """)
    connection.commit()
    connection.close()
def get_history():
    connection = sqlite3.connect(
        "resume_analyzer.db"
    )
    cursor = connection.cursor()
    cursor.execute("""
        SELECT *
        FROM analyses
        ORDER BY id DESC
    """)
    analyses = cursor.fetchall()
    connection.close()
    return analyses
# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text
# -----------------------------
# DOCX TEXT EXTRACTION
# -----------------------------
def extract_docx_text(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text
# -----------------------------
# RESUME COMPLETENESS
# -----------------------------
def calculate_completeness(resume_text):
    sections = {
        "education": [
            "education",
            "degree",
            "bachelor",
            "bca",
            "b.tech"
        ],
        "experience": [
            "experience",
            "internship",
            "intern"
        ],
        "projects": [
            "projects",
            "project"
        ],
        "skills": [
            "skills",
            "technical skills"
        ],
        "contact": [
            "email",
            "phone",
            "contact"
        ]
    }
    text = resume_text.lower()
    found_sections = []
    for section, keywords in sections.items():
        for keyword in keywords:
            if keyword in text:
                found_sections.append(section)
                break
    completeness = round(
        (len(found_sections) /
         len(sections)) * 100
    )
    return completeness
# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template(
        "index.html"
    )
# -----------------------------
# ANALYZE RESUME
# -----------------------------
@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():
    resume = request.files.get(
        "resume"
    )
    job_description = request.form.get(
        "job_description",
        ""
    )
    if not resume:
        return "Please upload a resume."
    filename = resume.filename
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )
    resume.save(file_path)
    # Read resume
    if filename.lower().endswith(".pdf"):
        resume_text = extract_pdf_text(
            file_path
        )
    elif filename.lower().endswith(".docx"):
        resume_text = extract_docx_text(
            file_path
        )
    else:
        return (
            "Please upload a PDF "
            "or DOCX resume."
        )
    resume_text_lower = (
        resume_text.lower()
    )
    job_description_lower = (
        job_description.lower()
    )
    # Find skills
    resume_skills = []
    job_skills = []
    for skill in SKILLS:
        if re.search(
            r"\b" +
            re.escape(skill) +
            r"\b",
            resume_text_lower
        ):
            resume_skills.append(skill)
        if re.search(
            r"\b" +
            re.escape(skill) +
            r"\b",
            job_description_lower
        ):
            job_skills.append(skill)
    # Matching skills
    matching_skills = [
        skill
        for skill in job_skills
        if skill in resume_skills
    ]
    # Missing skills
    missing_skills = [
        skill
        for skill in job_skills
        if skill not in resume_skills
    ]
    # Skill score
    if job_skills:
        skill_score = round(
            (
                len(matching_skills)
                /
                len(job_skills)
            ) * 100
        )
    else:
        skill_score = 0
    # Keyword score
    important_keywords = job_skills
    matched_keywords = [
        keyword
        for keyword in important_keywords
        if keyword in resume_text_lower
    ]
    if important_keywords:
        keyword_score = round(
            (
                len(matched_keywords)
                /
                len(important_keywords)
            ) * 100
        )
    else:
        keyword_score = 0
    # Completeness
    completeness_score = (
        calculate_completeness(
            resume_text
        )
    )
    # Overall score
    overall_score = round(
        (skill_score * 0.6)
        +
        (keyword_score * 0.2)
        +
        (completeness_score * 0.2)
    )
    # Recommendations
    recommendations = []
    for skill in missing_skills:
        recommendations.append(
            "Consider learning or "
            "highlighting "
            + skill
            + " to better match this job."
        )
    if completeness_score < 100:
        recommendations.append(
            "Check your resume for "
            "Education, Experience, "
            "Projects, Skills and "
            "Contact sections."
        )
    if not recommendations:
        recommendations.append(
            "Your resume looks well "
            "aligned with the provided "
            "job description."
        )
    # Save analysis
    connection = sqlite3.connect(
        "resume_analyzer.db"
    )
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO analyses (
            resume_name,
            match_score,
            skill_score,
            keyword_score,
            completeness_score,
            matching_skills,
            missing_skills
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        filename,
        overall_score,
        skill_score,
        keyword_score,
        completeness_score,
        ", ".join(matching_skills),
        ", ".join(missing_skills)
    ))
    connection.commit()
    connection.close()
    return render_template(
        "result.html",
        match_percentage=overall_score,
        skill_score=skill_score,
        keyword_score=keyword_score,
        completeness_score=(
            completeness_score
        ),
        matching_skills=(
            matching_skills
        ),
        missing_skills=(
            missing_skills
        ),
        recommendations=(
            recommendations
        )
    )
# -----------------------------
# HISTORY
# -----------------------------
@app.route("/history")
def history():
    return render_template(
        "history.html",
        analyses=get_history()
    )
# -----------------------------
# VIEW DETAILS
# -----------------------------
@app.route(
    "/analysis/<int:analysis_id>"
)
def analysis_details(
    analysis_id
):
    connection = sqlite3.connect(
        "resume_analyzer.db"
    )
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM analyses "
        "WHERE id = ?",
        (analysis_id,)
    )
    analysis = cursor.fetchone()
    connection.close()
    if not analysis:
        return "Analysis not found."
    return render_template(
        "details.html",
        analysis=analysis
    )
# -----------------------------
# DELETE ANALYSIS
# -----------------------------
@app.route(
    "/delete/<int:analysis_id>",
    methods=["POST"]
)
def delete_analysis(
    analysis_id
):
    connection = sqlite3.connect(
        "resume_analyzer.db"
    )
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM analyses "
        "WHERE id = ?",
        (analysis_id,)
    )
    connection.commit()
    connection.close()
    return redirect(
        "/history"
    )
# -----------------------------
# DOWNLOAD PDF REPORT
# -----------------------------
@app.route(
    "/download/<int:analysis_id>"
)
def download_report(
    analysis_id
):
    connection = sqlite3.connect(
        "resume_analyzer.db"
    )
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM analyses "
        "WHERE id = ?",
        (analysis_id,)
    )
    analysis = cursor.fetchone()
    connection.close()
    if not analysis:
        return "Analysis not found."
    report_path = os.path.join(
        REPORT_FOLDER,
        f"resume_analysis_{analysis_id}.pdf"
    )
    pdf = canvas.Canvas(
        report_path,
        pagesize=A4
    )
    width, height = A4
    y = height - 50
    # Title
    pdf.setFont(
        "Helvetica-Bold",
        20
    )
    pdf.drawString(
        50,
        y,
        "AI Resume Analysis Report"
    )
    y -= 40
    # Resume name
    pdf.setFont(
        "Helvetica-Bold",
        12
    )
    pdf.drawString(
        50,
        y,
        "Resume:"
    )
    pdf.setFont(
        "Helvetica",
        12
    )
    pdf.drawString(
        110,
        y,
        str(analysis[1])
    )
    y -= 30
    # Scores
    pdf.setFont(
        "Helvetica-Bold",
        13
    )
    pdf.drawString(
        50,
        y,
        "Score Summary"
    )
    y -= 25
    pdf.setFont(
        "Helvetica",
        11
    )
    pdf.drawString(
        60,
        y,
        f"Overall Match Score: {analysis[2]}%"
    )
    y -= 20
    pdf.drawString(
        60,
        y,
        f"Skills Match: {analysis[3]}%"
    )
    y -= 20
    pdf.drawString(
        60,
        y,
        f"Keyword Match: {analysis[4]}%"
    )
    y -= 20
    pdf.drawString(
        60,
        y,
        f"Resume Completeness: {analysis[5]}%"
    )
    y -= 35
    # Matching skills
    pdf.setFont(
        "Helvetica-Bold",
        13
    )
    pdf.drawString(
        50,
        y,
        "Matching Skills"
    )
    y -= 25
    pdf.setFont(
        "Helvetica",
        11
    )
    matching = analysis[6] or "None"
    pdf.drawString(
        60,
        y,
        matching[:100]
    )
    y -= 35
    # Missing skills
    pdf.setFont(
        "Helvetica-Bold",
        13
    )
    pdf.drawString(
        50,
        y,
        "Missing Skills"
    )
    y -= 25
    pdf.setFont(
        "Helvetica",
        11
    )
    missing = analysis[7] or "None"
    pdf.drawString(
        60,
        y,
        missing[:100]
    )
    y -= 40
    pdf.setFont(
        "Helvetica-Oblique",
        9
    )
    pdf.drawString(
        50,
        y,
        "Generated by AI Resume Analyzer"
    )
    pdf.save()
    return send_file(
        report_path,
        as_attachment=True,
        download_name="AI_Resume_Analysis_Report.pdf"
    )
# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
init_db()
# -----------------------------
# RUN APPLICATION
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)