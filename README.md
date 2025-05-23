# Personalized News Aggregator

A Django-based web application that allows users to register, select topics of interest, and see a personalized news feed.

## Features

- User authentication (register, login, logout)
- Topic management (add, view, remove topics)
- Personalized news feed based on user's topics
- News fetching from external APIs (currently simulated for testing)

## Setup

1. Clone this repository
2. Make sure Python 3.8+ is installed
3. Run the setup script:

```
python setup.py
```

This will:
- Create a virtual environment
- Install dependencies
- Apply database migrations
- Run tests to ensure everything is working

## Run the Application

Activate the virtual environment and start the development server:

```
# Windows
.venv\Scripts\activate
python manage.py runserver

# macOS/Linux
source .venv/bin/activate
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser to use the application.

## Project Structure

- `accounts/` - User authentication functionality
- `news/` - Topic management and news aggregation
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and other static files

## Testing

Run the test suite:

```
python manage.py test
```

## API Key Configuration

To fetch real news data, you need to set the `NEWS_API_KEY` environment variable:

```
# Windows
set NEWS_API_KEY=your_api_key_here

# macOS/Linux
export NEWS_API_KEY=your_api_key_here
```