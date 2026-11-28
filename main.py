import sqlite3
from contextlib import closing
from pathlib import Path

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()
DB_PATH = Path(__file__).with_name("leads.db")


class LeadCreate(BaseModel):
    name: str
    message: str


@app.post("/leads", status_code=status.HTTP_201_CREATED)
def create_lead(lead: LeadCreate):
    with closing(sqlite3.connect(DB_PATH)) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        cursor = db.execute(
            "INSERT INTO leads (name, message) VALUES (?, ?)",
            (lead.name, lead.message),
        )
        db.commit()
        return {"id": cursor.lastrowid}