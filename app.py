import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Import project-specific modules
from config import Config
from database import db, User, History
from ml_logic import calculate_ats_score
from utils import extract_text_from_pdf, save_upload, generate_resume_pdf

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Plugins
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# --- 1. AUTHENTICATION ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        new_user = User(username=request.form['username'], email=request.form['email'], password=hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Username or Email already exists.', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid login credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear() 
    return redirect(url_for('login'))

# --- 2. DASHBOARD & HISTORY ---

@app.route('/dashboard')
@login_required
def dashboard():
    user_history = History.query.filter_by(user_id=current_user.id).order_by(History.date.desc()).all()
    latest = History.query.filter_by(user_id=current_user.id).order_by(History.date.desc()).first()
    return render_template('dashboard.html', 
                           history=user_history[:5], 
                           total_scans=len(user_history),
                           latest_score=latest.score if latest else 0)

@app.route('/history')
@login_required
def history():
    all_history = History.query.filter_by(user_id=current_user.id).order_by(History.date.desc()).all()
    return render_template('history.html', history=all_history)

@app.route('/delete-history/<int:id>', methods=['POST'])
@login_required
def delete_history(id):
    entry = History.query.get_or_404(id)
    if entry.user_id == current_user.id:
        db.session.delete(entry)
        db.session.commit()
        flash("Record deleted successfully.", "success")
    return redirect(url_for('history'))

# --- 3. ANALYSIS & REPORTING ---

@app.route('/analyze')
@login_required
def analyze():
    return render_template('analyze.html')

@app.route('/process_analysis', methods=['POST'])
@login_required
def process_analysis():
    file = request.files.get('resume_file')
    jd_text = request.form.get('job_description', '')
    
    file_path = save_upload(file, app.config['UPLOAD_FOLDER'])
    if not file_path:
        flash('Upload a valid PDF resume.', 'danger')
        return redirect(url_for('analyze'))
    
    resume_text = extract_text_from_pdf(file_path)
    results = calculate_ats_score(resume_text, jd_text if jd_text.strip() else None)
    
    # Store results in session for the Chatbot to access
    session['last_results'] = results
    
    new_entry = History(
        job_title=jd_text[:50] if jd_text else "General Assessment",
        score=results['score'],
        full_report_json=json.dumps(results),
        user_id=current_user.id
    )
    db.session.add(new_entry)
    db.session.commit()
    
    return render_template('report.html', results=results)

@app.route('/report/<int:report_id>')
@login_required
def view_report(report_id):
    report_entry = History.query.get_or_404(report_id)
    if report_entry.user_id != current_user.id:
        return redirect(url_for('dashboard'))
    
    results = json.loads(report_entry.full_report_json)
    session['last_results'] = results 
    return render_template('report.html', results=results)

# --- 4. RESUME BUILDER ---

@app.route('/builder')
@login_required
def builder():
    return render_template('builder.html')

@app.route('/generate_resume', methods=['POST'])
@login_required
def generate_resume():
    data = request.form.to_dict()
    filename = f"builder_{current_user.username}.pdf"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if generate_resume_pdf(data, file_path):
        return send_file(file_path, as_attachment=True)
    
    flash('Error generating PDF.', 'danger')
    return redirect(url_for('builder'))

# --- 5. SMART CHATBOT API ---

@app.route('/get_chat_response', methods=['POST'])
@login_required
def chatbot_response():
    data = request.get_json()
    user_msg = data.get("message", "").lower()
    results = session.get('last_results', {})
    
    if not results:
        return jsonify({"response": "Analysis data missing. Please scan your resume again."})

    missing_skills = results.get('missing_skills', [])
    missing_sections = results.get('missing_sections', [])
    score = results.get('score', 0)

    # Question 1: Top 3 Fixes
    if "top 3" in user_msg:
        tips = []
        if missing_skills: tips.append(f"Add Skills: {', '.join(missing_skills[:2])}")
        if missing_sections: tips.append(f"Add Section: {missing_sections[0]}")
        tips.append("Include more numbers and metrics.")
        return jsonify({"response": "🔑 **Top Fixes:** " + " | ".join(tips)})

    # Question 2: Weakest Area
    elif "weakest" in user_msg:
        if missing_sections:
            return jsonify({"response": "Your **Structure** is the weakest point. Standard headings were not detected."})
        return jsonify({"response": "Your **Keyword Match** is the weakest point. Your skills don't fully match the Job Description."})

    # Question 3: Metrics
    elif "metrics" in user_msg:
        return jsonify({"response": "Try this: 'Improved revenue by 20% by implementing X'. Use percentages and currency signs!"})

    # Question 4: Tailoring
    elif "tailor" in user_msg:
        if missing_skills:
            return jsonify({"response": f"Focus on adding **{', '.join(missing_skills[:3])}** to your Bullet Points."})
        return jsonify({"response": "Your keywords match well! Focus on mirroring the action verbs used in the JD."})

    # Question 5: Summary Tips
    elif "summary" in user_msg:
        return jsonify({"response": "Keep it short. Mention: [Job Title] + [Top Skill] + [Biggest Accomplishment]."})

    # Question 6: Layout Safety
    elif "layout" in user_msg:
        return jsonify({"response": "Stick to a single-column layout. Avoid images, charts, and tables inside the resume."})

    return jsonify({"response": "I'm ready! Select a topic above."})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)