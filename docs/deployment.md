# KitchenOS Deployment Guide

## Overview

KitchenOS is a Django-based cloud kitchen SaaS application. This guide explains how to run the application locally and how the current version is deployed on a Google Cloud Compute Engine virtual machine.

---

## Prerequisites

Install the following before running the project:

- Python 3
- pip
- Git
- Python virtual environment support

Check your Python version:

```bash
python --version
```

Check pip:

```bash
pip --version
```

---

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/Darshi-Jain/cloud-kitchen-saas.git
cd cloud-kitchen-saas
```

Replace the repository URL if your GitHub repository uses a different name.

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Linux or macOS:

```bash
source venv/bin/activate
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Apply database migrations

```bash
python manage.py migrate
```

Verify migrations:

```bash
python manage.py showmigrations
```

---

### 5. Run Django checks

```bash
python manage.py check
```

Expected output:

```text
System check identified no issues (0 silenced).
```

---

### 6. Start the development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

---

## Google Cloud Deployment

The current portfolio deployment runs on a Google Cloud Compute Engine virtual machine.

### Deployment flow

```text
User Browser
      |
      v
Google Cloud Compute Engine VM
      |
      v
Ubuntu Linux
      |
      v
Python Virtual Environment
      |
      v
Django Application
      |
      v
SQLite Database
      |
      v
WhiteNoise Static File Serving
```

---

## Running on the Cloud VM

Connect to the virtual machine and move to the project directory:

```bash
cd ~/cloud-kitchen-saas
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the application:

```bash
python manage.py runserver 0.0.0.0:8001
```

The application can then be accessed using the virtual machine's external IP address:

```text
http://<EXTERNAL_IP>:8001/
```

---

## Firewall Configuration

The Google Cloud firewall must allow inbound traffic on port `8001`.

The firewall rule should permit:

```text
Protocol: TCP
Port: 8001
Source: 0.0.0.0/0
```

For a production environment, access should be restricted and routed through HTTPS.

---

## Static Files

KitchenOS uses WhiteNoise to serve static files.

Static files include:

- CSS
- JavaScript
- Bootstrap assets
- Images
- Icons

Collect static files using:

```bash
python manage.py collectstatic
```

WhiteNoise middleware must remain enabled in `backend/settings.py`.

---

## Environment Configuration

Sensitive values should not be hard-coded in the repository.

Recommended environment variables include:

```text
SECRET_KEY
DEBUG
ALLOWED_HOSTS
DATABASE_URL
```

A production `.env` file should not be committed to GitHub.

Example `.gitignore` entry:

```text
.env
```

---

## Production Recommendations

The current deployment is suitable for portfolio demonstration. A production deployment should use:

- Gunicorn as the application server
- Nginx as a reverse proxy
- PostgreSQL as the database
- HTTPS with SSL certificates
- Environment-based secrets
- Centralized logging
- Automated backups
- CI/CD deployment
- Role-based access control

Recommended production flow:

```text
User
  |
  v
HTTPS
  |
  v
Nginx
  |
  v
Gunicorn
  |
  v
Django
  |
  v
PostgreSQL
```

---

## Useful Deployment Commands

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run checks:

```bash
python manage.py check
```

Apply migrations:

```bash
python manage.py migrate
```

Collect static files:

```bash
python manage.py collectstatic --noinput
```

Start the server:

```bash
python manage.py runserver 0.0.0.0:8001
```

Stop a running Django development server:

```bash
pkill -f "manage.py runserver"
```

Restart the server:

```bash
pkill -f "manage.py runserver"
python manage.py runserver 0.0.0.0:8001
```

---

## Troubleshooting

### Port already in use

```bash
pkill -f "manage.py runserver"
```

Then restart the server.

---

### Static files are missing

Run:

```bash
python manage.py collectstatic --noinput
```

Then restart the server.

---

### Migration errors

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Django configuration errors

Run:

```bash
python manage.py check
```

Review the displayed traceback and fix the referenced file.

---

## Future Deployment Enhancements

Planned improvements include:

- Docker containerization
- PostgreSQL migration
- Gunicorn deployment
- Nginx reverse proxy
- HTTPS configuration
- GitHub Actions CI/CD
- Automated database backups
- Application monitoring
- Centralized error logging

