# Bharat Shopee

## Overview

**Bharat Shopee** is an e-commerce platform designed to support local producers by providing a direct digital marketplace. By eliminating intermediaries, it reduces operational costs by 15% and promotes fair trade. The platform includes an admin dashboard for efficient management of items, sales, and customer details.

---

## Live Link & Resources

- **Live Link:**  [Click Here](https://django-mac-ecom-website.vercel.app/).
- **Demo Video:** [Click Here](https://drive.google.com/file/d/1jDZRwF0-iHomGfUy6U8ZpU8UUMWaGBtk/view)
- **GitHub Repository:** [Click Here](https://github.com/jaynandwana200/Django-MAC-Ecom-Website/tree/master/Django)

---

## Tech Stack

- **Backend Framework:** Django
- **Database:** PostgreSQL (hosted on AWS RDS)
- **Deployment:** Vercel
- **Frontend:** HTML, CSS, JavaScript

---

## Features

1. **Digital Marketplace:**
   - Direct platform for local producers to sell their goods.
   - Reduces middleman involvement, enhancing profitability.
2. **Admin Dashboard:**
   - Add, edit, and delete items.
   - Track and analyze sales.
   - Manage customer details.
3. **Optimized Data Flow:**
   - Advanced data modeling ensures seamless integration between components.
   - High performance for large datasets.

---

## Installation and Setup

### Prerequisites

- Python 3.9+
- PostgreSQL
- Virtual Environment (recommended)
- AWS account for RDS

### Steps

1. **Clone the repository:**
   ```bash
   git clone [Insert GitHub URL here]
   cd bharat-shopee
   ```
2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate   # For Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the database:**
   - Create a PostgreSQL database (hosted locally or on AWS RDS).
   - Update `settings.py` with your database credentials:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your_db_name',
             'USER': 'your_db_user',
             'PASSWORD': 'your_password',
             'HOST': 'your_db_host',
             'PORT': 'your_db_port',
         }
     }
     ```
5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Start the server:**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000` to view the application.

---

## Deployment

The application is deployed using **Vercel**. Follow these steps to deploy:

1. Connect your GitHub repository to Vercel.
2. Set environment variables for the Django project (e.g., `DATABASE_URL`, `SECRET_KEY`).
3. Push the code to the main branch. Vercel will automatically build and deploy the application.

---

## Contribution Guidelines

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a pull request.

---

## Acknowledgments

Special thanks to:

- Local producers for feedback on platform design.
- Django and PostgreSQL communities for robust documentation and support.

---


