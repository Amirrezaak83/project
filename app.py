from flask import Flask, request, jsonify
from datetime import datetime
from project import Appointment, Clinic, User, UserInsurance, insurance, create_database_and_tables


app = Flask(__name__)

create_database_and_tables()

# In-memory database
database = {
    "1": 25,
    "2": 15,
    "3": 15,
    "4": 20,
    "5": 30,
    "6": 9,
    "7": 8
}

@app.route('/')
def home():
    return "Welcome to the Clinic Management System"


@app.route('/initializer', methods=['GET'])
def initialize_clinic():
    try:
        Clinic.AddClinic()
        return jsonify({"success": True, "message": "Clinic initialized successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/slots', methods=['GET'])
def get_slots():
    return jsonify(database)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    if not all([username, name, email, password, user_type]):
        return jsonify({"error": "All fields are required"}), 400

    success = User.register_account(username, name, email, password, user_type)
    if success:
        return jsonify({"message": "Registered successfully"})
    else:
        return jsonify({"error": "User with this email or username already exists"}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    success = User.login(username, password)
    if success:
        return jsonify({"message": "Logged in successfully"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route('/login_with_generated_password', methods=['POST'])
def login_with_generated_password():
    data = request.json
    username = data.get('username')
    otp = data.get('otp')

    if not username or not otp:
        return jsonify({'error': 'Username and OTP are required'}), 400

    result = User.login_with_generated_password(username, otp)
    return jsonify({'message': result})


@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    success = User.logout(username)
    if success:
        return jsonify({"message": "Logged out successfully"})
    else:
        return jsonify({"error": "Invalid username or already logged out"}), 401


@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    new_name = data.get('new_name')
    new_email = data.get('new_email')
    new_password = data.get('new_password')

    success = User.Update_profile(username, new_name, new_email, new_password)   
    if success:
        return jsonify({"message": "Profile updated successfully"})
    else:
        return jsonify({"error": "Update failed"}), 400


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    User.delete_user(username)
    return jsonify({"message": f"User with username {username} deleted successfully"})


@app.route('/view_appointments', methods=['GET'])
def view_appointments():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        appointments = Appointment.view_appoinment(username)
        if not appointments:
            return jsonify({'message': 'No appointments found for this user.'})
        else:
            return jsonify({'appointments': appointments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/search_clinic', methods=['GET'])
def search_clinic():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    clinics = Clinic.search_clinic(keyword)
    return jsonify({'clinics': clinics})


@app.route('/get_available_slots', methods=['GET'])
def get_available_slots():
    clinic_id = request.args.get('clinic_id')
    if not clinic_id:
        return jsonify({'error': 'Clinic ID is required'}), 400

    available_slots = Clinic.get_available_slots(clinic_id)
    return jsonify(available_slots)


@app.route('/increase_capacity', methods=['POST'])
def increase_capacity():
    data = request.json
    clinic_id = data.get('clinic_id')
    additional_capacity = data.get('additional_capacity', type=int)
    
    if not clinic_id or additional_capacity is None:
        return jsonify({'error': 'Clinic ID and additional capacity are required'}), 400

    result = Clinic.increase_appointment_capacity(clinic_id, additional_capacity)
    return jsonify({'message': result})


@app.route('/view_all_appointments', methods=['GET'])
def view_all_appointments():
    clinic_id = request.args.get('clinic_id')
    if not clinic_id:
        return jsonify({'error': 'Clinic ID is required'}), 400

    appointments = Appointment.view_all_appointments(clinic_id)
    return jsonify({'appointments': appointments})


@app.route('/cancel_appointment', methods=['POST'])
def cancel_appointment():
    data = request.json
    appointment_id = data.get('appointment_id')
    
    if not appointment_id:
        return jsonify({'error': 'Appointment ID is required'}), 400

    result = Appointment.cancel_appointment_by_secretary(appointment_id)
    return jsonify({'message': result})


@app.route('/add_insurance', methods=['POST'])
def add_insurance():
    data = request.json
    company_name = data.get('company_name')
    services = data.get('services')
    phone_number = data.get('phone_number')

    if not all([company_name, services, phone_number]):
        return jsonify({'error': 'All fields are required'}), 400

    insurance.add_insurance(company_name, services, phone_number)
    return jsonify({'message': 'Insurance added successfully'})


@app.route('/add_user_insurance', methods=['POST'])
def add_user_insurance():
    data = request.json
    username = data.get('username')
    insurance_name = data.get('insurance_name')

    if not username or not insurance_name:
        return jsonify({'error': 'Username and insurance name are required'}), 400

    result = UserInsurance.add_user_insurance(username, insurance_name)
    if result:
        return jsonify({'message': 'User insurance added successfully'})
    else:
        return jsonify({'error': 'Failed to add insurance to user'})


@app.route('/reserve', methods=['POST'])
def reserve_slot():
    data = request.json
    clinic_id = str(data.get('id'))
    reserved = data.get('reserved', 0)

    if clinic_id in database and database[clinic_id] >= reserved:
        database[clinic_id] -= reserved
        return jsonify({"success": True, "remaining_slots": database[clinic_id]})
    else:
        return jsonify({"success": False, "message": "Invalid request"}), 400
 
    
@app.route('/daily_capacity/<clinic_id>', methods=['GET'])
def get_daily_capacity(clinic_id):
    today = datetime.now().date()
    remaining_capacity = Appointment.calculate_daily_capacity(clinic_id, today)
    return jsonify({"remaining_capacity": remaining_capacity})



if __name__ == '__main__':
    app.run(debug=True)


