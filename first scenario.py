
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





