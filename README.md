# Sentiment-Analysis-using-LLM

Certainly! Here's a `README.md` file description for your project. This document will provide an overview of the project, instructions for setting up the environment, usage, and additional information about the API.

### `README.md`

```markdown
# Sentiment Analysis API

This project is a Python-based web application that processes customer reviews using a sentiment analysis model. It allows users to upload a `.csv` or `.xlsx` file containing customer reviews, performs sentiment analysis using the Groq API, and returns structured results in a JSON format. The application is built using Django, Django REST Framework, and includes a user-friendly frontend for file uploads and result visualization.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)


## Features
- Upload `.csv` or `.xlsx` files containing customer reviews.
- Integrate with the Groq API for sentiment analysis.
- Returns structured JSON responses with positive, negative, and neutral sentiment scores.
- Stores the response in a JSON file with the same name as the input file.
- Provides a web-based interface for file uploads and results display.
- Handles API rate limits with retry mechanisms.

## Project Structure
```
sentiment_analysis_project/
├── manage.py
├── sentiment_analysis_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
├── reviews_api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   ├── index.html
│   ├── migrations/
│   │   └── __init__.py
└── env/ (Your virtual environment)
```

## Requirements
- Python 3.8+
- Django 4.2+
- Django REST Framework
- `pandas` for file processing
- `groq` library for integrating with the Groq API
- `fpdf` (optional, for generating PDF documentation)
- `openpyxl` for processing `.xlsx` files
- A valid Groq API key

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sentiment-analysis-api.git
   cd sentiment-analysis-api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variable for the Groq API key:**
   - On Windows:
     ```bash
     set GROQ_API_KEY=your_api_key
     ```
   - On macOS/Linux:
     ```bash
     export GROQ_API_KEY=your_api_key
     ```

5. **Run the migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Open your web browser and go to `http://127.0.0.1:8000/api/`.

## Usage
1. **Upload a File:**
   - On the web interface, use the "Upload CSV/XLSX File" button to upload your customer review file.
   - Click "Upload and Analyze" to process the file and view the sentiment analysis results.

2. **API Usage:**
   - Send a POST request to the `/api/upload/` endpoint with a `.csv` or `.xlsx` file using tools like `curl` or Postman.
   - Example using `curl`:
     ```bash
     curl -X POST -F "file=@path/to/customer_reviews.csv" http://127.0.0.1:8000/api/upload/
     ```

3. **Output:**
   - The sentiment analysis results are displayed on the frontend.
   - A JSON file with the same name as the uploaded file is saved in the `uploads` directory.

## API Endpoints
- **`POST /api/upload/`**: Accepts a `.csv` or `.xlsx` file, processes the reviews for sentiment analysis, and returns a structured JSON response.
- **`GET /api/`**: Displays the web interface for file uploads.

## Error Handling
- Provides error messages for:
  - Unsupported file formats
  - Missing or invalid "Review" column in the uploaded file
  - API errors and rate limits (includes retry mechanisms)
- Alerts are shown on the frontend for any errors during file upload or processing.


