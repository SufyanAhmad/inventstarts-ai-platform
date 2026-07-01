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