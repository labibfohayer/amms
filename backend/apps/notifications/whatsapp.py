import requests
import os

WHATSAPP_SERVICE_URL = os.getenv('WHATSAPP_SERVICE_URL', 'http://localhost:3001')

def send_whatsapp_message(phone: str, message: str) -> bool:
    try:
        formatted = f"880{phone[1:]}" if phone.startswith('0') else phone
        response = requests.post(
            f"{WHATSAPP_SERVICE_URL}/send",
            json={"phone": formatted, "message": message},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"WhatsApp send failed: {e}")
        return False

def send_admission_notification(student, password: str):
    message = (
        f"আস-সালামু আলাইকুম!\n\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\n"
        f"আপনার সন্তান *{student.name_bn or student.name}* এর ভর্তি সম্পন্ন হয়েছে।\n\n"
        f"*Student ID:* {student.student_id}\n"
        f"*Password:* {password}\n\n"
        f"এই ID ও Password দিয়ে App-এ Login করুন।\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(student.guardian_phone, message)

def send_absent_notification(student, date_str: str):
    message = (
        f"আস-সালামু আলাইকুম!\n\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\n"
        f"আজ *{date_str}* তারিখে আপনার সন্তান\n"
        f"*{student.name_bn or student.name}* মাদ্রাসায় অনুপস্থিত ছিলেন।\n\n"
        f"কোনো সমস্যা থাকলে মাদ্রাসায় যোগাযোগ করুন।\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(student.guardian_phone, message)

def send_fee_reminder(student, month_name: str, amount: float):
    message = (
        f"আস-সালামু আলাইকুম!\n\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\n"
        f"বিনীত স্মরণ করিয়ে দেওয়া যাচ্ছে যে,\n"
        f"*{student.name_bn or student.name}* এর *{month_name}* মাসের\n"
        f"বেতন *৳{amount}* এখনো পরিশোধিত হয়নি।\n\n"
        f"অনুগ্রহ করে দ্রুত পরিশোধ করুন।\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(student.guardian_phone, message)

def send_result_notification(student, exam_name: str, gpa: float):
    message = (
        f"আস-সালামু আলাইকুম!\n\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\n"
        f"*{student.name_bn or student.name}* এর\n"
        f"*{exam_name}* এর ফলাফল প্রকাশিত হয়েছে।\n\n"
        f"*GPA:* {gpa}\n\n"
        f"App-এ Login করে বিস্তারিত দেখুন।\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(student.guardian_phone, message)

def send_notice_broadcast(phones: list, title: str, body: str):
    message = (
        f"আস-সালামু আলাইকুম!\n\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\n"
        f"*📢 নোটিশ: {title}*\n\n"
        f"{body}\n\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    success_count = 0
    for phone in phones:
        if send_whatsapp_message(phone, message):
            success_count += 1
    return success_count

def send_teacher_credentials(teacher, password: str):
    message = (
        f"আস-সালামু আলাইকুম!\n\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\n"
        f"আপনার অ্যাকাউন্ট তৈরি হয়েছে।\n\n"
        f"*Teacher ID:* {teacher.teacher_id}\n"
        f"*Password:* {password}\n\n"
        f"এই ID ও Password দিয়ে App-এ Login করুন।\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(teacher.phone, message)
