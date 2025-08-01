import sqlite3
import hashlib


def calculate_md5(text):
    return hashlib.md5(text.encode()).hexdigest()


# Connect to the SQLite database
connection = sqlite3.connect('old_approach/Database/AccountSystem.db')
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS AccountDB(ID INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, Email TEXT, Password TEXT, Type TEXT,UniID TEXT, Sign_MD5 TEXT,  Ratings REAL DEFAULT 0.4)")
cur.execute("""
    CREATE TABLE IF NOT EXISTS DriverDetails (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        User_ID TEXT NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        seats INTEGER NOT NULL,
        Booked_seats INTEGER NOT NULL,
        departure_time TIME NOT NULL,
        fair INTEGER NOT NULL
    )
""")

# Create the table if it doesn't exist

# Example user ID and password
email = "k214771@nu.edu.pk"
password = "fast123"
# Extract UniID
uni_id = email.split('@')[0]

role = "Passenger"
uni_id = email.split('@')[0]
hashed_password = calculate_md5(password)
Signature_md5 = calculate_md5(uni_id + password + role)

# Insert sample data into the table
cur.execute("INSERT INTO AccountDB (FirstName, LastName, Email, Password, Type, UniID, Sign_MD5,Ratings) VALUES (?, ?, ?, ?, ?, ?, ?,?)",
            ("mehdi", "badami", email, hashed_password, "Passenger", uni_id, Signature_md5,0.4))

# Sample data for the new driver
first_name = "Shah"
last_name = "Muhammad"
email = "k213557@nu.edu.pk"
password = "fast123"  # You should hash this password
role = "Driver"
ratings = 0.4
role = "Driver"
uni_id = email.split('@')[0]
hashed_password = calculate_md5(password)
Signature_md5 = calculate_md5(uni_id + password + role)


cur.execute("""
    INSERT INTO AccountDB (FirstName, LastName, Email, Password, Type, UniID, Sign_MD5, Ratings)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (first_name, last_name, email, hashed_password, role, uni_id, Signature_md5, ratings))

# Commit changes and close the connection
connection.commit()
connection.close()
