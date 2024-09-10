from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import date

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="."), name="static")

class Space(BaseModel):
    id: int
    space_name: str
    space_description: Optional[str]
    capacity: int
    event_description: Optional[str]
    booking_date: Optional[date]
    time_slot: Optional[str]
    booking_status: Optional[str]

def get_db_connection():
    conn = sqlite3.connect('database_monty.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("webpage2.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/open-bookings", response_class=HTMLResponse)
async def open_bookings():
    with open("open_bookings.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/api/open-spaces", response_model=List[Space])
async def get_open_spaces():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM spaces 
        WHERE booking_status IS NULL OR booking_status != 'booked'
        ORDER BY booking_date, time_slot
    """)
    spaces = cursor.fetchall()
    conn.close()
    
    if not spaces:
        raise HTTPException(status_code=404, detail="No open spaces found")
    
    return [Space(**dict(space)) for space in spaces]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)