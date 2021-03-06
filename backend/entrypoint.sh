#!/usr/bin/env bash
#
#echo "*************** creating database ****************"
#alembic create schema vmi_db if not exists

echo "_______________running autogenerate_______________"
alembic revision --autogenerate -m "Added command table"

echo "_______________executing migrations_______________"
alembic upgrade head

echo "_______________running fastapi_______________"
uvicorn backend.web.main:app --host 0.0.0.0 --port 5000 --reload