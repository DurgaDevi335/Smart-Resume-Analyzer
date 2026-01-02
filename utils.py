import os
from fpdf import FPDF
import fitz

def extract_text_from_pdf(path):
    text = ""
    try:
        doc = fitz.open(path)
        for page in doc: text += page.get_text()
        doc.close()
    except: pass
    return text

import os
from werkzeug.utils import secure_filename

def save_upload(file, folder):
    # 1. Check if the file actually exists
    if not file or file.filename == '':
        return None
    
    # 2. Check extension (Fixes the Google Drive generic MIME type issue)
    allowed_ext = file.filename.lower().endswith('.pdf')
    if not allowed_ext:
        return None

    # 3. Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # 4. Clean the filename (removes spaces/special characters)
    # This is very important for Linux servers like Render
    filename = secure_filename(file.filename)
    path = os.path.join(folder, filename)
    
    # 5. Save the file
    file.save(path)
    return path

def generate_resume_pdf(data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Clean non-latin-1 characters
        def clean(t):
            if not t: return ""
            return t.replace('•', '-').replace('–', '-').encode('latin-1', 'ignore').decode('latin-1')

        # Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, clean(data.get('full_name', 'Resume')).upper(), ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, clean(f"{data.get('email')} | {data.get('phone')} | {data.get('location')}"), ln=True, align='C')
        pdf.ln(8)

        def add_formatted_section(title, key):
            content = data.get(key)
            if content and content.strip():
                pdf.set_font("Arial", 'B', 11)
                pdf.set_fill_color(245, 245, 245)
                pdf.cell(0, 7, title, ln=True, fill=True)
                pdf.ln(2)
                
                pdf.set_font("Arial", '', 10)
                lines = content.split('\n')
                for line in lines:
                    c_line = clean(line.strip())
                    if not c_line:
                        pdf.ln(2) # Handles double enter spacing
                        continue
                    
                    if c_line.startswith('-') or c_line.startswith('*'):
                        pdf.set_x(15) # Indent bullets
                    else:
                        pdf.set_x(10)
                    pdf.multi_cell(0, 5, c_line)
                pdf.ln(4)

        sections = [
            ("PROFESSIONAL SUMMARY", 'summary'), ("WORK EXPERIENCE", 'experience'),
            ("PROJECTS", 'projects'), ("EDUCATION", 'education'),
            ("TECHNICAL SKILLS", 'skills'), ("CERTIFICATIONS", 'certifications'),
            ("ACHIEVEMENTS", 'achievements')
        ]
        for t, k in sections: add_formatted_section(t, k)

        pdf.output(file_path)
        return True
    except Exception as e:
        print(f"Error: {e}")

        return False
