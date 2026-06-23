# Subscription Integrity System

A full-stack web application that helps users track recurring subscriptions, monitor upcoming charges, simulate billing cycles, and gain better visibility into their monthly spending.

## Overview

Subscription services have become a part of everyday life. From streaming platforms and cloud storage to productivity tools and software subscriptions, it is easy to lose track of recurring payments over time.

The Subscription Integrity System was built to address this problem by providing a centralized platform where users can manage subscriptions, monitor upcoming billing events, and understand their recurring expenses before charges occur.

The application combines a React frontend with a Flask backend and includes a billing simulation engine, validation mechanisms, and automated tests to ensure correctness and reliability.

---

## Live Demo

**Frontend:** https://subscription-integrity-system.vercel.app

**Backend API:** https://subscription-integrity-system.onrender.com

**Health Check:** https://subscription-integrity-system.onrender.com/health

---

## Features

### Subscription Management

* Add new subscriptions
* View all active subscriptions
* Store billing cycle information
* Track upcoming payment dates

### Upcoming Billing Detection

* Displays subscriptions due within the next 7 days
* Helps users prepare for upcoming charges
* Improves visibility into recurring expenses

### Monthly Cost Summary

* Calculates total recurring monthly cost
* Provides a quick overview of subscription spending

### Billing Simulation Engine

* Processes subscriptions due for billing
* Creates billing history records
* Automatically updates the next billing date
* Maintains billing consistency

### Billing History Tracking

* Records billing events
* Enables auditing of processed charges
* Provides historical visibility

### Validation & Error Handling

* Prevents invalid inputs
* Rejects negative subscription costs
* Validates billing dates
* Validates billing cycles
* Handles malformed requests gracefully

### Automated Testing

* 33 unit tests implemented using Pytest
* Covers billing logic, validation, summaries, and edge cases

---

## Tech Stack

### Frontend

* React
* JavaScript
* CSS

### Backend

* Flask
* Flask-CORS
* Flask-SQLAlchemy

### Database

* SQLite

### Testing

* Pytest
* Pytest-Flask

### Deployment

* Vercel (Frontend)
* Render (Backend)

---

## Project Architecture

```text
React Frontend
      │
      ▼
REST API Requests
      │
      ▼
Flask Backend
      │
      ▼
Service Layer
      │
      ▼
SQLAlchemy ORM
      │
      ▼
SQLite Database
```

The backend follows a modular architecture with separate layers for:

* Routes
* Services
* Validation
* Database Models

This structure improves maintainability, scalability, and code organization.

---

## API Endpoints

### Health Check

```http
GET /health
```

### Subscriptions

```http
GET /subscriptions
POST /subscriptions
GET /subscriptions/upcoming
```

### Billing

```http
POST /billing/run
GET /billing/events
```

### Summary

```http
GET /summary/monthly-cost
```

---

## Running Locally

### Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

Backend runs at:

```text
http://127.0.0.1:5000
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm start
```

Frontend runs at:

```text
http://localhost:3000
```

---

## Testing

Run backend tests:

```bash
cd backend

pytest
```

The project includes 33 automated test cases covering:

* Subscription creation
* Validation logic
* Billing engine functionality
* Monthly cost calculations
* Edge cases and error handling

---

## Key Design Considerations

### Duplicate Prevention

The system prevents duplicate subscription records from being created unintentionally.

### Billing Integrity

Billing operations are designed to be idempotent, ensuring that subscriptions are not processed multiple times for the same billing period.

### Validation First

All incoming data is validated before reaching the database, reducing the risk of inconsistent or invalid records.

### Modular Architecture

Business logic is separated from route handlers, making the codebase easier to maintain and extend.

---

## Challenges Solved

During development and deployment, several practical challenges were addressed:

* Designing a reliable billing simulation engine
* Implementing validation and duplicate prevention
* Managing cross-origin communication between frontend and backend
* Deploying a React frontend on Vercel
* Deploying a Flask backend on Render
* Debugging production CORS issues
* Configuring environment variables for deployment

---

## Future Improvements

The current version focuses on core subscription management functionality. Future enhancements could include:

### Authentication & Authorization

* User registration and login
* JWT-based authentication
* Password hashing and account security
* Role-based access control

### Notifications & Reminders

* Email reminders before billing dates
* Push notifications
* Upcoming payment alerts
* Weekly subscription summaries

### Database Improvements

* Migration from SQLite to PostgreSQL
* Database migrations using Alembic
* Improved scalability and reliability

### Background Processing

* Scheduled billing jobs
* Automated subscription checks
* Task queues using Celery or APScheduler

### Analytics Dashboard

* Monthly spending trends
* Subscription category analysis
* Cost forecasting
* Visual reports and charts

### Multi-User Support

* Individual user accounts
* User-specific subscription data
* Personalized dashboards

### Cloud & DevOps

* Docker containerization
* CI/CD pipelines
* Cloud-native deployment
* Monitoring and logging

### Subscription Enhancements

* Subscription categories
* Currency support
* Annual billing support
* Subscription cancellation tracking
* Budget recommendations

---

## Learning Outcomes

This project helped strengthen practical skills in:

* Full-stack development
* REST API design
* Database modeling
* Software architecture
* Automated testing
* Production deployment
* Debugging real-world issues
* Cross-origin communication (CORS)
* Environment configuration

---

## Author

**Shaik Abdul Haseeb**

Computer Science Engineering Student

Passionate about Software Development, Data Science, Artificial Intelligence, and building practical solutions to real-world problems.
