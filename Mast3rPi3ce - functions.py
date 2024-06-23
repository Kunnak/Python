# All Functions used in this Program

# IMPORTS
import files
from datetime import datetime
import json
import re
import hashlib

#                               ---------- LOGGING---------
#                               ---------------------------

# Datum und Uhrzeit generieren
def get_date():
    date = datetime.now()
    datum = date.strftime("%d.%m.%y")
    uhrzeit = date.strftime("%H:%M:%S")

    return datum, uhrzeit

def log_this(data):
    timestamp = get_date()
    date = timestamp[0]
    time = timestamp[1]
    message = f"[{date} | {time}]: {data}!\n"

    with open(files.logfile, 'a', newline='') as file:
        file.writelines(message)


#                               ---------- USER ----------
#                               --------------------------

class User:
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.tasks = []
        self.save_user()

    @staticmethod
    def check_password(password):
        pattern_password = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!§$%&=?€@_.])[A-Za-z0-9!§$%&=?€@_.]{8,}$'
        return re.match(pattern_password, password) is not None

    @staticmethod
    def check_email(email):
        pattern_email = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        return re.match(pattern_email, email) is not None

    @staticmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def dump_json(self, validate=True):
        if validate and (not self.check_password(self.password) or not self.check_email(self.email)):
            raise ValueError("Invalid password or email")

        return {
            "username": self.username,
            "password": self.encrypt_password(self.password) if validate else self.password,
            "name": self.name,
            "email": self.email,
            "tasks": [task.dump_json() for task in self.tasks]
        }

    @classmethod
    def load_existing_user(cls, user_data):
        user = cls.__new__(cls)
        user.username = user_data['username']
        user.password = user_data['password']
        user.name = user_data['name']
        user.email = user_data['email']
        user.tasks = [ToDo(task['task-name'], task['description'], task['zeitangabe'], task['status']) for task in user_data.get('tasks', [])]
        return user

    def save_user(self, validate=True):
        user_data = self.dump_json(validate=validate)
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        for i, user in enumerate(data):
            if user['username'] == self.username:
                data[i] = user_data
                break
        else:
            data.append(user_data)

        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_user(validate=False)


def create_user(username, password, name, email):
    user = User(username, password, name, email)
    return user

def get_userdata():
    while True:
        username = input(f"Username:  ")
        if not re.match(r'^[A-Za-z0-9_]{3,20}$', username):
            print(
                "Invalid username format. Please use alphanumeric characters and underscore (_), between 3 and 20 characters.")
            continue

        password = input(f"Password:  ")
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!§$%&=?€@_.])[A-Za-z0-9!§$%&=?€@_.]{8,}$', password):
            print(
                "Invalid password format. Password must be at least 8 characters long, and include at least one uppercase letter, one lowercase letter, one digit, and one special character.")
            continue

        name = input(f"Name:  ")
        # Optional: Validierung für Name hinzufügen, falls erforderlich

        email = input(f"Email:  ")
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            print("Invalid email format. Please enter a valid email address.")
            continue

        return username, password, name, email

def get_logindata():
    print(f"\nLogin!")
    username = input(f"Username:  ")
    password = input(f"Password:  ")
    return username, password

def check_login(username, password):
    with open(files.users, 'r') as file:
        data = json.load(file)
        for user_data in data:
            if user_data['username'] == username and user_data['password'] == hash_password(password):
                return True
        return False

def load_users():
    filename = files.users
    with open(filename, 'r') as file:
        users = json.load(file)
    return users

def save_users(users):
    filename = files.users
    with open(filename, 'w') as file:
        json.dump(users, file, indent=4)

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def change_password():
    users = load_users()
    updated = False
    username = input(f"Für welche User?:  ")
    new_password = input(f"Neues Passwort:  ")

    for user in users:
        if user['username'] == username:
            user['password'] = hash_password(new_password)
            updated = True

    if updated:
        print(f"[Kunnak] hat dat Passwort von {username} erfolgreich aktualisiert")
        save_users(users)
        log_this(f"[Kunnak] hat das Passwort von {username} erfolgreich aktualisiert")
    else:
        print(f"{username} nicht gefunden!")
        log_this(f"{username} für Passwortänderung nicht gefunden!")
        return None

def choose_user():
    users = load_users()
    print("Verfügbare Benutzer:")
    for user in users:
        print(user['username'])
    selected_user = input("Wähle einen User: ")
    for user in users:
        if user['username'] == selected_user:
            return user['username']
    print("Benutzer nicht gefunden. Bitte versuchen Sie es erneut.")
    return choose_user()

def assign_task_to_user(username, task):
    users = load_users()
    for user in users:
        if user['username'] == username:
            user_obj = User.load_existing_user(user)
            task_obj = ToDo(task.name, task.description, task.timelimit, task.status)
            user_obj.add_task(task_obj)
            print(f"Aufgabe erfolgreich zugewiesen an {username}")
            log_this(f"Aufgabe [{task.name}] wurde zugewiesen an {username}")
            return
    print("Fehler: Benutzer nicht gefunden.")


#                               ---------- TASKS ---------
#                               --------------------------

# Aufgabenklasse
class ToDo:
    def __init__(self, name, description, timelimit, status):
        self.name = name
        self.description = description
        self.timelimit = timelimit
        self.status = status

    def dump_json(self):
        return {
            "task-name": self.name,
            "description": self.description,
            "zeitangabe": self.timelimit,
            "status": self.status
        }

    def display_info(self):
        return (f"Name: {self.name}\n"
                f"Beschreibung: {self.description}\n"
                f"Zeitangabe: {self.timelimit}\n"
                f"Wichtigkeit: {self.status}\n")

def new_task():
    name = input("Task name: ")
    description = input("Task description: ")
    timelimit = input("Timelimit: ")
    status = input("Rate importance [1-10]: ")
    table = (name, description, timelimit, status)
    log_this(f"Aufgabe [{name}] wurde erstellt")
    return table

def show_assigned_tasks(username):
    users = load_users()
    for user_data in users:
        if user_data['username'] == username:
            user_obj = User.load_existing_user(user_data)
            tasks = user_obj.tasks
            if tasks:
                print(f"Aufgaben für Benutzer '{username}':")
                for index, task in enumerate(tasks, start=1):
                    print(f"Aufgabe {index}:")
                    print(task.display_info())
            else:
                print(f"Keine Aufgaben zugewiesen für Benutzer [{username}]")
            return
    print("Benutzer nicht gefunden.")
    log_this(f"Process failed to show tasks for [{username}] - no user found")

def remove_task_from_user(username, task_name):
    users = load_users()
    for user in users:
        if user['username'] == username:
            user_obj = User.load_existing_user(user)
            tasks = user_obj.tasks
            for task in tasks:
                if task.name == task_name:
                    tasks.remove(task)
                    user_obj.save_user(validate=False)
                    print(f"Aufgabe [{task_name}] erfolgreich entfernt von [{username}]")
                    log_this(f"Aufgabe '{task_name}' wurde von {username} entfernt")
                    return
            else:
                print(f"Aufgabe [{task_name}] nicht gefunden bei [{username}]")
                log_this(f"Process failed to remove task from {username} - Username not found")
                return
    print("Fehler: Benutzer nicht gefunden.")
    log_this(f"Process failed to remove task from [{username}] - Username not found")


#                         ---------- PROGRAMMFÜHRUNG ---------
#                         ------------------------------------

def intro():
    print(f"\nWillkommen\n"
          f"Bitte Melde dich an, oder erstelle einen neuen Account!\n"
          f"[1] Anmelden | [2] Neuerstellen | [3] Programm beenden")
    answer = input(f"Eingabe: ")
    if answer == '1':
        return True
    elif answer == '2':
        return False
    elif answer == '3':
        log_this(f"Program closed")
        stats()
        exit()

def menu(username):
    if username == "Kunnak":
        return input(f"[1] Show own Tasks | [2] Add Task for Users | [3] Remove Task from Users | [4] Change Users Passwords | [9] Quit\n"
                     f"Eingabe: ")
    else:
        return input(f"[1] Show Task | [2] Add Task | [3] Remove Task | [9] Quit\n"
                     f"Eingabe: ")

def stats():
    file = files.logfile
    with open(file, 'r') as file:
        reader = file.readlines()
        starts = 0
        closed = 0
        for row in reader:
            if 'started' in row:
                starts += 1
            if 'closed' in row:
                closed += 1
        print(f"Programm wurde {starts}x geöffnet!\n"
              f"Programm wurde {closed}x geschlossen!")
