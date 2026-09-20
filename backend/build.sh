#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "from apps.accounts.models import User; User.objects.filter(phone='01700000000').exists() or User.objects.create_user(phone='01700000000', password='admin123', role='principal', name='Principal', name_bn='প্রিন্সিপাল', user_id='PRIN-001')"
