from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import uvicorn

# Create FastAPI app
app = FastAPI()

# Allow CORS (similar to Flask-CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### BELOW IS THE COMMENTED GLOBAL STATEMENTS ###

#DATABASE = 'database_monty.db'
# Connect to SQLite database (or create it if it doesn't exist)
#conn = sqlite3.connect('database_monty.db')

# Create a cursor object to execute SQL commands
#cursor = conn.cursor()


# Example function to execute an SQLite statement
def execute_sql(statement, values=None):
   # DATABASE = 'database_monty.db'
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('database_monty.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    try:
        if values:
            cursor.execute(statement, values)
        else:
            cursor.execute(statement)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error executing SQL: {e}")
    cursor.close()
    conn.close()


# Example to create a table
# create_table_sql = '''
# CREATE TABLE IF NOT EXISTS database_monty (
#    id INTEGER PRIMARY KEY AUTOINCREMENT, 
#    space_name TEXT NOT NULL UNIQUE, 
#    space_description TEXT, 
#    capacity INTEGER NOT NULL, 
#    event_description TEXT, 
#    booking_date DATE, 
#    time_slot TEXT, 
#    booking_status TEXT
# );
# '''

# conn.commit()
# cursor.execute("SELECT * FROM database_monty")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)


# Define request body model using Pydantic
class BookingData(BaseModel):
    time_slot: str
    classrooms: list[str]
    purpose: str


# API route to handle booking data
@app.post("/book")
async def book_space(data: BookingData):
   # DATABASE = 'database_monty.db'
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('database_monty.db')

    # Create a cursor object to execute SQL commands
    # cursor = conn.cursor()
    # Log the data to the console
    print("Booking Details Received:")
    print(f"Time Slot: {data.time_slot}")
    print(f"Classroom: {data.classrooms}")
    print(f"Purpose: {data.purpose}")

    # Send back the booking details as a response (to display on the webpage)
    response_data = {
        "message": "Booking received successfully!",
        "time_slot": data.time_slot,
        "classroom": data.classrooms,
        "purpose": data.purpose
    }
    conn.close()
    return response_data


########### checking db for available classrooms to display when a timeslot is selected ##########


def available_classrooms(time_slot):
   # DATABASE = 'database_monty.db'
    # Connect to SQLite database (or create it if it doesn't exist)
   # conn = sqlite3.connect('database_monty.db')

    # Create a cursor object to execute SQL commands

    conn = sqlite3.connect('database_monty.db')

    cursor = conn.cursor()

    table_contents = cursor.execute('SELECT * FROM spaces').fetchall()
    for row in table_contents:
        print(row)
    #conn = sqlite3.connect(DATABASE)
    #cursor = conn.cursor()

    # Query to get available classrooms for the selected time slot
    cursor.execute("""
        SELECT space_name FROM spaces
        WHERE time_slot = ? AND booking_status = 'Available'
    """, (time_slot,))

    available_classrooms = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return available_classrooms


# API route to get available classrooms for the selected time slot
# @app.get("/available_classrooms/{time_slot}")
# async def available_classrooms(time_slot: str):
#     print('available_classrooms called')
#     DATABASE = 'database_monty.db'
#
#     # Connect to SQLite database
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#
#     # Query to get available classrooms for the selected time slot
#     cursor.execute("""
#             SELECT space_name FROM database_monty
#             WHERE time_slot = ? AND booking_status = 'Open'
#         """, (time_slot,))
#
#     available_classrooms = [row[0] for row in cursor.fetchall()]
#
#     # Print available classrooms
#     print(f'Available classrooms for time_slot "{time_slot}": {available_classrooms}')
#
#     conn.close()
#
#     return {"available_classrooms": available_classrooms}

# THIS IS WITH THE 'WITH CLOSING' CONSTRUCT TO PREVENT DATA LEAKAGE
from contextlib import closing


@app.get("/available_classrooms/{time_slot}")
async def available_classrooms(time_slot: str):
    conn = sqlite3.connect('database_monty.db')
    print('available_classrooms called')
    # DATABASE = 'database_monty.db'

    # Use a context manager for the database connection

    print('connected to database')
    testing_conn = conn.execute("""SELECT * from spaces;""").fetchall()
    print(testing_conn)
    # Use closing to ensure the cursor is closed properly
    with closing(conn.cursor()) as cursor:
        print('inside with closing statement')
        # Query to get available classrooms for the selected time slot
        cursor.execute("""
            SELECT space_name FROM spaces
            WHERE time_slot = ? AND booking_status = 'Open';
        """, (time_slot,))
        print('executed')
        available_classrooms = [row[0] for row in cursor.fetchall()]

        # Print available classrooms
        print(f'Available classrooms for time_slot "{time_slot}": {available_classrooms}')
    conn.close()

    return {"available_classrooms": available_classrooms}


# Run the server (can use uvicorn to run)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
