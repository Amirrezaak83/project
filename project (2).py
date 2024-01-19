import sqlite3
import requests
from datetime import datetime

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
                    
                    cursor.execute("SELECT * FROM Clinics WHERE Clinic_id = ?", (clinic_id,))
                    existing_clinic = cursor.fetchone()

                    if existing_clinic is None:
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
            
            
            
            
            
class Appoinment(Clinic, User): #inherit from User and Clinic 
    def __init__(self, Appoinment_id, clinic_id, User_id, DateTime, Status):
        super().__init__(clinic_id, User_id)  
        self.Appoinment_id = Appoinment_id
        self.DateTime = DateTime
        self.Status = Status
        
    @classmethod
    def make_appoinment(cls, username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Appointments (
                            AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                            ClinicID INTEGER,
                            UserID INTEGER ,
                            DateTime DATETIME,
                            Status VARCHAR(255),
                            FOREIGN KEY (ClinicID) REFERENCES Clinics(Clinic_id),
                            FOREIGN KEY (UserID) REFERENCES Users(User_id))
                        ''')
            cursor.execute('''SELECT * FROM Users WHERE username = ? ''', (username,))
            existing_user = cursor.fetchone()
            if existing_user is not None:
                if existing_user[5] == 'c':
                    print("you don,t have access to this part")
                    return True
                else:
                    cursor.execute('''SELECT User_id FROM Users WHERE username = ?''', (username,))
                    user_id_tuple = cursor.fetchone()
                    User_id = user_id_tuple[0]
                    Clinic_id = input("Enter your intended clinic id: ")
                    date_time_str = input("Enter date and time (YYYY-MM-DD HH:MM): ")
                    try:
                        DateTime = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
                        if Appoinment.check_clinic_capacity(Clinic_id) == True:
                            cursor.execute('''INSERT INTO Appointments (ClinicID, UserID, DateTime, Status)
                                               VALUES (?, ?, ?, ?)''', (Clinic_id, User_id, DateTime, "Scheduled"))
                            cursor.execute('''UPDATE Clinics SET Capacity = Capacity - 1 WHERE Clinic_id = ?''', (Clinic_id,))
                        Clinic_database.commit()
                        
                        print("Appoinment scheduled successfully")
                        return True
                    except ValueError:
                        print("invalid date and time")
                        
            else:
                print("invalid username or password")
                return False
            
            
            
    @staticmethod
    def cancell_appoinment(username):
        with sqlite3.connect("Clinic Database.sql") as Clinic_database:
            cursor = Clinic_database.cursor()
            cursor.execute('''SELECT * FROM Users WHERE username = ?''', (username,))
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
                        cursor.execute('''SELECT ClinicID FROM Appointments WHERE UserID = ?''', (user_id,))
                        clinic_id_tuple = cursor.fetchone()
                        if clinic_id_tuple is not None:
                            cursor.execute('''UPDATE Clinics SET Capacity = Capacity + 1 WHERE Clinic_id = ?''',(clinic_id_tuple[0],))
                            Clinic_database.commit()
                            print("appoinment have cancelled successfully")
                            return True
                        else:
                            return False
                    else:
                        return False
            

       
    @staticmethod
    def reschedule_appoinment(username):
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

            # Check if the user already has this insurance
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
        select_options = input("Select option:  ")
        if select_options == '1':
            User.register_account()
        if select_options == '2':
            print("1. login with your username and password")
            print("2. login with one time password")
            login_method = input("select an option From above: ")
            if login_method == '1':
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                User.login(username, password)
                with sqlite3.connect("Clinic Database.sql") as Clinic_database:
                    cursor =  Clinic_database.cursor()
                    cursor.execute('''SELECT * FROM Users WHERE username = ? AND password = ?''', (username, password))
                    existing_user = cursor.fetchone()
                    if existing_user is not None:
                        if existing_user[5] == 'p':
                            print("1. make appoinment")
                            print("2. cancell appoinment")
                            print("3. view appoinment")
                            print("4. logout")
                            print("5. updaate inoformation")
                            patient_options  = input("select your option: ")
                            if patient_options == '1':
                                Appoinment.make_appoinment(username, password)
                            elif select_options == '2':
                                Appoinment.cancell_appoinment(username, password)  
                            elif select_options == '3':
                                User.view_appoinment(username, password)
                            elif select_options == '4':
                                User.logout(username, password)
                            elif select_options == '5' :
                                if existing_user[5] == 'p':
                                    User.Update_profile(username, password)
                                    '''
        elif login_method == '2':
            generated_password = 
            
            
                
                                
main()
'''


def show_users():
    # Connect to the database
    with sqlite3.connect("Clinic Database.sql") as clinic_database:
        # Create a cursor
        cursor = clinic_database.cursor()

        # Execute SELECT query to fetch data from the Users table
        cursor.execute("SELECT * FROM Users")

        # Fetch all rows from the result set
        users = cursor.fetchall()

        # Print or process the retrieved data
        for user in users:
            print(user)
show_users()


def show_clinics():
    # Connect to the database
    with sqlite3.connect("Clinic Database.sql") as clinic_database:
        # Create a cursor
        cursor = clinic_database.cursor()

        # Execute SELECT query to fetch data from the Users table
        cursor.execute("SELECT * FROM Clinics")

        # Fetch all rows from the result set
        clinics = cursor.fetchall()

        # Print or process the retrieved data
        for clinic in clinics:
            print(clinic)
show_clinics()





