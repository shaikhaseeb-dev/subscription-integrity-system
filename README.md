# Subscription Integrity System

## Overview

A full-stack system to manage subscriptions, simulate billing cycles, and prevent financial leakage from recurring payments.

## Tech Stack

- Backend: Flask (Python)
- Frontend: React
- Database: SQLite
- Testing: Pytest (33 test cases)

## Key Features

- Add and manage subscriptions
- Monthly cost and annual projections
- Upcoming billing (next 7 days)
- Billing simulation engine
- Billing history tracking

## Architecture

- Modular Flask backend using blueprints
- Service layer for business logic
- React frontend with centralized API client

## Correctness & Safety

- Prevents duplicate subscriptions
- Ensures billing idempotency
- Validates input data (cost, date, cycle)
- Handles edge cases (future dates, invalid inputs)

## Testing

- 33 unit tests using pytest
- Covers billing logic, validation, and summaries

## AI Usage

- AI used for scaffolding and structure
- All generated code manually reviewed and verified
- Tests used to ensure correctness

## Tradeoffs

- Uses SQLite (not production scale)
- No authentication (single-user system)
- No background job scheduler

## Future Improvements

- Add authentication
- Move to PostgreSQL
- Add async billing jobs
- Deploy to cloud

## How to Run

### Backend

cd backend  
python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt  
python app.py

### Frontend

cd frontend  
npm install  
npm start
