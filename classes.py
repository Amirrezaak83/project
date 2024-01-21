from datetime import datetime
import sqlite3
import requests
import random
import string


def create_database_and_tables():
    with sqlite3.connect("Clinic Database.sql") as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Clinics (
                Clinic_id INTEGER PRIMARY KEY,
                name TEXT,
                address TEXT,
                phone_number TEXT,
                services TEXT,
                capacity INTEGER,
                availability BOOLEAN
            )
        ''')


        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Appointments (
                AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                ClinicID INTEGER,
                UserID INTEGER,
                DateTime DATETIME,
                Status VARCHAR(255)
            )
        ''')


        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                User_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) UNIQUE,
                name VARCHAR(255),
                Email VARCHAR(255),
                Password VARCHAR(255),
                User_type VARCHAR(255),
                Logged_in BOOLEAN
            )
        ''')


        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notifications (
                NotificationsID INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER ,
                message TEXT,
                date DATETIME,
                FOREIGN KEY (user_id) REFERENCES Users(User_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserInsurance (
                UserInsuranceID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER,
                InsuranceID INTEGER,
                FOREIGN KEY (UserID) REFERENCES Users(User_id),
                FOREIGN KEY (InsuranceID) REFERENCES Insurances(InsuranceID)
            )
        ''')

        conn.commit()


if __name__ == "__main__":
    create_database_and_tables()
    print("Database and tables created successfully.")


class User:
    def __init__(self, username, name, email, password, user_type, logged_in):
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.logged_in = logged_in
        
    @classmethod
    def register_account(cls, username, name, email, password, user_type):
        new_account = cls(username, name, email, password, user_type, logged_in=False)
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
                        User_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(255) UNIQUE,
                        name VARCHAR(255),
                        Email VARCHAR(255),
                        Password VARCHAR(255),
                        User_type VARCHAR(255),
                        Logged_in BOOLEAN)
                    ''')
        cursor.execute("SELECT * FROM Users WHERE email = ? OR username = ?", (email, username))
        existing_user = cursor.fetchone()
        if existing_user is not None:
            print("User with this email or username already exists.")
            return False
        else:

            cursor.execute('''INSERT INTO Users (username, name, email, password, user_type, logged_in)
                            VALUES (?, ?, ?, ?, ?, ?)
                           ''', (new_account.username, new_account.name, new_account.email,new_account.password, new_account.user_type, new_account.logged_in))
        Clinic_database.commit()
        print("registered successfully")
        return True
    
    
    @staticmethod
    def login(username, password):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
            existing_user = cursor.fetchone()
            
            if existing_user is not None:
                if existing_user[6] == 1:
                    print("You  have been logged in before")
                    return True
                else:
                    cursor.execute("UPDATE Users SET logged_in = 1 WHERE username = ?", (username,))
                    Clinic_database.commit()
                    print("logged in successfully")
                    return True
            else:
                print("invalid username or password")
                return False
    
    @staticmethod
    def login_with_generated_password( username, otp):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ?''', (username,))
            existing_user = cursor.fetchone()
            
            if existing_user is not None:
                if existing_user[6] == 1:
                    print("You  have been logged in before")
                    return True
                else:
                    cursor.execute("UPDATE Users SET logged_in = 1 WHERE username = ?", (username,))
                    Clinic_database.commit()
                    print("logged in successfully")
                    return True
            else:
                print("invalid username or password")
                return False     
            
            
    @staticmethod
    def logout(username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ?''', (username,))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("You are currently logged out")
                    return True
                else:
                    cursor.execute('''UPDATE Users SET logged_in = 0 WHERE username = ?''', (username,))
                    Clinic_database.commit()
                    print("logged out successfully")
                    return True
            else:
                print("invalid username or password")
                return False


    @staticmethod
    def Update_profile(username, new_name=None, new_email=None, new_password=None):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user is None:
                print("Invalid username.")
                return False

            if existing_user[6] == 0:  
                print("Please log in first.")
                return False

            updates = []
            params = []
            if new_name:
                updates.append("name = ?")
                params.append(new_name)
            if new_email:
                updates.append("email = ?")
                params.append(new_email)
            if new_password:
                updates.append("password = ?")
                params.append(new_password)

            if not updates:
                print("No updates provided.")
                return False

            sql = "UPDATE Users SET " + ", ".join(updates) + " WHERE username = ?"
            params.append(username)
            cursor.execute(sql, tuple(params))
            Clinic_database.commit()
            print("Profile updated successfully.")
            return True           
      
    @classmethod
    def delete_user(cls, username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
            Clinic_database.commit()
            print(f"User with username {username} deleted successfully")

          
    @classmethod
    def view_appoinment(cls, username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT ClinicID, DateTime, Status FROM Appointments JOIN Users ON Appointments.UserID = Users.User_id 
                           WHERE username = ?''', (username,))
            result = cursor.fetchall()
            return result
 

    @staticmethod   
    def get_user_type(username):
        with sqlite3.connect("Clinic Database.sql") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_type FROM Users WHERE username = ?", (username,))
            result = cursor.fetchone()
            return result[0] if result else None


    @staticmethod 
    def user_menu(username):
        user_type = User.get_user_type(username)
        
        if user_type == 'c':
            secretary_menu()
            
        else:
            while True:
                print("1. make appointment")
                print("2. cancel appointment")
                print("3. view appointment")
                print("4. update information")
                print("5. logout and return to main menu")
                patient_options = input("Select your option: ")
        
                if patient_options == '1':
                    Appointment.make_appoinment(username)
                elif patient_options == '2':
                    Appointment.cancel_appoinment(username)
                elif patient_options == '3':
                    User.view_appoinment(username)
                elif patient_options == '4':
                    User.update_profile(username)
                elif patient_options == '5':
                    print("Logging out...")
                    break
                else:
                    print("Invalid option selected.")



class Clinic:
    def __init__(self, clinic_id, name, address, phone_number, services, capacity, availablity):
        self.clinic_id = clinic_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.services = services
        self.capacity = capacity
        self.availablity = availablity

    @classmethod
    def AddClinic(cls):
        response = requests.get('http://127.0.0.1:5000/slots')
        if response.status_code == 200:
            id_and_cap = response.json()  # converted response to json
            with sqlite3.connect("Clinic Database.sql") as Clinic_database:
                cursor = Clinic_database.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS Clinics (
                            Clinic_id INTEGER PRIMARY KEY,
                            name TEXT NULLABLE,
                            address TEXT NULLABLE,
                            phone_number TEXT NULLABLE,
                            services TEXT NULLABLE,
                            capacity INTEGER,
                            availability BOOLEAN NULLABLE
                            )
                        ''')
                for clinic_id, capacity in id_and_cap.items():
                # Check if Clinic_id already exists
                    cursor.execute("SELECT * FROM Clinics WHERE Clinic_id = ?", (clinic_id,))
                    existing_clinic = cursor.fetchone()

                if existing_clinic is not None:
                    # Update existing record instead of inserting
                    cursor.execute('''UPDATE Clinics SET capacity = ? WHERE Clinic_id = ?''', (capacity, clinic_id))
                else:
                    # Insert new record
                    cursor.execute('''INSERT INTO Clinics (Clinic_id, capacity) VALUES(?, ?)''', (clinic_id, capacity))

                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Yas', 'Tehran, Ekbatan', '09122121021', 'Dental clinic', 1, 1))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Arya', 'shahrak gharb', '09230991250', 'Eye clinic', 1, 2))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Afra', 'Tajrish', '09230991163', 'Heart clinic', 0, 3))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Samarghand', 'Saadatabad', '09122064051', 'nouro clinic', 1, 4))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Shafa', 'Eslamshahr', '09128964951', 'orthopedia clinic', 0, 5))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Noor', 'Motehari street', '09216489632', 'Eye clinic', 1, 6))
                cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone_number = ?, services = ?, availability = ? WHERE Clinic_id = ?''',
                               ('Farda', 'Argentina square', '09337369788', 'Heart clinic', 0, 7))
                
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}")
          
          
    @staticmethod    
    def search_clinic(keyword):
        with sqlite3.connect("Clinic Database.sql") as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Clinics WHERE name LIKE ? OR services LIKE ?"
            cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
            results = cursor.fetchall()
        return results

    @staticmethod
    def get_available_slots(clinic_id):
        today = datetime.now().date()
        remaining_capacity = Appointment.calculate_daily_capacity(clinic_id, today)

        return {"remaining_capacity": remaining_capacity}


    @staticmethod
    def update_clinic_info(clinic_id, new_name=None, new_address=None, new_phone_number=None, new_services=None):
        updates = []
        params = []

        if new_name:
            updates.append("name = ?")
            params.append(new_name)
        if new_address:
            updates.append("address = ?")
            params.append(new_address)
        if new_phone_number:
            updates.append("phone_number = ?")
            params.append(new_phone_number)
        if new_services:
            updates.append("services = ?")
            params.append(new_services)

        if not updates:
            return "No updates provided."

        with sqlite3.connect("Clinic Database.sql") as conn:
            cursor = conn.cursor()
            query = "UPDATE Clinics SET " + ", ".join(updates) + " WHERE Clinic_id = ?"
            params.append(clinic_id)
            cursor.execute(query, params)
            conn.commit()
        
        return "Clinic information updated successfully"
    

    @staticmethod
    def increase_appointment_capacity(clinic_id, additional_capacity):
        with sqlite3.connect("Clinic Database.sql") as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT capacity FROM Clinics WHERE Clinic_id = ?", (clinic_id,))
            result = cursor.fetchone()
            if result is None:
                return "Clinic not found."

            current_capacity = result[0]
            new_capacity = current_capacity + additional_capacity

            cursor.execute("UPDATE Clinics SET capacity = ? WHERE Clinic_id = ?", (new_capacity, clinic_id))
            conn.commit()
            return "Clinic capacity increased successfully."
            
                 
class Appointment(Clinic, User):
    def __init__(self, Appoinment_id, clinic_id, User_id, DateTime, Status):
        super().__init__(clinic_id, User_id)
        self.Appoinment_id = Appoinment_id
        self.DateTime = DateTime
        self.Status = Status
        
       
    @staticmethod
    def calculate_daily_capacity(clinic_id, date):
        with sqlite3.connect("Clinic Database.sql") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM Appointments 
                WHERE ClinicID = ? AND DATE(DateTime) = ? AND Status = 'Scheduled'
            ''', (clinic_id, date))
            reserved_appointments = cursor.fetchone()[0]
    
            cursor.execute('SELECT capacity FROM Clinics WHERE Clinic_id = ?', (clinic_id,))
            total_capacity = cursor.fetchone()[0]
            capacity = max(total_capacity - reserved_appointments, 0)
            if capacity>0:
                return int(capacity)
            else:
                return print("This clinic is full")


    @staticmethod
    def make_appoinment(username, clinic_id, date_time_str):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Appointments (
                                AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                                ClinicID INTEGER,
                                UserID INTEGER,
                                DateTime DATETIME,
                                Status VARCHAR(255))
                            ''')
            cursor.execute('''SELECT * FROM Users WHERE username = ?''', (username,))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[5] == 'c':
                    print("You don't have access to this part")
                    return False
                else:
                    cursor.execute('''SELECT User_id FROM Users WHERE username = ?''', (username,))
                    user_id_tuple = cursor.fetchone()
                    User_id = user_id_tuple[0]
                    Clinic_id = input("Enter your intended clinic id: ")
                    date_time_str = input("Enter date and time (YYYY-MM-DD HH:MM): ")
                    try:
                        DateTime = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
                        if Appointment.calculate_daily_capacity(Clinic_id, DateTime) == True:
                            cursor.execute('''INSERT INTO Appointments (ClinicID, UserID, DateTime, Status)
                                               VALUES (?, ?, ?, ?)''', (Clinic_id, User_id, DateTime, "Scheduled"))
                            cursor.execute('''UPDATE Clinics SET Capacity = Capacity - 1 WHERE Clinic_id = ?''', (Clinic_id,))
                            
                            response = requests.post('http://127.0.0.1:5000/reserve', json={'id': Clinic_id, 'reserved': 1})
                            if response.status_code == 200:
                                Clinic_database.commit()
                                print("Appointment scheduled successfully")
                            else:
                                print("Failed to update slots in API")
                            return True
                    except ValueError:
                        print("Invalid date and time")
            else:
                print("Invalid username or password")
            return False
        
        
    @staticmethod
    def cancel_appoinment(username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ?''', (username))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("please login first")
                    return True
                if existing_user[5] != 'p':
                    print("You can,t cancell the appoinment ")
                    return True
                else:
                    cursor.execute('''SELECT User_id FROM Users WHERE username = ?''', (username,))
                    user_id_tuple = cursor.fetchone()
                    
                    if user_id_tuple is not None:
                        user_id = user_id_tuple[0]
                        cursor.execute('''UPDATE Appointments SET Status = ? WHERE UserID = ?''', ("cancelled", user_id))
                        Clinic_database.commit()
                        cursor.execute('''SELECT ClinicID FROM Appointments WHERE UserID = ?''', (user_id))
                        clinic_id_tuple = cursor.fetchone()
                        if clinic_id_tuple is not None:
                            cursor.execute('''UPDATE Clinics SET Capacity = Capacity + 1 WHERE Clinic_id = ?''',(clinic_id_tuple[0]))
                            Clinic_database.commit()
                            print("appoinment have cancelled successfully")
                            return True
                        else:
                            return False
            else:
                return False
            
     
    @staticmethod
    def reschedule_appoinment(username, appointment_id, new_time_str):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ?''', (username,))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("please login first")
                    return True
                if existing_user[5] != 'p':
                    print("You can,t change the appointment ")
                    return True
                else:
                    AppoinmentID = input("Enter your Appointment ID that you want change: ") 
                    new_time_str = input("Enter New time you want your appointment (YYYY-MM-DD HH:MM):   ")
                    cursor.execute('''SELECT * FROM Appointments WHERE AppointmentID = ?''', (AppoinmentID,))
                    new_datetime = datetime.strptime(new_time_str,"%Y-%m-%d %H:%M")
                    cursor.execute('''UPDATE Appointments SET DateTime = ?''', (new_datetime,))
                    Clinic_database.commit()
                    return True
            else:
                return False 


    @staticmethod
    def view_all_appointments(clinic_id):
        with sqlite3.connect("Clinic Database.sql") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Appointments WHERE ClinicID = ?", (clinic_id,))
            appointments = cursor.fetchall()
            return appointments
        

    @staticmethod
    def cancel_appointment_by_secretary(appointment_id):
        with sqlite3.connect("Clinic Database.sql") as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Appointments WHERE AppointmentID = ?", (appointment_id,))
            if cursor.fetchone() is None:
                return "Appointment not found."

            cursor.execute("DELETE FROM Appointments WHERE AppointmentID = ?", (appointment_id,))
            conn.commit()
            return "Appointment cancelled successfully."


            
class Notifications:
    def __init__(self,user_id, message):
        self.user_id = user_id
        self.message = message
        self.date = datetime.now()
        
    
    def send(self, username):
        Message_With_Time = f"{self.message}, {self.date}"
        ID_with_message = f"NotificationID: {self.NotificationID},  7{Message_With_Time}"
        message = f"User ID: {self.user_id},  {ID_with_message}"
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT User_id FROM Users WHERE username = ?''', (username,))
            user_id_tuple = cursor.fetchone()
            if user_id_tuple is not None:
                user_id = user_id_tuple[0]
                cursor.execute('''CREATE TABLE IF NOT EXISTS Notifications (
                                NotificationsID INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER ,
                                message TEXT,
                                date DATETIME,
                                FOREIGN KEY (user_id) REFERENCES Users(User_id))
                            ''')
                cursor.execute('''INSERT INTO Notifications (user_id, message, date)
                                  VALUES (?, ?, ?)''', (user_id, message, self.date))
                                  
        print(message)



class insurance:
    def __init__(self, insurance_id, company_name, services, phone_number):
        self.insurance_id = insurance_id
        self.company_name = company_name
        self.services = services
        self.phone_number = phone_number

    @classmethod
    def add_insurance(cls):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Insurances (
                            InsuranceID INTEGER PRIMARY KEY AUTOINCREMENT,
                            CompanyName TEXT,
                            services TEXT,
                            PhoneNumber TEXT)
                           ''')
            cursor.execute('''INSERT INTO Insurances (CompanyName, services, PhoneNumber)
                                 VALUES (?, ?, ?)''', ("Iran Insurance", "Health Insurance", "02146149289"))

            cursor.execute('''INSERT INTO Insurances (CompanyName, services, PhoneNumber)
                                 VALUES (?, ?, ?)''', ("Mehr Insurance", "Dental Insurance", "02166358976"))
            cursor.execute('''INSERT INTO Insurances (CompanyName, services, PhoneNumber)
                                VALUES (?, ?, ?)''', ("Mellat Insurance", "Health Insurance", "09128765467"))
            cursor.execute('''INSERT INTO Insurances (CompanyName, services, PhoneNumber)
                                 VALUES (?, ?, ?)''', ("Farda Insurance", "Dental Insurance", "02178763789"))
            cursor.execute('''INSERT INTO Insurances (CompanyName, services, PhoneNumber)
                                 VALUES (?, ?, ?)''', ("Amirreza Insurance", "Supplementary Insurnace", "09031736415"))

            Clinic_database.commit()
            print("insurances inserted successfully")

    @classmethod
    def view_insurances(cls):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Insurances''')
            insurances = cursor.fetchall()
        if insurances:
            for insurance in insurances:
                print("Insurance ID:", insurance[0])
                print("Company Name:", insurance[1])
                print("Services:", insurance[2])
                print("Phone Number:", insurance[3])
        else:
            print("No insurances found in the database.")



class UserInsurance(insurance, User):
    def __init__(self, user_id, insurance_id):
        super().__init__(insurance_id, user_id)
        self.user_id = user_id
        self.insurance_id = insurance_id

    @classmethod
    def add_user_insurance(cls, username, insurance_name):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS UserInsurance (
                               UserInsuranceID INTEGER PRIMARY KEY AUTOINCREMENT,
                               UserID INTEGER,
                               InsuranceID INTEGER,
                               FOREIGN KEY (UserID) REFERENCES Users(User_id),
                               FOREIGN KEY (InsuranceID) REFERENCES Insurances(InsuranceID))
                           ''')
            cursor.execute("SELECT User_id FROM Users WHERE username = ?", (username,))
            user_id = cursor.fetchone()[0]
            cursor.execute('''SELECT InsuranceID FROM Insurances WHERE CompanyName = ?''', (insurance_name,))
            insurance_id = cursor.fetchone()[0]

            cursor.execute("SELECT * FROM UserInsurance WHERE UserID = ? AND InsuranceID = ?", (user_id, insurance_id))
            existing_user_insurance = cursor.fetchone()

            if existing_user_insurance is not None:
                print("User already has this insurance.")
                return False
            else:
                cursor.execute('''INSERT INTO UserInsurance (UserID, InsuranceID)
                                     VALUES (?, ?)''', (user_id, insurance_id))
                Clinic_database.commit()
                print("User insurance added successfully.")
                return True



def main():
    while True:
        print("1. register account")
        print("2. login account")
        print("3. exit program")
        select_options = input("Select option: ")

        if select_options == '1':
            User.register_account()
        elif select_options == '2':
            user_logged_in = False
            username = input("Enter your username: ")
            if user_login():
                user_logged_in = True
                User.user_menu(username)
            else:
                print("Login failed or cancelled. Returning to main menu.")

        elif select_options == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid option selected.")



def user_login():
    print("1. login with your username and password")
    print("2. login with one time password")
    login_method = input("Select an option from above: ")


    if login_method == '1':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if User.login(username, password):
            with sqlite3.connect("Clinic Database.sql") as Clinic_database:
                cursor = Clinic_database.cursor()
                cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
                existing_user = cursor.fetchone()
                if existing_user:
                    return True
        return False
    elif login_method == '2':
        username = input("Enter your username: ")
        characters = string.ascii_uppercase + string.ascii_letters + string.digits + string.ascii_lowercase
        generated_password = "".join(random.choices(characters, k=8))
        print("Your one-time password is:", generated_password)
        otp = input("Enter the one-time password: ")
        if otp == generated_password:
            User.login_with_generated_password(username)
            with sqlite3.connect('''Clinic Database.sql''') as Clinic_database:
                cursor = Clinic_database.cursor()
                cursor.execute('''SELECT * From Users WHERE username = ?''',(username,))
                existing_user = cursor.fetchone()
                return True
        return False
    
    else:
        print("Invalid login method.")
        return False



def secretary_menu():
    while True:
        print("\nSecretary Menu:")
        print("1. View current appointments")
        print("2. Cancel an appointment")
        print("3. Increase appointment capacity")
        print("4. Log out")

        choice = input("Select an option: ")
        if choice == '1':
            appointments = Appointment.view_all_appointments()
            for appt in appointments:
                print(appt)

        elif choice == '2':
            appointment_id = input("Enter the appointment ID to cancel: ")
            result = Appointment.cancel_appointment_by_secretary(appointment_id)
            print(result)

        elif choice == '3':
            clinic_id = input("Enter clinic ID: ")
            additional_capacity = int(input("Enter additional capacity: "))
            Clinic.increase_appointment_capacity(clinic_id, additional_capacity)
             
        elif choice == '4':
            break
        
        else:
            print("Invalid option selected.")

