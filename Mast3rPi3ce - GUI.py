from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import hashlib
import functions
import files
import json

class GUI(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.show_register_login_menu()
        return self.layout

    def show_register_login_menu(self, instance=None):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Willkommen!'))

        register_button = Button(text='Registrieren')
        register_button.bind(on_press=self.show_register)
        login_button = Button(text='Anmelden')
        login_button.bind(on_press=self.show_login)
        self.layout.add_widget(register_button)
        self.layout.add_widget(login_button)

    def show_main_menu_user(self, instance=None):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Hauptmenü'))

        show_own_tasks = Button(text='Aufgaben anzeigen')
        show_own_tasks.bind(on_press=self.show_tasks)
        self.layout.add_widget(show_own_tasks)

        self.add_task = Button(text='Aufgabe hinzufügen')
        self.layout.add_widget(self.add_task)

        self.delete_task = Button(text='Aufgabe entfernen')
        self.layout.add_widget(self.delete_task)

        self.close_program = Button(text='Programm beenden')
        self.layout.add_widget(self.close_program)

    def show_main_menu_admin(self,instance=None):

        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Hauptmenü'))

        show_own_tasks = Button(text='Aufgaben anzeigen')
        show_own_tasks.bind(on_press=self.show_tasks)
        self.layout.add_widget(show_own_tasks)

        self.add_task = Button(text='Aufgabe hinzufügen')
        self.layout.add_widget(self.add_task)

        self.delete_task = Button(text='Aufgabe entfernen')
        self.layout.add_widget(self.delete_task)

        self.change_password = Button(text='Passwort zurücksetzen')
        self.layout.add_widget(self.change_password)

        self.quit = Button(text='Programm beenden')
        self.layout.add_widget(self.quit)

    def show_register(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Registrieren'))

        self.layout.add_widget(Label(text='Benutzername'))
        self.input_username = TextInput()
        self.layout.add_widget(self.input_username)

        self.layout.add_widget(Label(text='Passwort'))
        self.password = TextInput(password=True)
        self.layout.add_widget(self.password)

        self.layout.add_widget(Label(text='Name'))
        self.input_name = TextInput()
        self.layout.add_widget(self.input_name)

        self.layout.add_widget(Label(text='Email'))
        self.email = TextInput()
        self.layout.add_widget(self.email)

        register = Button(text='Registrieren')
        register.bind(on_press=self.process_register)
        self.layout.add_widget(register)

        back = Button(text='Zurück')
        back.bind(on_press=self.show_register_login_menu)
        self.layout.add_widget(back)

    def process_register(self, instance):
        username = self.input_username.text
        password = self.password.text
        name = self.input_name.text
        email = self.email.text
        functions.create_user(username, password, name, email)
        functions.log_this(f"User {username} wurde erstellt")
        self.show_login()

    def show_login(self, instance=None):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Anmelden'))

        self.layout.add_widget(Label(text='Benutzername'))
        self.input_username = TextInput()
        self.layout.add_widget(self.input_username)

        self.layout.add_widget(Label(text='Passwort'))
        self.password = TextInput(password=True)
        self.layout.add_widget(self.password)

        login = Button(text='Anmelden')
        login.bind(on_press=self.process_login)
        self.layout.add_widget(login)

        back = Button(text='Zurück')
        back.bind(on_press=self.show_register_login_menu)
        self.layout.add_widget(back)

    def process_login(self, instance):
        username = self.input_username.text
        password = self.password.text

        MASTER_LOGIN = functions.check_login(username, password)
        print(f"Anmelden mit Benutzername: {username}, Passwort: {hashlib.sha256(password.encode()).hexdigest()}")

        if MASTER_LOGIN and username != 'Kunnak':
            print(f"Anmeldung mit {username} erfolgreich!")
            self.show_main_menu_user()
        elif MASTER_LOGIN and username == 'Kunnak':
            print(f"Willkommen allherschender Meister!")
            self.show_main_menu_admin()
        else:
            print(f"Anmeldung fehlgeschlagen!")
            self.show_register_login_menu()

    def show_tasks(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Daten aus JSON'))

        users = files.users

        # JSON-Datei einlesen
        with open(users, 'r') as f:
            data = json.load(f)

        # Überprüfen, ob data eine Liste oder ein Dictionary ist
        if isinstance(data, list):
            # Falls data eine Liste ist, nimm das erste Element
            data = data[0]

        username = self.input_username.text

        if username in data:
            user_data = data[username]
            # Daten anzeigen
            if 'tasks' in user_data:
                counter = 0
                for task in data['tasks']:
                    counter += 1
                    self.layout.add_widget(Label(text=f"Aufgabe {counter}:"))
                    self.layout.add_widget(Label(text=f"Aufgabenname: {task['task-name']}"))
                    self.layout.add_widget(Label(text=f"Beschreibung: {task['description']}"))
                    self.layout.add_widget(Label(text=f"Zeitangabe: {task['zeitangabe']}"))
                    self.layout.add_widget(Label(text=f"Status: {task['status']}"))
                    self.layout.add_widget(Label(text=''))

        back = Button(text='Zurück')
        if username == 'Kunnak':
            back.bind(on_press=self.show_main_menu_admin)
        else:
            back.bind(on_press=self.show_main_menu_user)
        self.layout.add_widget(back)


if __name__ == '__main__':
    GUI().run()
