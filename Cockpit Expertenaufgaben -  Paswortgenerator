import string
import random

anzahl = 14

def generate_password():
    global anzahl
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(anzahl))
    return password

print(generate_password())
