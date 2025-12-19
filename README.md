# Cars Dealership - Full-Stack Application

## Project Overview
Cars Dealership is a comprehensive full-stack web application built for a national car retailer in the United States. This application enables users to browse dealership locations, view dealer information, and submit reviews with sentiment analysis.

## Features
- Browse car dealerships across different states
- User registration and authentication
- Post and view dealership reviews
- Sentiment analysis on reviews
- Admin panel for data management
- Responsive UI design
- RESTful API architecture

## Technology Stack
- **Frontend**: React.js
- **Backend**: Django REST Framework
- **Database**: SQLite
- **Sentiment Analysis**: Flask microservice
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: IBM Cloud Code Engine

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- Docker (optional)

### Backend Setup
```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd server/frontend
npm install
npm start
```

### Sentiment Analysis Service
```bash
cd server/sentiment_analyzer
pip install -r requirements.txt
python app.py
```

## API Endpoints
- `/djangoapp/get_dealers/` - Get all dealers
- `/djangoapp/get_dealers/:state` - Get dealers by state
- `/djangoapp/dealer/:id` - Get dealer by ID
- `/djangoapp/reviews/dealer/:id` - Get reviews for a dealer
- `/djangoapp/add_review` - Add a new review
- `/djangoapp/login` - User login
- `/djangoapp/logout` - User logout
- `/djangoapp/register` - User registration

## Author
Full-Stack Developer - IBM Capstone Project

## License
MIT License
