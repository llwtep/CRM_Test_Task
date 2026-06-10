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

This project can be further enhanced in several directions to improve scalability, security, and maintainability:

- **Migration from integer IDs to UUIDs**  
  The current implementation uses auto-incrementing integer IDs for database tables. While this approach is sufficient for the current scope and simplifies testing and debugging, switching to UUIDs would improve security and reduce predictability of record identifiers in a production environment.

- **Asynchronous processing of AI operations**  
  AI-related requests could be moved to background jobs using a task queue system such as Celery. This would decouple heavy processing from the main request-response cycle, improving overall API responsiveness and system scalability.

- **Role-based authentication and authorization (RBAC)**  
  Introducing an authentication system with role-based permissions would allow finer control over access to CRM operations. Different roles (e.g., admin, teacher, manager) could have restricted or extended permissions depending on their responsibilities.

- **Caching layer for frequently accessed data**  
  Implementing caching (e.g., Redis) for high-frequency read operations such as attendance records and group-student relationships could significantly reduce database load and improve response times.

- **Dedicated read-only database user for AI services**  
  For improved security, a separate database user with read-only permissions could be created specifically for AI-related services. This would ensure that AI components cannot modify data and would reduce the potential impact of malicious or unintended operations.