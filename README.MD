# FastAPI Server

A lightweight FastAPI server boilerplate designed for scalability, maintainability, and extensibility. This base setup provides a clean foundation to build APIs and web applications.

---

## Overview

This project serves as a starter template for FastAPI-based server applications. It includes:
- A modular project structure.
- Middleware for common functionalities.
- Separate routes for API endpoints and web pages.
- A customizable, extensible setup for developers.
- Hot reloading using Arel for seamless development experience.

---

## Features

- **FastAPI Framework**: A high-performance, easy-to-use framework for building APIs and web applications.
- **Middleware**:
  - **GZip Compression**: Optimizes responses for faster delivery.
  - **Authorization Middleware**: Creates a guest cookie, the value is just a string of text──it is not attached to a session.
  - **No-Cache Middleware**: Ensures fresh data by disabling client-side caching.
  - **CORS**: CORS configuration is set up, but currently doesn't have any restrictions.
- **Hot Reloading**: Leveraging Arel, changes made to files in the `resources` and `public` directories automatically refresh the browser.
- **Environment Configuration**: Simplified management of environment variables via `.env`.
- **Scalable Structure**: Organized directory layout to support future growth and enhancements.

---

## Project Structure

```
fastapi_server/
├── app/
│   ├── controllers/          # Handles business logic and route controllers
│   ├── lib/                  # Utility classes and helpers
│   ├── routes/               # API route definitions
│   └── __init__.py           # Application module initializer
├── public/                   # Static assets (CSS, JS, images, etc.)
├── resources/                # Templates or other project resources
├── main.py                   # Main entry point for the application
├── .env                      # Environment variables configuration
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Getting Started

### Prerequisites

- **Python**: Version `3.12.6` or higher
- **pip**: Version `24.3.1` or higher

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BradleyParkerDev/fastapi_server.git
   cd fastapi_server
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   ```bash
   source ./venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate     # Windows
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   - Create a `.env` file based on `example.env`.
   ```bash
   cp example.env .env
   ```

---

## Scripts

### Start the Server
To start the FastAPI server:
```bash
python main.py
```

By default, the server runs at `http://127.0.0.1:5001`.

---

## Development Notes

### Routes
- **API Routes**: Defined in `app/routes/users_routes.py` for user-related API endpoints.
- **Web Routes**: Defined in `app/routes/web_routes.py` for rendering web pages using templates.

### Middleware
Custom middleware can be found in `main.py`:
- **Authorization Middleware**: Intended purpose is to manage the user's session.
- **No-Cache Middleware**: Disables browser caching.

### Hot Reloading with Arel
- **Hot Reload**: Using Arel, any changes made to files in the `resources` and `public` directories automatically trigger a browser refresh.
- **WebSocket Setup**: A WebSocket route is included in `main.py` to support hot reloading.

### Installed Packages
- The only two packages that were explicitly installed for this project were **`FastAPI`** and **`Arel`**.
- All of the other packages that are listed in the `requirements.txt` were automatically downloaded as dependencies for these two packages.

---

## Requirements

Below are the primary dependencies:
- **FastAPI**: The core framework for APIs.
- **Jinja2**: Template rendering for web routes.
- **Uvicorn**: ASGI server for FastAPI.
- **Python-Dotenv**: Environment variable management.
- **Starlette**: Provides foundational ASGI support.
- **AnyIO**: Manages asynchronous operations.
- **Arel**: Enables hot reloading for improved development workflow.

See `requirements.txt` for the full list of dependencies.

---

## License

This project is open for personal and educational use. No specific license applies.
