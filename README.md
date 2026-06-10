# Educational CRM Backend

A professional, asynchronous FastAPI-based backend system designed to manage training center operations, including teachers, students, groups, attendance tracking, and AI-driven data analysis.

## Description
This project provides a robust RESTful API for managing educational center workflows. It solves the problem of manual administrative data management by providing structured CRUD operations and intelligent, LLM-based querying capabilities to derive insights from the CRM database.

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL (with `asyncpg`)
- **Caching/Queuing:** Redis
- **ORM:** SQLAlchemy (Async)
- **Validation:** Pydantic v2
- **Dependency Management:** `uv`
- **Deployment:** Docker & Docker Compose

## Features
- **Teacher Management:** Full CRUD operations for teachers.
- **Student Management:** Full CRUD operations for students.
- **Group Management:** Organization of students and teachers into active, planning, frozen, or completed groups.
- **Group Student Enrollment:** Managing student associations with groups.
- **Attendance Tracking:** Daily attendance recording and management.
- **AI-Powered Analytics:** Query the CRM database using natural language via Groq/LLM integration.
- **System Health:** Monitoring endpoint for infrastructure status.

## Installation & Setup

### Local Setup
1. **Prerequisites:** Ensure `uv` is installed.
2. **Install dependencies:**
   ```bash
   uv sync
   ```
3. **Environment Variables:** Copy `.env.example` to `.env` and fill in the required values.
4. **Database Migrations:**
   ```bash
   uv run alembic upgrade head
   ```
5. **Start server:**
   ```bash
   uv run uvicorn main:app --reload
   ```

### Docker Setup
1. Ensure Docker and Docker Compose are installed.
2. Build and run the project:
   ```bash
   docker compose up -d --build
   ```
3. The API will be available at `http://localhost:8000`.

## Environment Variables
- `DATABASE_URL`: Connection string for PostgreSQL (e.g., `postgresql+asyncpg://user:pass@host:5432/db`)
- `REDIS_HOST`: Redis server hostname
- `REDIS_PORT`: Redis server port
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name
- `GROQ_API_KEY`: API key for Groq AI integration

## API Documentation
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

## Future Improvements

- This section is reserved for future enhancements
