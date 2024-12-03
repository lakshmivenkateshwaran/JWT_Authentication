## Stock Market Analysis with JWT Authentication

This project demonstrates the use of FastAPI, Scrapy, and JWT for web scraping and secure user authentication. The system allows users to create accounts, log in, receive a JWT token, and use that token to initiate web scraping operations.

## Project Overview

This project is designed to:
- Create a user account with a secure password.
- Authenticate the user and issue a JWT token upon login.
- Use the JWT token to authorize and initiate web scraping tasks (using Scrapy).
- Scraped data is fetched from external websites and stored in a predefined repository (if not already present).

## Technologies Used

- FastAPI: A fast web framework for building APIs with Python.
- Scrapy: A web crawling framework used for extracting data from websites.
- SQLAlchemy: ORM for interacting with the database.
- JWT (JSON Web Token): For secure user authentication and authorization.
- PyMySQL: Used to interact with a MySQL database for storing user credentials and tokens.

## Installation

1. Clone the repository:
    ```
    git clone <repository_url>
    cd <repository_name>
    ```

2. Create and activate a virtual environment:
    ```
    python -m venv env
    source env/bin/activate   # For Windows, use: env\Scripts\activate
    ```

3. Install required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Setup

1. Ensure you have a MySQL database set up and accessible with the required credentials.

2. If you prefer using environment variables for configuration, create a `.env` file with the following contents:
    ```
    DATABASE_URL=mysql+pymysql://<username>:<password>@<host>/<database_name>
    SECRET_KEY=your_secret_key_here
    ```

    Replace `<username>`, `<password>`, `<host>`, and `<database_name>` with your MySQL credentials.

## Endpoints

1. **POST /create_user/**: This endpoint allows the creation of a new user.
   - **Request Body**:
     ```json
     {
       "username": "string",
       "password": "string"
     }
     ```
   - **Response**:
     ```json
     {
       "message": "User created successfully",
       "user": "string"
     }
     ```

2. **POST /token/**: This endpoint allows users to login and get an authentication token.
   - **Request Body**:
     ```json
     {
       "username": "string",
       "password": "string"
     }
     ```
   - **Response**:
     ```json
     {
       "access_token": "string",
       "token_type": "bearer"
     }
     ```

3. **GET /scrape/**: This endpoint triggers the scraping process, which scrapes documents from the ITC portal.
   - **Headers**:
     - `Authorization: Bearer <access_token>`
   - **Response**:
     ```json
     {
       "message": "Scraping started successfully"
     }
     ```

## Running the Application

1. Start the FastAPI server:
    ```
    uvicorn main:app --reload
    ```

2. Once the server is running, you can access the endpoints using Postman or any HTTP client.

## Notes

- JWT tokens expire after 30 minutes by default.
- Ensure your MySQL database is running and accessible.
- Scrapy will save the scraped files in a predefined directory if the file doesn't already exist.

## Troubleshooting

- No Files Downloaded: If you already have the files in the repository, Scrapy will mark them as uptodate and will not re-download them. This is to prevent duplicate downloads.
- Re-running Scraping: If you want to re-download the files, either remove the existing files manually from the repository or modify the Scrapy settings to ignore the uptodate status.