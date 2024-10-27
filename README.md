# FastAPI CRUD App

## Overview

This FastAPI CRUD application is designed to provide a foundational structure for building RESTful APIs with a modern backend stack. The app includes essential CRUD functionality (Create, Read, Update, Delete) with a PostgreSQL database, SQLAlchemy for ORM, and Alembic for database migrations. The project is intended for use as an API-only backend, without any server-rendered HTML templates.

## Features

- **`FastAPI Framework`**: Utilized for fast, asynchronous web API development.
- **`CRUD Operations`**: Full support for Create, Read, Update, and Delete operations on database entities.
- **`Database`**: PostgreSQL as the main database, managed via SQLAlchemy ORM.
- **`Migrations`**: Alembic for handling database migrations and schema versioning.
- **`Authentication`**: Session based authentication with JSON Web Tokens and HTTP only cookies. Tracks guest and authenticated user sessions.
- **`Middleware`**:

    - GZip Compression: GZip middleware enabled for optimized API responses.
    - Authorization Middleware: Checks session cookie and gives authorization to authenticated users. Also creates guest sessions for non authenticated users, feature could be used in a cart system. 
    - No-Cache Middleware: Ensures API responses are not cached on the client side, always delivering fresh data.

- **`Environment Configuration`**: .env support for easy environment variable management.
- **`Scalable Project Structure`**: Well-organized directory structure for easy project scalability and maintenance.

## Project Structure

```

fastapi_crud_app/
│
├── app/
│   ├── controllers/          # Business logic and CRUD operations
│   ├── database/             # Database configuration and models
│   │   ├── db.py             # Database initialization
│   │   └── migrations/       # Alembic migrations folder
│   ├── lib/                  # Utility classes (e.g., authentication)
│   ├── models/               # SQLAlchemy ORM models
│   ├── routes/               # API route definitions
│   └── __init__.py           # Application module initializer
│
├── main.py                   # Main entry point of the application
├── .env                      # Environment variables configuration
├── alembic.ini               # Alembic configuration file
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

```

## Getting Started

### Prerequisites

- Python (3.12.6 or higher)
- pip (24.2 or higher)

### Installation

1. **Clone the repository and `cd` into `fastapi_crud_app` :**

    ```sh
    git clone https://github.com/BradleyParkerDev/fastapi_crud_app.git
    cd fastapi_crud_app
    ```

2. **Rename `example.env` to `.env` and add your desired environment variables:**

   ```bash
   mv example.env .env
   ```


3. **Create a virtual envirionment:**

   ```bash
   python -m venv venv
   ```


4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```


5. **Generate your first database migration:**

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

6. **Upgrade the database with the migration:**

   ```bash
   alembic upgrade head
   ```

## Scripts

**`Start the server` :**

   ```bash
   python main.py
   ```

## Packages

This project leverages a variety of libraries and tools to handle different aspects of API development, database management, security, and more. Below is an overview of each installed package:

- **Alembic** (`alembic==1.13.3`): Handles database migrations, allowing you to version control schema changes with ease.

- **Annotated Types** (`annotated-types==0.7.0`): Provides additional type annotations for strict data validation.

- **AnyIO** (`anyio==4.6.2.post1`): An asynchronous library used by Starlette for high-level networking and concurrency.

- **bcrypt** (`bcrypt==4.2.0`): Used for hashing passwords, providing secure storage of sensitive data.

- **Certifi** (`certifi==2024.8.30`): Ensures that secure SSL certificates are used in HTTP requests.

- **Click** (`click==8.1.7`): A package used for handling command-line interfaces, primarily for the FastAPI CLI.

- **dnspython** (`dnspython==2.7.0`): A library for DNS handling, used by `email_validator` for validating domain names in emails.

- **Email Validator** (`email_validator==2.2.0`): Validates email addresses, commonly used in user registration and authentication.

- **FastAPI** (`fastapi==0.115.3`): The main web framework used for building the API, offering high performance and ease of use.

- **FastAPI CLI** (`fastapi-cli==0.0.5`): Provides additional command-line tools for managing FastAPI projects.

- **Greenlet** (`greenlet==3.1.1`): Used as a dependency for SQLAlchemy to handle concurrency with green threads.

- **Httpcore** (`httpcore==1.0.6`) and **Httpx** (`httpx==0.27.2`): Both libraries are used for making HTTP requests, often to external APIs or microservices.

- **httptools** (`httptools==0.6.4`): A dependency for Uvicorn, helping with HTTP parsing.

- **idna** (`idna==3.10`): Supports the Internationalized Domain Names in Applications (IDNA) standard, enhancing DNS compatibility.

- **Jinja2** (`Jinja2==3.1.4`): A templating engine used within FastAPI for rendering HTML templates if needed (though this project is API-only).

- **Mako** (`Mako==1.3.6`): A dependency for Alembic to generate migration scripts.

- **Markdown-It-Py** (`markdown-it-py==3.0.0`): Parses Markdown content, useful if your project needs to render or transform Markdown files.

- **Psycopg2-Binary** (`psycopg2-binary==2.9.10`): A PostgreSQL adapter for Python, allowing SQLAlchemy to interact with PostgreSQL databases.

- **Pydantic** (`pydantic==2.9.2`): Provides data validation and settings management using Python type annotations, heavily utilized in FastAPI for request and response models.

- **Pygments** (`Pygments==2.18.0`): Used for syntax highlighting in documentation and logging output.

- **Python Dotenv** (`python-dotenv==1.0.1`): Loads environment variables from a `.env` file, useful for managing secrets and configuration settings.

- **Python Multipart** (`python-multipart==0.0.12`): Allows handling of `multipart/form-data`, typically used in file upload endpoints.

- **PyYAML** (`PyYAML==6.0.2`): Used to read and write YAML files, a common format for configuration files.

- **Rich** (`rich==13.9.3`): Provides beautiful console output, enhancing readability of logs and debugging information.

- **Shellingham** (`shellingham==1.5.4`): Detects the shell in use, used by CLI tools like Typer.

- **Sniffio** (`sniffio==1.3.1`): Helps with context-based concurrency detection, assisting async frameworks like AnyIO.

- **SQLAlchemy** (`SQLAlchemy==2.0.36`): The ORM used to interact with PostgreSQL, allowing for Pythonic manipulation of database records.

- **Starlette** (`starlette==0.41.0`): A lightweight ASGI framework that powers FastAPI’s core functionality, handling routing, sessions, and more.

- **Typer** (`typer==0.12.5`): A modern command-line interface library, simplifying argument parsing and command creation.

- **Typing Extensions** (`typing_extensions==4.12.2`): Adds backported features from newer versions of Python's `typing` module, enabling forward compatibility.

- **Uvicorn** (`uvicorn==0.32.0`): An ASGI server used to serve the FastAPI application, allowing for asynchronous handling of requests.

- **Uvloop** (`uvloop==0.21.0`): An alternative event loop for asyncio, speeding up request handling for FastAPI applications.

- **Watchfiles** (`watchfiles==0.24.0`): Monitors file changes, often used in development for auto-reloading applications.

- **Websockets** (`websockets==13.1`): Allows WebSocket support in ASGI applications, although not actively used if this project is purely API-focused.

## License

None.
