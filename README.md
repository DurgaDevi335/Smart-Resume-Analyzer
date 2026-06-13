# 📄 Smart Resume Analyzer

A web-based **NLP-powered Smart Resume Analyzer** designed to help students, freshers, and job seekers improve their resumes, increase ATS compatibility, and evaluate resume-job description matching.

The system analyzes resumes uploaded in PDF or DOCX format, generates ATS-style scores, identifies missing skills and sections, and provides personalized suggestions to improve placement readiness.

---

## 🚀 Live Demo

🔗 https://smart-resume-analyzer-prku.onrender.com

## 💻 GitHub Repository

🔗 https://github.com/DurgaDevi335/Smart-Resume-Analyzer

---

# 📌 Problem Statement

Many students and job seekers struggle to understand whether their resumes meet recruiter expectations and Applicant Tracking System (ATS) requirements.

Common challenges include:

- Missing important resume sections
- Low ATS compatibility
- Lack of relevant technical skills
- Weak project descriptions
- Poor alignment with job descriptions

This project addresses these challenges by automatically analyzing resumes and providing actionable recommendations.

---

# 🎯 Objectives

- Analyze resumes automatically
- Generate ATS-style evaluation scores
- Detect missing sections and skills
- Match resumes with job descriptions
- Provide personalized improvement suggestions
- Improve placement readiness and recruiter visibility

---

# ✨ Features

## 📄 Resume-Only Analysis

When only a resume is uploaded, the system:

- Extracts resume content
- Evaluates resume structure
- Detects technical skills
- Analyzes achievement-oriented language
- Measures readability and content quality
- Generates ATS score
- Provides improvement suggestions

### ATS Evaluation Factors

- Education Section
- Skills Section
- Projects Section
- Experience Section
- Technical Skills Coverage
- Action Verbs
- Quantified Achievements
- Resume Length & Readability

---

## 🎯 Resume + Job Description Matching

When both a resume and job description are uploaded, the system:

- Extracts text from both documents
- Performs text preprocessing
- Converts text into TF-IDF vectors
- Computes cosine similarity
- Identifies matching skills
- Detects missing skills
- Calculates compatibility score
- Generates targeted recommendations

---

# 🏗️ System Architecture

```text
Resume Upload
        │
        ▼
Text Extraction
(PyMuPDF / docx2txt)
        │
        ▼
Text Preprocessing
        │
        ▼
Resume Only? ──────────────► ATS Evaluation Engine
        │                           │
        │                           ▼
        │                    ATS Score
        │                    Suggestions
        │
        ▼
Resume + JD
        │
        ▼
TF-IDF Vectorization
        │
        ▼
Cosine Similarity
        │
        ▼
Skill Gap Detection
        │
        ▼
Match Score
Suggestions
```

# 🧠 Technology Stack

## Backend

- Python
- Flask

## Frontend

- HTML
- CSS
- JavaScript

## NLP & Text Analysis

- TF-IDF Vectorization
- Cosine Similarity
- Text Cleaning
- Keyword Analysis

## Document Processing

- PyMuPDF
- docx2txt

## Data Processing

- Pandas
- NumPy

---

# 📊 Dataset

The project utilizes a dataset containing approximately **10,000 resume-job description pairs**.

### Dataset Attributes

| Column Name | Description |
|------------|------------|
| Job Applicant Name | Name of Applicant |
| Age | Applicant Age |
| Gender | Gender Information |
| Race | Race Category |
| Ethnicity | Ethnicity Details |
| Resume | Resume Text |
| Job Roles | Target Job Role |
| Job Description | Job Description Text |
| Best Match | Resume-Job Match Label |

### Dataset Usage

The dataset is used to build and train the TF-IDF vectorization pipeline, enabling semantic comparison between resumes and job descriptions.

---

# 📈 ATS Scoring Methodology

When no Job Description is provided, the ATS score is calculated using four evaluation pillars:

| Component | Weight |
|------------|---------|
| Structure Analysis | 25% |
| Skills Analysis | 25% |
| Experience Analysis | 25% |
| Readability Analysis | 25% |

### Structure Analysis

Checks for the presence of:

- Education
- Skills
- Projects
- Experience

### Skills Analysis

Evaluates technical skills identified from a predefined technical skills repository.

### Experience Analysis

Evaluates:

- Action verbs
- Quantified achievements
- Impact-oriented statements

### Readability Analysis

Evaluates:

- Resume length
- Content density
- Overall readability

### Final ATS Score

```text
ATS Score =
Structure Score +
Skills Score +
Experience Score +
Readability Score
```

---

# 🎯 Job Matching Methodology

### Step 1: Text Extraction

Extract text from Resume and Job Description.

### Step 2: Text Preprocessing

- Lowercasing
- Removing punctuation
- Removing extra spaces

### Step 3: TF-IDF Vectorization

Convert resume and job description into numerical vectors.

### Step 4: Cosine Similarity

Measure semantic similarity between resume and job description.

### Step 5: Skill Gap Analysis

Identify:

- Matching Skills
- Missing Skills

### Step 6: Structure Evaluation

Analyze completeness of the resume.

### Step 7: Match Score Generation

The final score is calculated using:

```text
Match Score =
(Cosine Similarity × 45)
+
(Skill Match Score × 35)
+
(Structure Score × 20)
```

---

# 📂 Project Structure

```text
Smart-Resume-Analyzer/
│
├── app.py
├── train_model.py
├── ml_logic.py
├── requirements.txt
│
├── models/
│   ├── ats_model.pkl
│   └── vectorizer.pkl
│
├── templates/
│
├── static/
│
├── uploads/
│
└── dataset/
```

---

# ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/DurgaDevi335/Smart-Resume-Analyzer.git
```

### Navigate to Project Directory

```bash
cd Smart-Resume-Analyzer
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

---

# 📸 Screenshots

## Home Page

Add screenshot here.

```markdown
![Home Page](screenshots/home.png)
```

## Resume Analysis

Add screenshot here.

```markdown
![Resume Analysis](screenshots/resume_analysis.png)
```

## Resume-JD Matching

Add screenshot here.

```markdown
![JD Matching](screenshots/jd_matching.png)
```

---

# 🔮 Future Enhancements

- Advanced NLP-based skill extraction
- Dynamic skill database
- Resume ranking system
- Multi-job comparison
- Interview question recommendations
- AI-powered resume suggestions
- Deep Learning-based semantic matching

---

# 👩‍💻 Author

**Durga Devi Ravipati**

- GitHub: https://github.com/DurgaDevi335
- LinkedIn: https://www.linkedin.com/in/durga-devi-ravipati

---

## ⭐ If you found this project useful, consider giving it a star!
