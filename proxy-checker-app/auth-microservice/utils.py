import string
import random

def generate_random_password(length=12):
    """
    Generate a random password string.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
