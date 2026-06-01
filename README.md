# First Endpoint FastAPI

A simple FastAPI application with user authentication, task management, and AI-based task suggestion.

## Features

- User signup and OAuth2 login with JWT bearer tokens
- Create, read, update, and delete tasks
- Protected endpoints with token authentication
- PostgreSQL database integration via SQLAlchemy
- Optional AI task suggestion endpoint using Google GenAI
- Docker and Docker Compose support for local deployment

## Requirements

- Python 3.13
- PostgreSQL
- Docker and Docker Compose (optional)

## Environment Variables

Create a `.env` file in the project root with:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi_db
API_KEY=<your_google_api_key>
```

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Run Locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

Build and run the app with Docker Compose:

```bash
docker compose up --build
```

This starts:

- `app` on port `8000`
- `postgres_db` on port `5432`

## Database

The app uses SQLAlchemy models defined in `models.py`.
The database connection is configured from `DATABASE_URL` in `database.py`.

## API Endpoints

### Public

- `GET /` - health check
- `POST /signup` - create a new user
- `POST /login` - obtain an access token

### Protected (Bearer token required)

Add the header:

```http
Authorization: Bearer <token>
```

- `GET /tasks` - list tasks for current user
- `POST /tasks` - create a new task
- `PUT /tasks/{id}` - update a task fully
- `PATCH /tasks/{id}` - update a task partially
- `DELETE /tasks/{id}` - delete a task
- `POST /tasks/suggest` - generate suggested tasks from a goal and store them

## Schemas

- `User`: `username`, `password`
- `Task`: `id`, `title`
- `Updt_Task`: optional `title`
- `GoalRequest`: `goal`
- `Token`: `access_token`, `token_type`

## Notes

- The login endpoint accepts OAuth2 password form data
- JWT tokens are generated with a 30-minute expiration
- AI suggestions use Google GenAI via `google.genai` in `ai.py`
- Database tables are created automatically by `Base.metadata.create_all(bind=engine)` in `models.py`
