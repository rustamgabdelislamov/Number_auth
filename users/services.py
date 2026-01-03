import random
import string

def generate_invite_code(length=6):
    invite_base = []
    characters = string.ascii_letters + string.digits  # Символы: буквы и цифры
    invite_code = ''.join(random.choice(characters) for _ in range(length))
    invite_base.append(invite_code)
    return invite_code

# Пример использования
invite_code_ = generate_invite_code()
print(invite_code_)

def get_relevance_number():
    pass