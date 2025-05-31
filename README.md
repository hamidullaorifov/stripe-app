# Stripe Payment app

Stripe payment application with checkout session and payment intent for items and orders

Demo : [https://effective-mobile.duckdns.org/](https://sripe-app-django.duckdns.org/)  \
*The demo is hosted on AWS EC2 instance*

## Features

- Product catalog with multiple currencies (USD, EUR)
- Stripe Checkout and Payment Intent integration
- Order management system
- Discount and tax calculation
- Admin dashboard for managing products/orders


## Technology Stack

- Backend: Django
- Frontend: HTML 5, CSS, Bootstrap, Django templates, JQuery
- Deployment: AWS EC2, Nginx, Gunicorn

## Prerequisites

- Python 3.9+
- Git
- Stripe account
- Docker (optional)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/hamidullaorifov/stripe-app.git
cd stripe-app
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
Create a .env file in the project root:
```dotenv
SECRET_KEY=your-django-secret-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-public-key
```

### 5. For new database remove db.sqlite3 file and Run Migrations
```bash
python manage.py migrate
```

## 7. Run Development Server
### Option 1
```bash
python manage.py runserver
```
### Option 2 (Docker)
```bash
docker build -t my-django-app .
docker run -p 8000:8000 my-django-app
```
The application will be available at http://localhost:8000
