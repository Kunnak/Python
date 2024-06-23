# Main Program

# IMPORTS
import functions

functions.log_this(f"Program started")
login_create = functions.intro()
if not login_create:
    username, password, name, email = functions.get_userdata()
    new_user = functions.create_user(username, password, name, email)
    functions.log_this(f"User {username} wurde erstellt")
    MASTER = functions.check_login(username, password)
else:
    username, password = functions.get_logindata()
    MASTER = functions.check_login(username, password)

if MASTER:
    print(f"\n\n\nWillkommen {username}!")
    functions.log_this(f"{username} hat sich angemeldet")
    while True:
        if username == 'Kunnak':
            menu_choice = functions.menu(username)
            if menu_choice == '1':
                functions.show_assigned_tasks(username)
            elif menu_choice == '2':
                name, task, timelimit, status = functions.new_task()
                task1 = functions.ToDo(name, task, timelimit, status)
                user_to_assign = functions.choose_user()
                functions.assign_task_to_user(user_to_assign, task1)
            elif menu_choice == '3':
                user = functions.choose_user()
                functions.show_assigned_tasks(username)
                task_name = input("Welche Aufgabe soll gelöscht werden ?: ")
                functions.remove_task_from_user(user, task_name)
            elif menu_choice == '4':
                functions.change_password()
            elif menu_choice == '9':
                functions.log_this(f"Program closed")
                functions.stats()
                break

        else:
            menu_choice = functions.menu(username)
            if menu_choice == '1':
                functions.show_assigned_tasks(username)
                functions.log_this(f"{username} hat sich seine Aufgaben anzeigen lassen")
            elif menu_choice == '2':
                name, task, timelimit, status = functions.new_task()
                task1 = functions.ToDo(name, task, timelimit, status)
                functions.assign_task_to_user(username, task1)

            elif menu_choice == '3':
                functions.show_assigned_tasks(username)
                task_name = input("Welche Aufgabe soll gelöscht werden ?: ")
                functions.remove_task_from_user(username, task_name)
            elif menu_choice == '9':
                functions.log_this(f"Program closed")
                functions.stats()
                break

else:
    print(f"Anmeldung fehlgeschlagen!")
    functions.log_this(f"Anmeldung fehlgeschlagen - User [{username}]")
