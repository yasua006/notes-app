import hashlib


def create_users(cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL UNIQUE
        )
    """)

def new_user(cursor, email: str, password: str):
    insert_query = "INSERT INTO Users (email, password_hash) VALUES (?, ?)"
 
    encoded_password: bytes = password.encode()
    password_hash: str = hashlib.sha512(encoded_password).hexdigest()

    # parametized (?) - no SQL injection attack
    cursor.execute(insert_query, (email, password_hash))
