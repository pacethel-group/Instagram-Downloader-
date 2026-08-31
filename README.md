InstaFetch

Instagram Video, Reels, Stories & Photo Downloader

InstaFetch is a simple web application designed to help users retrieve and download publicly accessible Instagram media.

Features

- Instagram video downloader
- Reels downloader
- Public Stories downloader
- Photo downloader
- Carousel media support
- Mobile-friendly interface
- No user account required
- Fast and simple interface

Project Structure

instagram-downloader/
│
├── index.html
│
└── backend/
    ├── app.py
    ├── requirements.txt
    └── .env.example

Frontend

The frontend is contained in one file:

index.html

It contains:

- HTML
- CSS
- JavaScript

Backend

The backend uses:

- Python
- Flask
- Flask-CORS

Main API:

POST /api/instagram/fetch

Health check:

GET /api/health

How It Works

1. User copies an Instagram URL.
2. User pastes the URL into InstaFetch.
3. The frontend sends the URL to the Flask API.
4. The backend validates the URL.
5. The backend identifies the content type.
6. A public-content retrieval provider processes the request.
7. Available media information is returned to the frontend.
8. The user can download available media.

Supported URL Types

Examples include:

Instagram Reels
Instagram Posts
Instagram Videos
Public Instagram Stories
Instagram Photos
Instagram Carousels

Important

InstaFetch is intended for publicly accessible content.

It does not bypass:

- Private accounts
- Instagram login requirements
- Access controls
- DRM
- Security mechanisms
- Rate limits

Users are responsible for ensuring that they have the right to download and use the content they retrieve.

Development

Clone the repository:

git clone YOUR_REPOSITORY_URL

Enter the project:

cd instagram-downloader

Install backend dependencies:

cd backend
pip install -r requirements.txt

Start the Flask server:

python app.py

The API will run locally on:

http://localhost:5000

Status

Current version: 1.0.0

The frontend and Flask API foundation are complete.

The public-content retrieval provider still needs to be connected.

License

This project is provided for development and educational purposes.# Instagram-Downloader-
