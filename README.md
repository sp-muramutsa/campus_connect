# Campus Connect

This document outlines the architecture, setup instructions, and security measures implemented in the `campus_connect` Django web application.

## 1. File Structure Description

This project uses a standard Django layout, organized around the top-level project directory (`campus_backend`) and the primary application (`api`).

| Directory / File | Type | Purpose |
| :--- | :--- | :--- |
| **Project Root** | |
| `manage.py` | Command Line Utility | The primary interface for interacting with Django. |
| `requirements.txt` | Text File | Lists all required Python packages. |
| `build.sh` | Shell Script | Script executed by Render for setup (installs, migrations, superuser creation). |
| `db.sqlite3` | Database File | SQLite database file (used for local development). |
| **`campus_backend/`** | **Project Configuration** | **The main Django project folder containing global settings.** |
| &nbsp;&nbsp;&nbsp;`__init__.py` | Python Module | Initialization file. |
| &nbsp;&nbsp;&nbsp;`asgi.py` | Python Module | Entry point for ASGI servers (Asynchronous operations). |
| &nbsp;&nbsp;&nbsp;`settings.py` | Python Module | Global configuration (Database, Security, Installed Apps, Environment checks). |
| &nbsp;&nbsp;&nbsp;`urls.py` | Python Module | The master URL configuration, directing traffic to app-level URLs. |
| &nbsp;&nbsp;&nbsp;`wsgi.py` | Python Module | Entry point for WSGI servers (Synchronous operations, e.g., Gunicorn). |
| **`api/`** | **App Directory** | **Contains the core logic for the "Events" feature and other APIs.** |
| &nbsp;&nbsp;&nbsp;`__init__.py` | Python Module | Initialization file. |
| &nbsp;&nbsp;&nbsp;`admin.py` | Python Module | Configuration for displaying models in the Django Admin. |
| &nbsp;&nbsp;&nbsp;`apps.py` | Python Module | Application configuration. |
| &nbsp;&nbsp;&nbsp;`migrations/` | Directory | Stores database schema changes. |
| &nbsp;&nbsp;&nbsp;`models.py` | Python Module | Defines the data structure (e.g., the `Event` model). |
| &nbsp;&nbsp;&nbsp;`tests.py` | Python Module | Contains tests for the API app. |
| &nbsp;&nbsp;&nbsp;`urls.py` | Python Module | App-level URL routing. |
| &nbsp;&nbsp;&nbsp;`views.py` | Python Module | Contains the business logic (view functions). |
| **`static/`** | **Static Assets** | **Used for collecting and serving static files (CSS, images).** |
| &nbsp;&nbsp;&nbsp;`images/` | Directory | Stores images used on the site. |
| &nbsp;&nbsp;&nbsp;`styles.css` | CSS File | Core cascading style sheets. |
| **`templates/`** | **HTML Templates** | **Stores all HTML files rendered by Django views.** |
| &nbsp;&nbsp;&nbsp;`base.html` | HTML Template | The base layout for the entire site. |
| &nbsp;&nbsp;&nbsp;`index.html` | HTML Template | The homepage view. |
| &nbsp;&nbsp;&nbsp;`login.html` | HTML Template | User login page. |
| &nbsp;&nbsp;&nbsp;`register.html` | HTML Template | User registration page. |
| &nbsp;&nbsp;&nbsp;`profile.html` | HTML Template | User profile page. |
| &nbsp;&nbsp;&nbsp;... (other html) | HTML Templates | Templates for various app sections (events, groups, contact, etc.). |
| `venv/` | Directory | Python virtual environment (ignored in production). |

## 2. Instructions on How to Open/Run the Web Application

### Local Development Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/sp-muramutsa/campus_connect](https://github.com/sp-muramutsa/campus_connect)
    cd campus_connect
    ```
2.  **Setup Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scripts\activate   # Windows
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Database Setup:** Create the tables and an administrator user.
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```
5.  **Run Server:**
    ```bash
    python manage.py runserver
    ```
    The application will be accessible at `http://127.0.0.1:8000/`.

### Production Deployment (Render)

The application is deployed to Render.com and is accessible at:
[https://campus-connect-ue58.onrender.com](https://campus-connect-ue58.onrender.com)

Deployment is **automatic** upon every push to the `main` branch.

## 3. Known Issues/Limitations

* **Free Tier Shell Restriction:** Interactive shell access (`python manage.py shell`) is disabled on the Free Tier, requiring administrative commands (like superuser creation) to be automated within the `build.sh` script.
* **Cold Start Latency:** As a Free Tier web service, the application will spin down after 15 minutes of inactivity, causing a delay for the first request (50 seconds or more).
* **Missing Data:** The database is currently empty and requires data entry via the Admin panel.

## 4. Future Improvements

* Implement user registration, login, and profile management for public users.
* Develop a full API using Django REST Framework for mobile/external client consumption of Event data.
* Add filtering and search functionality to the main Event list.
* Implement comprehensive Unit and Integration tests.

---

## 5. Site Map & Backend Routing

### Backend Routing Overview

Routes are handled by the master URL dispatcher, directing traffic to the appropriate application views.

| Method | Path | Handled By | Purpose |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | `api.views.home` | Fetches and renders all events on the main homepage. |
| **GET/POST** | `/admin/` | `django.contrib.admin.urls` | Handles Admin Login, Dashboard, and CRUD operations for models. |

### Site Map (User Navigation)

The primary user flow is simple, focusing on the main list and administrative access.

1.  **Public User:** `https://campus-connect-ue58.onrender.com/` (Homepage)
2.  **Administrator:**
    * Navigate to: `/admin/`
    * Authenticate with Superuser credentials.
    * Manage data (Events, Users) from the Admin Dashboard.

---

## 6. Security Measures Implemented

The application relies on Django's built-in security features, enforced by configuration.

| Technique | Description | Security Measure Used |
| :--- | :--- | :--- |
| **1. Cross-Site Request Forgery (CSRF) Protection** | Mitigates unauthorized command submissions from other websites. | **`CsrfViewMiddleware`** and the `{% csrf_token %}` template tag are mandatory for all internal POST forms (e.g., Admin login). |
| **2. SQL Injection Protection** | Prevents malicious SQL code from being executed in the database. | All database interactions use the **Django ORM** (`Event.objects.all()`), which automatically escapes user input and uses parameterized queries. |
| **3. HTTPS and Secure Cookies** | Encrypts all data transmission and ensures session integrity. | **Render enforced HTTPS/SSL** is used in production, and `CSRF_COOKIE_SECURE = True` and `SESSION_COOKIE_SECURE = True` are set in `settings.py`. |

### Authentication Flow Explanation

The application uses Django's **Session Authentication** system for all internal logins (Admin):

1.  **Credential Check:** Credentials submitted via the Admin form are checked by Django's `authenticate()` backend.
2.  **Session Creation:** Upon successful login, a unique **Session ID** is generated and linked to the user.
3.  **Cookie Delivery:** The Session ID is sent back to the browser in a secure `sessionid` HTTP cookie.
4.  **Authorization:** For subsequent requests, the browser sends the `sessionid` cookie, which Django validates against the database to confirm the user's identity and permissions.
