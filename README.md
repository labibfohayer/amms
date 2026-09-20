# Al Modina Model Madrasah And Research Institute Management System (AMMS)

## Overview
A full-stack Progressive Web App (PWA) for managing the Al Modina Model Madrasah, featuring a Django backend, a Next.js frontend, and a Node.js WhatsApp microservice.

## Prerequisites
- Python 3.11+
- Node.js 18+

## Project Structure
- `/backend`: Django REST Framework API. Includes all modules for student, teacher, fee, exam, etc., management.
- `/frontend`: Next.js 14 frontend using Tailwind CSS.
- `/whatsapp-service`: Node.js express app using `whatsapp-web.js` to send WhatsApp notifications.

## Setup Instructions

### Backend (Django)
1. `cd backend`
2. Activate your virtual environment.
3. Install dependencies (if not already installed): `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Run the server: `python manage.py runserver`

### Frontend (Next.js)
1. `cd frontend`
2. Install dependencies: `npm install`
3. Run the dev server: `npm run dev`

### WhatsApp Service (Node.js)
1. `cd whatsapp-service`
2. Install dependencies: `npm install`
3. Run the service: `npm start`
4. Scan the generated QR code with the WhatsApp app (using the Madrasah's official number).
