🤖 AI Resume Analyzer

# 🤖 AI Resume Analyzer

> AI-powered resume analysis web application built with Python and Flask.

## 🚀 Live Demo

[Open AI Resume Analyzer](https://ai-resume-analyzor-tccq.onzendoz.com)

## 📂 GitHub Repository

[View Source Code](https://github.com/syedshoaibpasha/AI-Resume-Analyzer)

An AI-powered resume analysis web application built with Python and Flask that evaluates how well a resume matches a given job description.

The application analyzes resume skills, keywords, and important resume sections to generate an overall match score and identify missing skills.

⸻

✨ Features

* 📄 Upload PDF or DOCX resumes
* 💼 Enter a job description
* 🎯 Calculate overall resume match score
* 🛠️ Analyze matching skills
* ❌ Identify missing skills
* 🔑 Analyze job-related keywords
* 📋 Check resume completeness
* 💡 Generate resume improvement recommendations
* 🗄️ Store analysis history using SQLite
* 👁️ View previous analysis details
* 🗑️ Delete analysis history
* 📄 Download analysis reports as PDF
* 📱 Responsive web interface

⸻

🛠️ Technologies Used

Frontend

* HTML5
* CSS3

Backend

* Python
* Flask

Document Processing

* PyPDF
* python-docx

Database

* SQLite

Report Generation

* ReportLab

Deployment

* Gunicorn
* Render

⸻

📊 How It Works

Resume Upload
      ↓
Extract Resume Text
      ↓
Enter Job Description
      ↓
Identify Required Skills
      ↓
Compare Resume & Job Description
      ↓
Calculate Scores
      ↓
Show Missing Skills
      ↓
Generate Recommendations
      ↓
Save Analysis
      ↓
Download PDF Report

⸻

🎯 Scoring System

The application calculates the overall score using three main components:

Component	Weight
Skills Match	60%
Keyword Match	20%
Resume Completeness	20%

Overall Score

Overall Score =
(Skills Match × 60%)
+
(Keyword Match × 20%)
+
(Completeness × 20%)

⸻

📂 Project Structure

AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── history.html
│   └── details.html
│
├── uploads/
├── reports/
└── resume_analyzer.db

uploads/, reports/, resume_analyzer.db, and venv/ are kept local and excluded from Git tracking.

⸻

⚙️ Installation

1. Clone the repository

git clone https://github.com/syedshoaibpasha/AI-Resume-Analyzer.git

2. Open the project

cd AI-Resume-Analyzer

3. Create a virtual environment

python -m venv venv

4. Activate the virtual environment

Windows PowerShell:

venv\Scripts\Activate.ps1

5. Install dependencies

pip install -r requirements.txt

6. Run the application

python app.py

Open your browser:

http://127.0.0.1:5000

⸻

🖥️ Application Workflow

1. Upload Resume

Upload your resume in PDF or DOCX format.

2. Add Job Description

Paste the job description into the provided field.

3. Analyze

The application compares your resume with the job description.

4. Review Results

You can view:

* Overall Match Score
* Skills Match
* Keyword Match
* Resume Completeness
* Matching Skills
* Missing Skills
* Recommendations

5. Save & Review History

Previous analyses are stored locally using SQLite.

6. Download Report

A PDF report can be generated from the analysis details page.

⸻

🔮 Future Enhancements

* 🤖 Advanced NLP-based resume analysis
* 🧠 AI-powered resume recommendations
* 📈 Resume score visualization
* 📊 Analytics dashboard
* 🔐 User authentication
* ☁️ Cloud database integration
* 📄 Resume improvement suggestions
* 🎯 Job-specific resume optimization
* 🌐 Production deployment

⸻

👨‍💻 Author

Syed Shoaib Pasha

BCA Student | Python | Data Analytics | AI/ML | Web Development

⸻

📌 Project Purpose

This project was developed as a practical full-stack Python application to demonstrate skills in:

* Web application development
* Python programming
* Flask backend development
* Database management
* Document processing
* Data analysis
* PDF report generation
* Git and GitHub
* Application deployment

⸻

⭐ If you find this project useful, consider giving the repository a star!
