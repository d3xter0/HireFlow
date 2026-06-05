# HireFlow Challenge

This repository contains the HireFlow recruitment platform challenge.

## Structure

- `challenge/` contains the Flask application.
- `tests/` contains verifier test scaffolding.
- `prompts/` contains the challenge prompt placeholder.
- `solution/` contains the solution patch placeholder.

## Setup

```bash
cd challenge
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py
python app.py
```

The application starts at `http://localhost:5000`.

Seeded users all use the password `Password123!`:

- `alice`
- `bob`
- `recruiter1`
- `admin`

## Run Tests

```bash
cd ../tests
bash test.sh
```

## Docker

```bash
cd challenge
docker compose up --build
```
