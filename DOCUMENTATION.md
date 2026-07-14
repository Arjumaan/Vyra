# Vyra - Smart Personal Expense Tracker

## Project Abstract
Vyra is a web-based personal finance management application designed to help users track their income, monitor expenses, set budgets, and gain valuable financial insights. By leveraging interactive visualizations and an AI-inspired rule-based insight engine, it promotes financial awareness and smart money management.

## Problem Statement
Many individuals struggle to keep track of their daily expenses and monthly budgets, leading to poor financial decisions and a lack of savings. Traditional methods of tracking expenses are tedious and lack actionable insights. Vyra solves this by providing a unified, automated, and intelligent platform for managing personal finances.

## Objectives
- To develop a secure and user-friendly web application for personal finance management.
- To provide categorized tracking of income and expenses.
- To enable users to set and monitor monthly budgets.
- To generate visual reports using Chart.js for better data comprehension.
- To offer AI-powered financial insights and recommendations based on user spending habits.

## Scope
The system allows registered users to log their financial transactions, categorize their spending, view interactive dashboard summaries, set budgets, and read dynamically generated financial insights. The application is tailored for students, employees, and freelancers.

## Technology Stack
- **Backend:** Python, Django 6.0
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
- **Visualizations:** Chart.js

## System Architecture
The application follows the traditional Model-View-Template (MVT) architecture of Django. 
- **Models:** Define the database schema (Income, Expense, Category, Budget).
- **Views:** Handle the business logic and user requests.
- **Templates:** Render the frontend using Bootstrap 5.

## Database Schema (ER Diagram Logic)
- **User:** Manages authentication.
- **Income:** (id, user_id, amount, source, date, notes)
- **Expense:** (id, user_id, category_id, amount, date, description)
- **Category:** (id, user_id, category_name)
- **Budget:** (id, user_id, monthly_budget, month, year)

All modules (Income, Expense, Category, Budget) have a ForeignKey relationship with the User model to ensure data privacy and separation.

## Data Flow Diagram (DFD) - High Level
1. User logs in/registers.
2. User navigates to Dashboard to see summary.
3. User adds Income/Expense -> Database updates.
4. User sets Budget -> Database updates.
5. System calculates totals, remaining budget, and savings -> Displayed on Dashboard and Reports.
6. System analyzes data -> Generates AI Insights.

## Features Implemented
1. **Authentication:** Register, Login, Logout with secure password hashing.
2. **Dashboard:** Summary of Total Income, Total Expenses, Balance, Savings, and Budget Usage.
3. **Income Management:** CRUD operations for income records.
4. **Expense Management:** CRUD operations for expenses with custom categories.
5. **Budget Management:** Monthly budget tracking with progress indicators.
6. **Reports:** Visual breakdown of expenses using Pie charts and summary statistics.
7. **AI Insights:** Intelligent, rule-based alerts and tips on spending habits (e.g., budget exceeded warnings, top category alerts).

## Future Enhancements
- Integration with OpenAI/Gemini for advanced natural language insights.
- Export reports to PDF/Excel.
- Receipt scanner using OCR.
- Multi-currency support.

## User Manual
1. Setup a virtual environment: `python -m venv venv`
2. Activate it and install Django: `pip install django`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the server: `python manage.py runserver`
6. Access the app at `http://127.0.0.1:8000/`

---
*Developed as a college mini-project demonstrating modern web development practices.*
