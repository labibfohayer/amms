import openpyxl
import io

def generate_fee_report_excel(students_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fee Report"
    
    headers = ["Name", "Class", "Monthly Fee", "Months Paid", "Total Paid", "Total Due"]
    ws.append(headers)
    
    for item in students_data:
        ws.append([
            item.get('name'),
            item.get('class_name'),
            item.get('monthly_fee'),
            item.get('months_paid'),
            item.get('total_paid'),
            item.get('total_due')
        ])
    
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

def generate_attendance_report_excel(data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance Report"
    
    headers = ["Student Name", "Total Days", "Present", "Absent", "Late", "Leave"]
    ws.append(headers)
    
    for item in data:
        ws.append([
            item.get('name'),
            item.get('total'),
            item.get('present'),
            item.get('absent'),
            item.get('late'),
            item.get('leave')
        ])
        
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
