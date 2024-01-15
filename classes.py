import sqlite3
import requests
class User:
    def __init__(self, username, name, email, password, user_type, logged_in):
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.logged_in = logged_in
    @classmethod
    def register_account(cls):
        username = input("Enter username: ")
        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        user_type = input("Enter user type: ")
        new_account = cls(username, name, email, password, user_type, logged_in=False) #create and return a User object
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
    def Update_profile(username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ?''', (username,))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("please log in at first")
                    return True
                else:
                    new_name = input("Enter new name: ")
                    new_email = input("Enter new email: ")
                    new_password = input("Enter new password: ")
                    cursor.execute('''UPDATE Users SET name = ?, email = ?, password = ? WHERE username = ?''', (new_name, new_email, new_password, username))
                    Clinic_database.commit()
                    print("update profile successfully")
                    return True
            else:
                print("invalid username or password")
                return False
            
    @staticmethod
    def view_appoinment(username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT ClinicID, DateTime, Status FROM Appointments 
                          JOIN Users ON Appointments.UserID = Users.User_id 
                          WHERE username = ?''', (username,))
            result = cursor.fetchall()
        # Check if there are appointments to show
            if result:
                print("Appointments for", username)
                for appointment in result:
                    print("Clinic ID: {}, DateTime: {}, Status: {}".format(appointment[0], appointment[1], appointment[2]))
            else:
                print("No appointments found for this user.")
                
            return result  




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
    def UpdateClinicInfo(username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ?''', (username,))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[6] == 0:
                    print("Please login first")
                    return True
                else:
                    if existing_user[5] == 'p':
                        print("you don,t have access to this part")
                        return True
                    else:
                        new_clinic_name = input("Enter new clinic name: ")
                        new_address = input("Entern new address: ")
                        new_phone_number = input('Enter new phone number: ')
                        new_services = input("Enter all of your services that you have now: ")
                        cursor.execute('''UPDATE Clinics SET name = ?, address = ?, phone number = ?, services = ? 
                                       WHERE Clinics.User_id = (SELECT Users.User_id FROM Users WHERE Users.username = ?)
                                       ''', (new_clinic_name, new_address, new_phone_number, new_services, username))
                        Clinic_database.commit()
                        print("Update Clinic info successfully")
                        return True
            else:
                print("invalid username or password")
                return False