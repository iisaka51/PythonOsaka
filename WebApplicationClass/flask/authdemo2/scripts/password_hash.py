from werkzeug.security import generate_password_hash, check_password_hash
hash = generate_password_hash('Python')
print(hash)

check = check_password_hash(hash, 'python')
print(check)
check = check_password_hash(hash, 'Python')
print(check)
