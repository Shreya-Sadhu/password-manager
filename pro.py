from cryptography.fernet import Fernet
import os

# Generate a key for encryption and decryption
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the key from the current directory
def load_key():
    return open("secret.key", "rb").read()

# Initialize encryption key
def initialize_key():
    if not os.path.exists("secret.key"):
        generate_key()
    return load_key()

# Encrypt a message
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Decrypt a message
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

# Save a password
def save_password(service, username, password, key):
    encrypted_username = encrypt_message(username, key)
    encrypted_password = encrypt_message(password, key)
    
    with open("passwords.txt", "ab") as file:
        file.write(service.encode() + b" " + encrypted_username + b" " + encrypted_password + b"\n")

# Load passwords
def load_passwords(key):
    if not os.path.exists("passwords.txt"):
        return []

    passwords = []
    with open("passwords.txt", "rb") as file:
        for line in file:
            service, encrypted_username, encrypted_password = line.split(b" ", 2)
            username = decrypt_message(encrypted_username, key)
            password = decrypt_message(encrypted_password, key)
            passwords.append((service.decode(), username, password))
    return passwords

# Main program
def main():
    key = initialize_key()

    while True:
        print("Password Manager")
        print("1. Save a password")
        print("2. Load passwords")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter the service name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            save_password(service, username, password, key)
            print("Password saved!")
        elif choice == "2":
            passwords = load_passwords(key)
            if passwords:
                for service, username, password in passwords:
                    print(f"Service: {service}, Username: {username}, Password: {password}")
            else:
                print("No passwords found.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
