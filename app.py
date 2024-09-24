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

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database_monty.db')
    conn.row_factory = sqlite3.Row
    return conn

# Serve root HTML
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("webpage2.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

# Serve closed bookings HTML
@app.get("/closed-bookings", response_class=HTMLResponse)
async def closed_bookings():
    with open("closed_bookings.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)


# API endpoint for closed spaces
@app.get("/api/closed-spaces", response_model=List[Space])
async def get_closed_spaces():
    conn = get_db_connection(database_monty)
    cursor = conn.cursor()
    
    # Query to retrieve closed bookings (spaces that have been booked)
    cursor.execute("""
        SELECT * FROM spaces 
        WHERE booking_status = 'booked'
        ORDER BY booking_date, time_slot
    """)
    
    spaces = cursor.fetchall()
    conn.close()
    
    if not spaces:
        raise HTTPException(status_code=404, detail="No closed bookings found")
    
    return [Space(**dict(space)) for space in spaces]

# Main function for running the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
