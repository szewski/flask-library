from werkzeug.security import generate_password_hash


if __name__ == '__main__':
    username = 'admin'
    password = 'admin'

    hashed_password = generate_password_hash(password)

    print(hashed_password)

