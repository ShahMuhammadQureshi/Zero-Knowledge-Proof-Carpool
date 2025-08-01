# 🚗 Secure Carpooling Web Application

A Flask-based ride-sharing web application that enables secure user registration, authentication, and real-time offer/request handling for both drivers and passengers. Includes role-based login, MD5-hashed credentials, and a built-in SQLite database for persistent storage and logs.

---

## 🧰 Features

- 🔐 Secure User Authentication using MD5 hashing & unique signatures  
- 👥 Role-based access: Passenger & Driver profiles  
- 🔄 Live Driver-Passenger Matching System  
- 🗂️ SQLite3 Database Integration for persistent user and trip data  
- 🧾 Logging with RotatingFileHandler  
- 🧪 APIs for login, registration, offer posting, and selection  

---
```bash
## 🗂️ File Structure

.
├── templates/
│ ├── index.html # Login page
│ ├── register.html # Registration page
│ ├── create_request.html # Passenger interface
│ └── set_offer.html # Driver interface
├── old_approach/
│ └── Database/
│ └── AccountSystem.db # SQLite database
├── logs/
│ └── server.log # Logging info
└── app.py # Main Flask app

```
---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.x  
- Flask  
- SQLite3  

Install dependencies:
```bash
pip install flask
```
---
▶️ Running the App
```bash
python app.py
```
The server will start on http://127.0.0.1:5000

🧪 Key Endpoints
```bash
/ → Login page

/register → Registration page

/create_request → Passenger flow

/set_offer → Driver flow

/select_driver → Book a driver

/get_offer_details → Fetch current offer
```
---
📌 Notes
Passwords are stored as MD5 hashes

Logging is stored under logs/server.log

Ensure the SQLite DB is available at: old_approach/Database/AccountSystem.db
