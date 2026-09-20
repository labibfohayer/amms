import os
import subprocess
import sys

BASE_DIR = r"C:\Users\assdi\.gemini\antigravity\scratch\amms\backend"
PYTHON_EXE = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")

apps = [
    "accounts",
    "students",
    "teachers",
    "academic",
    "attendance",
    "fees",
    "exams",
    "library",
    "hostel",
    "notices",
    "reports",
]

apps_dir = os.path.join(BASE_DIR, "apps")
if not os.path.exists(apps_dir):
    os.makedirs(apps_dir)
    with open(os.path.join(apps_dir, "__init__.py"), "w") as f:
        pass

for app in apps:
    app_path = os.path.join(apps_dir, app)
    if not os.path.exists(app_path):
        subprocess.run([PYTHON_EXE, "manage.py", "startapp", app, app_path], cwd=BASE_DIR)
        
print("Apps created successfully!")
