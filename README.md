# Todo_List_API_Auth_Django

A Django REST Framework API for managing a personal to-do list with JWT-based user authentication, backed by a MySQL database.

## How It Works

```
Request → DRF View → JWT Auth Check → Serializer Validation → Django ORM → MySQL
                                                                               ├── Success → Serialized JSON Response
                                                                               └── Error   → DRF Error Response
```

- All users and todos are stored in a **MySQL database**
- Authentication is handled using **JWT tokens** via `djangorestframework-simplejwt`
- Each todo is tied to its owner — users can only access and modify **their own todos**
- Input validation is handled by **DRF Serializers**, which return structured error messages automatically
- Supports **pagination** on the todo list endpoint

## Prerequisites

- Python 3.8+
- MySQL server running locally
- [uv](https://github.com/astral-sh/uv) package manager

## Setup

**1. Clone the repo**
```bash
git clone <your-repo-url>
cd Todo_List_API_Auth_Django
```

**2. Create and activate a virtual environment using uv**
```bash
uv venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
uv add django djangorestframework mysqlclient djangorestframework-simplejwt
```

**4. Set up the database**

Open MySQL Workbench or your MySQL client and run:
```sql
CREATE DATABASE django_todo_api;
```

Django's ORM will handle creating the tables automatically via migrations.

**5. Configure database credentials**

Open `core/settings.py` and update the `DATABASES` section:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_todo_api',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
```

**6. Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**7. Run the app**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## Authentication

This API uses **JWT (JSON Web Tokens)**. After registering or logging in, you will receive an access token. Include it in the header of every protected request:

```
Authorization: Bearer <your_access_token>
```

Access tokens are short-lived. Use the refresh token to obtain a new one without logging in again.

## API Endpoints

### Register
```
POST /register/
```
**Body:**
```json
{
    "username": "johndoe",
    "email": "john@doe.com",
    "password": "password123"
}
```
**Response `201 Created`:**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Login
```
POST /login/
```
**Body:**
```json
{
    "username": "johndoe",
    "password": "password123"
}
```
**Response `200 OK`:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Get All Todos
```
GET /todos/?page=1&limit=10
```
Requires authentication. Returns only the todos belonging to the logged-in user.

**Response `200 OK`:**
```json
{
    "data": [
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Buy milk, eggs, and bread"
        }
    ],
    "page": 1,
    "limit": 10,
    "total": 1
}
```

---

### Get a Single Todo
```
GET /todos/<id>/
```
**Response `200 OK`:** Single todo or `404 Not Found`

---

### Create a Todo
```
POST /todos/
```
**Body:**
```json
{
    "title": "Buy groceries",
    "description": "Buy milk, eggs, and bread"
}
```
**Response `201 Created`:**
```json
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Buy milk, eggs, and bread"
}
```

---

### Update a Todo
```
PUT /todos/<id>/
```
**Body:** Same as Create Todo

**Response `200 OK`:** Updated todo or `403 Forbidden` if not the owner

---

### Delete a Todo
```
DELETE /todos/<id>/
```
**Response `204 No Content`** or `403 Forbidden` if not the owner

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK — request succeeded |
| 201 | Created — resource successfully created |
| 204 | No Content — resource successfully deleted |
| 400 | Bad Request — missing or invalid fields |
| 401 | Unauthorized — missing or invalid token |
| 403 | Forbidden — you do not own this resource |
| 404 | Not Found — resource does not exist |

## Project Structure

```
Todo_List_API_Auth_Django/
├── core/                          # Django project config
│   ├── settings.py                # Project settings (database, installed apps, JWT)
│   ├── urls.py                    # Root URL configuration
│   └── wsgi.py
├── users/                         # Users app
│   ├── serializers.py             # Registration serializer with validation
│   ├── views.py                   # Register view
│   └── urls.py                    # /register and /login routes
├── todos/                         # Todos app
│   ├── models.py                  # Todo model and database schema
│   ├── serializers.py             # DRF serializer for todos
│   ├── views.py                   # API views (CRUD logic)
│   └── urls.py                    # Todos URL patterns
├── manage.py                      # Django management CLI
├── pyproject.toml                 # Project dependencies (managed by uv)
└── uv.lock                        # Locked dependency versions
```