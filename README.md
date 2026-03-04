# FastAPI Todo - Level 7

## 1) Chay local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

## 2) Chay test

```bash
pytest -q
```

`tests/conftest.py` dung SQLite test rieng (`test_todo.db`) va override `get_db`, khong dung DB production.

## 3) Chay docker

```bash
docker compose up --build
```

- API: `http://localhost:8000`
- Postgres: `localhost:5432`

`docker-compose.yml` truyen `DATABASE_URL` de app dung Postgres.
