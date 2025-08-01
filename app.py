from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import hashlib
import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure logging
logs_dir = 'logs'
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler(os.path.join(logs_dir, 'server.log'), maxBytes=1000000, backupCount=1)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.DEBUG)  # Set logging level to DEBUG
app.logger.addHandler(log_handler)

# Function to calculate MD5 hash
def calculate_md5(text):
    return hashlib.md5(text.encode()).hexdigest()

# Function to authenticate user credentials against the SQLite database
def authenticate_user(email, password, user_type):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('old_approach/Database/AccountSystem.db')
        cursor = connection.cursor()

        # Calculate Signature MD5 Hash
        uni_id = email.split('@')[0]
        signature_md5 = calculate_md5(uni_id + password + user_type)

        # Execute the query to fetch user details
        hash_password = calculate_md5(password)
        cursor.execute("SELECT * FROM AccountDB WHERE Email=? AND Password=? AND Sign_MD5=?", 
                       (email, hash_password,signature_md5))
        user = cursor.fetchone()

        # Close the database connection
        connection.close()

        # Check if user exists and credentials match
        if user:
            return True
        else:
            return False
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return False

# Function to log user login
def log_user_login(email, user_type):
    try:
        log_text = f"Logged in: {email}, Type: {user_type}, Connection: {request.remote_addr}, Time: {datetime.datetime.now()}\n"
        
        # Write log text to file
        app.logger.info(log_text)
    except Exception as e:
        app.logger.error(f"An error occurred while logging user login: {e}")

# Function to register a new user
def register_user(first_name, last_name, email, password, role):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('old_approach/Database/AccountSystem.db')
        cursor = connection.cursor()

        # Check if email and role combination already exists
        cursor.execute("SELECT * FROM AccountDB WHERE Email=? AND Type=?", (email, role))
        existing_user = cursor.fetchone()
        if existing_user:
            return False, "User with the same email and role already exists"

        # Hash password
        uni_id = email.split('@')[0]
        hashed_password = calculate_md5(password)
        Signature_md5 = calculate_md5(uni_id + password + role)

        # Insert new user into the database
        cursor.execute("INSERT INTO AccountDB (FirstName, LastName, Email, Password, Type, UniID, Sign_MD5, Ratings) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (first_name, last_name, email, hashed_password, role, uni_id, Signature_md5, 0.4))
       
        connection.commit()

        # Close the database connection
        connection.close()

        return True, "Registration successful"
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return False, "Registration failed"
    
# Route to render the registration page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# Route to handle registration requests
@app.route('/register', methods=['POST'])
def register():
    try:
        # Get form data
        first_name = request.form.get('FirstName')
        last_name = request.form.get('LastName')
        email = request.form.get('Email')
        password = request.form.get('Password')
        confirm_password = request.form.get('ConfirmPassword')
        selected_role = request.form.get('selected_role')

        # Validate form data
        if not (first_name and last_name and email and password and confirm_password and selected_role):
            return "All fields are required", 400

        if password != confirm_password:
            return "Passwords do not match", 400

        # Register user
        success, message = register_user(first_name, last_name, email, password, selected_role)
        if success:
            return jsonify({'status': 'success', 'message': message}), 200
        else:
            return jsonify({'status': 'failure', 'message': message}), 400

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# Route to render the login page
@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

# Route to handle login requests
# Route to handle login requests
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('role')

        # Authenticate user
        auth_status = authenticate_user(email, password, user_type)

        if auth_status:
            # Authentication successful
            log_user_login(email, user_type)
            
            # Redirect user to profile based on user_type
            if user_type == 'Passenger':
                return redirect(url_for('create_request'))
            elif user_type == 'Driver':
                return redirect(url_for('set_offer'))

        else:
            # Authentication failed
            return jsonify({'status': 'failure', 'message': 'Invalid credentials'}), 401

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


# called by passenger
# when creating a request
# @app.route('/passenger_request', methods=['POST'])
# def passenger_request():
#     user_id = request.form.get('user_id')
#     source = request.form.get('source')
#     destination = request.form.get('destination')
    
#     # TODO: save in database
#     # TODO: navigate user to drivers offers screen
    
#     return record_id

# called by driver
# when submitting an offer
# @app.route('/driver_offers', methods=['POST'])
# def driver_offers():
#     driver_id = request.form.get('driver_id')
#     source = request.form.get('source')
#     destinations = request.form.get('destinations')
#     fare = request.form.get('fare')
#     max_passengers = request.form.get('max_passengers')
#     departure_time = request.form.get('departure_time')
#     status = 'CREATED'
#     passenger_request_ids = [] 
    

    # TODO: save in database
        # only update if already exists
        # create if new
    # TODO: navigate driver to user accepted offers screen

# called by passenger
# to get a list of available drivers
# fetched after every 5 seconds


# @app.route('/available_drivers', methods=['POST'])
# def available_drivers():
#     target_destination = request.form.get('destination')
    
#     all_driver_offers = [] # SELECT * FROM driver_offers WHERE {target_destination} IN destinations AND 

#     return jsonify({'offers': all_driver_offers})


# called by driver
# to see if any user has accepted his/her offer
# fetched after every 5 seconds

# @app.route('/get_driver_offer', me_driver_offerthods=['POST'])
# def list_accepted_driver_offers():
#     driver_id = request.form.get('driver_id')

#     offer = {} # SELECT * FROM driver_offers WHERE driver_id = {driver_id} LIMIT = 1

#     return jsonify(offer)


# fetched after every 5 seconds
# @app.route('/accept_driver_offers', methods=['POST'])
# def accepted_driver_offers():
#     user_id = request.form.get('user_id')
#     request_id = request.form.get('request_id')
#     driver_id = request.form.get('driver_id')

    # UPDATE  driver_offers WHERE driver_id = {driver_id} VALUES status = 'ACCEPTED'
    # UPDATE  driver_offers WHERE driver_id = {driver_id} VALUES status = 'ACCEPTED'


# Route for passenger profile
@app.route('/create_request', methods=['GET'])
def Passnger_page():
    return render_template('create_request.html')

@app.route('/create_request', methods=['POST'])
def create_request():
    try:
        # Extract request data
        user_id = request.form.get('user_id')
        source = request.form.get('source')
        destination = request.form.get('destination')

        # Connect to the SQLite database
        connection = sqlite3.connect('old_approach/Database/AccountSystem.db')
        cursor = connection.cursor()

        # Search for suitable drivers
        cursor.execute("""
        SELECT * FROM DriverDetails 
        WHERE source=? AND destination=? AND (seats - booked_seats) != 0
        """, (source, destination))
        matching_drivers = cursor.fetchall()

        # Close the connection
        connection.close()

        # Return the search results
        return jsonify({'status': 'success', 'matching_drivers': matching_drivers}), 200

    except Exception as e:
        # Return an error message if any exception occurs
        return jsonify({'status': 'error', 'message': str(e)}), 500




# Route for driver profile
@app.route('/set_offer',methods=['GET'])
def driver_page():
    return render_template('set_offer.html')

@app.route('/set_offer', methods=['POST'])
def set_offer():
    try: 
        # Get data from the request
        driver_id = request.form.get('user_id')
        source = request.form.get('source')
        destination = request.form.get('destination')
        fare = request.form.get('fare')
        max_passengers = request.form.get('seats')
        departure_time = request.form.get('departure_time')
        
        # Connect to the SQLite database
        connection = sqlite3.connect('old_approach/Database/AccountSystem.db')
        cursor = connection.cursor()
        
        # Check if an offer already exists for the given user ID
        cursor.execute("""
            SELECT COUNT(*) FROM DriverDetails WHERE User_ID=?
        """, (driver_id,))
        exists = cursor.fetchone()[0]
        
        if exists:
            # Update the existing offer
            cursor.execute("""
                UPDATE DriverDetails
                SET source=?, destination=?, seats=?, departure_time=?, fair=?
                WHERE User_ID=?
            """, (source, destination, max_passengers, departure_time, fare, driver_id))
        else:
            # Insert a new offer
            cursor.execute("""
                INSERT INTO DriverDetails (User_ID, source, destination, seats, Booked_seats, departure_time, fair)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (driver_id, source, destination, max_passengers, 0 , departure_time, fare))
        
        # Commit the transaction
        connection.commit()
        
        # Fetch the details of the offer
        cursor.execute("""
            SELECT * FROM DriverDetails WHERE User_ID=?
        """, (driver_id,))
        offer_details = cursor.fetchone()
        
        # Close the connection
        connection.close()
        
        # return jsonify({'status': 'success','message': 'Offer set successfully'}), 200
        # Send a success response along with offer details
        return jsonify({'status': 'success', 'message': 'Offer set successfully', 'offer_details': offer_details}), 200
    
    except Exception as e:
        # Send an error response if any exception occurs
        return jsonify({'status': 'error', 'message': str(e)}), 500
    


@app.route('/get_offer_details', methods=['GET'])
def get_offer_details():
    try:
        # Get the user ID from the request
        user_id = request.args.get('user_id')

        # Connect to the SQLite database
        connection = sqlite3.connect('old_approach/Database/AccountSystem.db')
        cursor = connection.cursor()

        # Execute query to fetch offer details for the specified user ID
        cursor.execute("SELECT * FROM DriverDetails WHERE User_ID=? ORDER BY ID DESC LIMIT 1", (user_id,))
        offer_details = cursor.fetchone()

        # Close the database connection
        connection.close()

        if offer_details:
            # Return offer details as JSON response
            return jsonify({'status': 'success', 'message': 'Offer details fetched successfully', 'offer_details': offer_details}), 200
        else:
            return jsonify({'status': 'error', 'message': 'No offer details found'}), 404
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500



@app.route('/select_driver', methods=['POST'])
def select_driver():
    try:
        driver_id = request.form.get('driver_id')

        # Connect to the SQLite database
        connection = sqlite3.connect('old_approach/Database/AccountSystem.db')
        cursor = connection.cursor()

        # Fetch driver details
        cursor.execute("""
            SELECT * 
            FROM DriverDetails 
            WHERE User_ID=?
        """, (driver_id,))
        result = cursor.fetchone()

        if result:
            # Extract details from the result
            driver_details = {
                'ID': result[0],
                'User_ID': result[1],
                'source': result[2],
                'destination': result[3],
                'seats': result[4],
                'Booked_seats': result[5],
                'departure_time': result[6],
                'fare': result[7]
            }

            # Check if there are available seats
            if driver_details['seats'] > driver_details['Booked_seats']:
                # Update booked seats
                cursor.execute("UPDATE DriverDetails SET Booked_seats = Booked_seats + 1 WHERE User_ID=?", (driver_id,))
                connection.commit()

                connection.close()
                return jsonify({'status': 'success', 'message': 'Driver selected and booked seats updated', 'driver_details': driver_details}), 200
            else:
                connection.close()
                return jsonify({'status': 'error', 'message': 'No available seats'}), 400
        else:
            connection.close()
            return jsonify({'status': 'error', 'message': 'Driver not found'}), 404

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500



# Main function to start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
