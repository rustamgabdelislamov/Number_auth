import random
import string

def generate_invite_code(length=6):
    characters = string.ascii_letters + string.digits  # Символы: буквы и цифры
    invite_code = ''.join(random.choice(characters) for _ in range(length))
    return invite_code

# Пример использования
invite_code = generate_invite_code()
print(invite_code)