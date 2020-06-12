# FridayNight

## Setup

1. `python -m venv venv`

1. `source venv/bin/activate`

1. `venv/bin/pip install -e . -r requirements.txt -r requirements-dev.txt`

<!-- 1. `pip install -r requirements-dev.txt` -->

## Database
Create the db from scratch from current migrations or run a new migration

1. `venv/bin/alembic upgrade head`

Auto-generate an alembic migration from a model

1. `venv/bin/alembic revision --autogenerate -m "Added accounts table"`

## Test

1. `venv/bin/pytest tests [-s, -k]`

#### With coverage reports

1. `venv/bin/coverage run -m pytest tests`

1. Use `venv/bin/coverage report` to report on the results (or `coverage html` and open in browser)

## Run

1. `venv/bin/gunicorn --reload "friday_night.app:get_app()"`
