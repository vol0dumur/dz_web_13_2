# FROM python:3.11-slim

# WORKDIR /app

# COPY ./quotes/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.11-slim

WORKDIR /app

# Встановлення netcat
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY ./quotes/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 8000

CMD ["sh", "-c", "/wait-for-it.sh db 5432 && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
