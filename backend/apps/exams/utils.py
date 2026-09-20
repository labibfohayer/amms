from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

def generate_marksheet_pdf(student, exam, results):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.drawString(100, 800, "Al Madina Model Madrasah")
    if exam:
        p.drawString(100, 780, f"Exam: {exam.name}")
    if student:
        p.drawString(100, 760, f"Student: {student.name}")
    
    y = 720
    p.drawString(100, 740, "Subject | Marks | Grade | GPA")
    for r in results:
        p.drawString(100, y, f"{r.subject.name} | {r.marks_obtained} | {r.grade} | {r.gpa}")
        y -= 20
        
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()
