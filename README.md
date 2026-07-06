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

## Database

The project uses:

- SQLAlchemy 2.x async ORM
- SQLite for local development
- Alembic for database schema migrations