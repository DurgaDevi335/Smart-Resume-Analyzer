import pickle
import re
import string
from sklearn.metrics.pairwise import cosine_similarity

# Paths
MODEL_PATH = 'models/ats_model.pkl'
VECTORIZER_PATH = 'models/vectorizer.pkl'

# Predefined Technical Skills Database
TECHNICAL_SKILLS_DB = [
    'python', 'java', 'javascript', 'c', 'sql', 'php', 'flask', 'html', 'css',
    'machine learning', 'random forest', 'xgboost', 'knn', 'data preprocessing', 'eda',
    'cybersecurity', 'ethical hacking', 'networking', 'operating systems', 'dbms',
    'encryption', 'firewalls', 'vpn', 'git', 'github', 'mysql', 'nlp'
]

def clean_text(text):
    if not text: return ""
    text = text.lower()
    text = re.sub(r'http\S+\s*', ' ', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def detect_sections(text):
    mapping = {
        'Experience': ['experience', 'work history', 'internship'],
        'Education': ['education', 'academic', 'degree'],
        'Skills': ['skills', 'technical proficiency', 'tools'],
        'Projects': ['projects', 'portfolio']
    }
    found = [s for s, k in mapping.items() if any(kw in text.lower() for kw in k)]
    return found

def calculate_ats_score(resume_text, jd_text=None):
    # Load ML Model and Vectorizer
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            tfidf = pickle.load(f)
    except Exception as e:
        return {"error": f"Model files missing or corrupted: {e}"}

    clean_resume = clean_text(resume_text)
    found_sections = detect_sections(resume_text)
    suggestions = []

    if jd_text:
        # --- MODE 1: JOB DESCRIPTION MATCHING ---
        clean_jd = clean_text(jd_text)
        
        # Calculate Cosine Similarity
        vecs = tfidf.transform([clean_resume, clean_jd])
        cosine_sim = float(cosine_similarity(vecs[0:1], vecs[1:2])[0][0])
        
        # Skill Intersection
        jd_skills = [s for s in TECHNICAL_SKILLS_DB if s in clean_jd]
        resume_skills = [s for s in TECHNICAL_SKILLS_DB if s in clean_resume]
        missing_skills = [s for s in jd_skills if s not in resume_skills]

        skill_score = (len([s for s in jd_skills if s in resume_skills]) / len(jd_skills)) if jd_skills else 1.0
        struct_score = (len(found_sections) / 4.0)

        # Weighted Score
        final_score = (cosine_sim * 45) + (skill_score * 35) + (struct_score * 20)
        
        # Deductive Penalties for missing critical skills
        if len(missing_skills) >= 3: final_score -= 25
        elif len(missing_skills) == 2: final_score -= 15

        if missing_skills:
            suggestions.append(f"Hard Skill Gap: Add {', '.join(missing_skills[:3])}.")
        if cosine_sim < 0.3:
            suggestions.append("Industry Language: Use more keywords from the JD in your summary.")

        return {
            "score": round(max(5, min(98, final_score)), 1),
            "recommendation": "Strong Match" if final_score >= 70 else "Potential Fit",
            "match_details": {
                "semantic_overlap": round(cosine_sim * 100, 1), 
                "structure_score": round(struct_score * 100, 1)
            },
            "missing_skills": missing_skills,
            "sections_found": found_sections,
            "missing_sections": [s for s in ['Experience', 'Education', 'Skills', 'Projects'] if s not in found_sections],
            "suggestions": suggestions
        }

    else:
        # --- MODE 2: RESUME-ONLY QUALITY AUDIT ---
        
        # PILLAR 1: STRUCTURE (25 Points)
        struct_score = (len(found_sections) / 4.0) * 25
        if len(found_sections) < 4:
            missing = [s for s in ['Experience', 'Education', 'Skills', 'Projects'] if s not in found_sections]
            suggestions.append(f"Structure: missing {', '.join(missing)} sections.")

        # PILLAR 2: SKILLS STRENGTH (25 Points)
        resume_skills = [s for s in TECHNICAL_SKILLS_DB if s in clean_resume]
        skill_score = min(len(resume_skills) * 2.5, 25) 
        if len(resume_skills) < 6:
            suggestions.append("Skills: Increase technical keyword density.")

        # PILLAR 3: EXPERIENCE DEPTH (25 Points)
        impact_verbs = ['led', 'managed', 'developed', 'optimized', 'created', 'increased', 'reduced']
        verb_count = len([v for v in impact_verbs if v in clean_resume])
        has_metrics = len(re.findall(r'\d+%', resume_text)) > 0 or len(re.findall(r'\$\d+', resume_text)) > 0
        
        exp_score = min(verb_count * 3, 15) + (10 if has_metrics else 0)
        if not has_metrics:
            suggestions.append("Experience: Use numbers (%, $) to quantify achievements.")

        # PILLAR 4: ATS READABILITY (25 Points)
        word_count = len(resume_text.split())
        readability_score = 0
        if 400 <= word_count <= 800:
            readability_score = 25
        elif 200 <= word_count < 400:
            readability_score = 15
            suggestions.append("Readability: Content is thin. Expand your details.")
        else:
            readability_score = 10
            suggestions.append("Readability: Resume length is sub-optimal.")

        total_score = struct_score + skill_score + exp_score + readability_score

        return {
            "score": round(total_score, 1),
            "recommendation": "Professional" if total_score >= 75 else "Needs Polish",
            "match_details": None, 
            "breakdown": {
                "structure": round(struct_score, 1),
                "skills": round(skill_score, 1),
                "experience": round(exp_score, 1),
                "readability": round(readability_score, 1)
            },
            "suggestions": suggestions,
            "sections_found": found_sections,
            "missing_sections": [s for s in ['Experience', 'Education', 'Skills', 'Projects'] if s not in found_sections]
        }