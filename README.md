# InventStarts AI Platform

A production-style AI backend built with FastAPI and Gemini.

## Current Features

- FastAPI backend
- Gemini AI integration
- Provider abstraction
- Provider factory
- Prompt manager
- Central logging
- Request correlation IDs
- Standard API response wrapper
- Global exception handling
- Custom validation responses
- Health endpoint
- Async AI requests
- Retry and timeout handling
- Automated tests with Pytest

## Tech Stack

- Python 3.12
- FastAPI
- Google Gemini
- Pydantic
- Pytest
- Tenacity

## Run Locally

```bash
conda activate mission-ai
uvicorn app.main:app --reload
## Automated Testing

The project includes automated tests for:

- Home endpoint
- Health endpoint
- Request validation
- Mocked AI chat responses

Tests run locally with Pytest and automatically through GitHub Actions.

```bash
pytest -v

## Architecture

Client → FastAPI Route → Service → Prompt Manager → Provider Interface → Gemini

## Conversation History

The platform now supports persistent conversation history using SQLAlchemy and SQLite.

### Features

- Create conversations
- Send messages to conversations
- Retrieve complete conversation history
- Async SQLAlchemy repository
- SQLite persistent storage
- Repository pattern
- 404 handling for unknown conversations
- Automated tests

🚀 Milestone: Database-Backed Conversation History

The conversation history module has been upgraded from an in-memory implementation to a persistent database-backed architecture using SQLAlchemy Async ORM and SQLite.

This milestone establishes the foundation for production-ready data persistence while keeping the application database-agnostic for an easy transition to PostgreSQL in the future.

✅ What Changed
Replaced the in-memory conversation repository with a SQLAlchemy-based repository.
Added persistent storage for conversations and conversation messages.
Implemented asynchronous database operations using AsyncSession.
Preserved the existing Repository Pattern and Service Layer architecture.
Kept API behavior unchanged while replacing the underlying storage implementation.
Maintained a clean separation of responsibilities:
models/ → SQLAlchemy ORM entities (database models)
schemas/ → Pydantic request/response DTOs (ViewModels)
repositories/ → Database access only
services/ → Business logic and mapping between ORM models and API schemas
🗄️ Database Architecture

Current database:

SQLite

Designed for future migration to:

PostgreSQL

Because the application is built on SQLAlchemy, changing the database backend will primarily require updating the connection string and running Alembic migrations, without changing the business logic.

📦 Technologies
FastAPI
SQLAlchemy 2.x (Async ORM)
SQLite
Alembic
Pydantic
AsyncIO
🧪 Testing

All automated tests continue to pass after the migration from in-memory storage to database persistence.

pytest -q

Current status:

7 passed
📈 Architecture
API
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
SQLAlchemy Async ORM
   │
   ▼
SQLite

This architecture follows production best practices by separating API contracts, business logic, and data access, making the platform maintainable, testable, and ready for future growth.
