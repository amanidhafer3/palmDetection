# Dockerfile
FROM python:3.11-slim

# منع الإخراج المؤقت
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تثبيت بعض الأدوات للنشر والبناء
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# ننسخ بقية الكود
COPY . .

# نجمع static وقت البناء (يمكن أيضًا في خطوة إطلاق)
RUN python manage.py collectstatic --noinput

# منفذ التطبيق
EXPOSE 8080

# أمر التشغيل عبر gunicorn
CMD ["gunicorn", "palmDetection.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]
