import string
import secrets

def generate_unique_id(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

# Example
unique_id = generate_unique_id()
print(unique_id)
