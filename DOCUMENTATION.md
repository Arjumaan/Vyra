# Vyra – Smart Personal Wealth Management Platform

**Vyra** is a centralized, highly-extensible personal finance and wealth management operating system built with Django. It is designed for complete financial consolidation—tracking every aspect of a user's financial life, from daily expenses and income to long-term wealth building, investments, debt management, and AI-driven insights.

## Project Scope & Architecture

### Core Principles
- **Monolithic Modularity:** Independent Django apps for distinct financial domains.
- **Data Integrity:** Fully normalized SQLite/PostgreSQL schema (Foreign Keys, Indexes, Validators).
- **No Duplication:** Single Source of Truth for transactions, assets, and liabilities.
- **Personalized:** Designed as a single-user or family-scale OS, focusing on completeness and feature-richness over multi-tenant SaaS scaling.

### System Modules

**1. Identity & Context**
- **Financial Profile:** Comprehensive profile (income, dependents, risk appetite, goals) serving as the baseline for AI recommendations.
- **Family Finance:** Relationship mapping, shared expenses, and split ownership.
- **Settings & Personalization:** Theme management, currency preferences, and security configurations.

**2. Core Finance & Banking**
- **Multi-Currency Engine:** Live and manual exchange rates, multi-currency assets/reports.
- **Bank & Cards:** Wallet, bank accounts, FD, RD, and credit cards.
- **Cash Flow & Budget:** Advanced daily/weekly/rolling budgets, spending heatmaps, and AI-generated budget suggestions.
- **Income & Expenses:** Daily transaction tracking with Receipt/OCR scanning support.

**3. Wealth & Asset Management**
- **Complete Asset Tracker:** Property, vehicles, electronics, digital assets, business ownership.
- **Investments:** Stocks, ETFs, Mutual Funds, Gold, Crypto.
- **Portfolio Analytics:** Allocation charts (asset, sector, risk), diversification scoring, and performance tracking.
- **Net Worth:** Real-time calculation and historical growth tracking.

**4. Liabilities & Commitments**
- **Debt Management:** Personal loans, EMIs, BNPL, outstanding payments.
- **Subscription Manager:** Tracking SaaS, streaming, and services with renewal reminders.
- **Insurance Portfolio:** Health, life, vehicle, property tracking with claim and nominee details.
- **Tax Center:** Income tax, GST, capital gains tracking, and yearly tax summaries.

**5. Planning & Forecasting**
- **Advanced Goal Planner:** Progress tracking, forecast completion, required monthly savings.
- **Retirement Planner:** Future value, inflation, and SIP calculators.
- **Emergency Fund Calculator:** Expense-based readiness scoring.
- **Expense Forecast:** ML-ready predictive cash flow analysis.

**6. AI & Automation**
- **AI Financial Coach:** Context-aware chat assistant utilizing user's financial data to answer questions and provide advice.
- **AI Monthly Reports:** Automated executive summaries, predictions, and strategy suggestions.
- **Document & Bill Scanners (OCR):** Auto-extraction of utility bills and receipts.

**7. Operations & Tools**
- **Financial Calendar:** Unified view of salaries, EMIs, bills, dividends, and renewals.
- **Notification Center:** Centralized alerts for budgets, loans, and goals.
- **Financial Journal:** Daily notes, mood tracking, and event timelines.
- **Document Vault:** Encrypted storage for PAN, Aadhaar, tax returns, and statements.
- **Security & Backup:** Login history, 2FA, manual/scheduled JSON/CSV database backups.
- **Reports Center:** PDF/Excel generation for income statements, cash flow, and tax reports.

## Tech Stack
- **Backend:** Python, Django 6.x
- **Frontend:** HTML5, CSS3 (Neumorphic Design System), Vanilla JS, Chart.js
- **Database:** SQLite (Dev) / PostgreSQL (Prod ready)
- **Deployment & DevOps:** Local environment optimized, ready for self-hosting.

## Coding Standards
- Strict PEP 8 compliance.
- Business logic encapsulated in `services.py` for complex apps.
- Comprehensive UI accessibility (Keyboard navigation, screen reader labels, high contrast support).

---
*Vyra is developed as the ultimate personal finance ecosystem, engineered for lifelong financial clarity and control.*
