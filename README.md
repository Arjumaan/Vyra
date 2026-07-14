# Vyra - Smart Personal Expense Tracker

Vyra is a web-based personal finance management application designed to help users track their income, monitor expenses, set budgets, and gain valuable financial insights. Developed using Django 6.0 and Bootstrap 5.

## Features
- **User Authentication:** Secure registration and login.
- **Dashboard:** At-a-glance summary of income, expenses, savings, and budget usage.
- **Income & Expense Tracking:** Add, edit, delete, and categorize your transactions.
- **Budget Management:** Set monthly budget limits and track your progress.
- **Reports:** Visual insights into your spending habits with Chart.js pie and line charts.
- **AI-Powered Insights:** Rule-based smart insights and alerts on your financial health.

## Installation & Setup

1. **Clone or Extract the Project**
2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```
3. **Activate the Virtual Environment:**
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. **Install Requirements:**
   ```bash
   pip install django
   ```
5. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```
6. **Create a Superuser (Optional, for Admin Access):**
   ```bash
   python manage.py createsuperuser
   ```
7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
8. **Access the Application:** Open your browser and go to `http://127.0.0.1:8000`

## Documentation
Full project documentation (including architecture, DFD, schemas, etc.) is available in the generated artifacts.

---
*Developed as a college mini-project.*
