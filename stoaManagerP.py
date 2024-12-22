'''
PROJECT: Password Manager

Project Brief: Create a simple Password Manager that securely stores, retrieves, and manages user credentials (website, username, and password). The program will allow users to interact through a menu-based system and save data to a file for persistence.

Core Features:

	1.	Add New Passwords
Allow users to input and save a website, username, and password. - complete

	2.	Retrieve Passwords
Search for stored credentials based on the website name or username. - complete

	3.	Edit Existing Passwords
Enable users to update their stored information.- complete

	4.	Delete Passwords
Remove credentials for a specific website. - complete

	5.	Save and Load Passwords
Use file handling (e.g., JSON or CSV) to store data securely and load it on startup.

	6.	Generate Strong Passwords (Optional)
Include a feature to create random secure passwords using the random library. - complete

Outcome:
A functional command-line Password Manager that helps users organize and secure their credentials in a user-friendly way.
'''

import random as rd
import string
from unittest import case

user_data = {}

def main():
    first_run = True
    while True:
        if first_run:
            print("\nWelcome to stoaManagerP :)")
            first_run = False

        print("\nPlease choose an option:")
        print("1. Add a new password")
        print("2. View a password")
        print("3. Edit existing password")
        print("4. Delete existing password")
        print("5. Save and Load Passwords")
        print("6. Generate Password")
        print("0. Exit")

        user_input = input("Your Choice: ")

        match user_input:
            case "1":
                add_password()
            case "2":
                view_password()
            case "3":
                edit_password()
            case "4":
                delete_password()
            case "5":
                save_password()
            case "6":
                password_generator()
            case "0":
                print("\nThank you for using stoaManagerP!")
                break
            case _:
                print("\nInvalid Input, please try again.")

def get_input(prompt, allow_exit=False):
    while True:
        user_input = input(prompt).strip()
        if allow_exit and user_input.lower() == "exit":
            return "Exit"
        if user_input:
            return user_input
        print("Input cannot be empty. Please try again.")

def add_password():
    while True:
        try:
            website = get_input("\nPlease enter the website name (type 'exit' to leave): ", allow_exit=True).capitalize()
            if website == "Exit":
                break

            username = get_input("Please enter the username: ")
            password = get_input("Please enter the password: ")

            if website in user_data:
                overwrite = input(f"An entry for '{website}' already exists. Overwrite? (yes/no): ").strip().lower()
                if overwrite != "yes":
                    print("Operation cancelled.")
                    continue

            user_data[website] = {username: password}
            print("\nSuccessfully added new password!")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

def view_password():
    if user_data:
        while True:
            print("\nPlease choose an option:")
            print("1. View existing credentials")
            print("2. View individual credentials")
            print("0. Exit")
            user_choice = get_input("Your choice: ")

            match user_choice:
                case "1":
                    print(f"\n--- All Credentials ---")

                    for websites in user_data:
                        username, password = next(iter(user_data[websites].items()))
                        print(f"{websites} User credentials:")
                        print(f"Username: {username}")
                        print(f"Password: {password}")
                        print("--------------------------")
                case "2":
                    while True:
                        user_request = get_input("\nPlease enter the website name (type 'exit' to leave): ").capitalize()
                        if user_request == "Exit":
                            break

                        if user_request in user_data:
                            username, password = next(iter(user_data[user_request].items()))
                            print(f"\n--- {user_request} Credentials ---")
                            print(f"Username: {username}")
                            print(f"Password: {password}")
                            print("-------------------------")
                            break
                        else:
                            print(f"\nCredentials for {user_request} not found. Please try again.")
                case "0":
                    break
                case _:
                    print("Invalid Input, please try again.")
    else:
        print("\nNo credentials entered. Please try again.")

def edit_password():
    print(f"\n--- Websites ---")
    for i, website in enumerate(user_data, start=1):
        print(f"{i}. {website}")

    user_choice = get_input("\nPlease enter the website name (type 'exit' to leave): ").capitalize()
    if user_choice not in user_data:
        print(f"No credentials found for {user_choice}.")
        return

    current_username, current_password = next(iter(user_data[user_choice].items()))
    print(f"\n{user_choice} User credentials:")
    print(f"Username: {current_username}")
    print(f"Password: {current_password}")

    edit_choice = input("\nWould you like to edit username, password, or both? ").strip().lower()
    match edit_choice:
        case "username":
            new_username = get_input("Please enter the new username: ")
            user_data[user_choice] = {new_username: current_password}
            print(f"\n{user_choice} username updated! Username is now {new_username}")
        case "password":
            new_password = get_input("Please enter the new password: ")
            user_data[user_choice][current_username] = new_password
            print(f"\n{user_choice} password updated! Password is now {new_password}")
        case "both":
            new_username = get_input("Please enter the new username: ")
            new_password = get_input("Please enter the new password: ")
            user_data[user_choice] = {new_username: new_password}
            print(f"\n{user_choice} credentials updated! New Username: {new_username}, New Password: {new_password}")
        case _:
            print("\nInvalid input. Please try again.")

def delete_password():
    if user_data:
        print(f"\n--- Websites ---")
        i = 1
        for website in user_data:
            print(f"{i}. {website}")
            i += 1

        while True:
            user_choice = get_input("\nPlease enter the website name (type 'exit' to leave): ").capitalize()
            if user_choice == "Exit":
                break
            elif user_choice in user_data:
                del user_data[user_choice]
                print("\nUser credentials deleted!")
                break
            else:
                print(f"\nCredentials for {user_choice} not found. Please try again.")
    else:
        print("\nNo credentials found. Please try again.")

def save_password():
    pass 

def password_generator():
    if user_data:
        print(f"\n--- Websites ---")
        for i, website in enumerate(user_data, start=1):
            print(f"{i}. {website}")

        while True:
            user_choice = get_input("\nPlease enter the website name (type 'exit' to leave): ").capitalize()
            if user_choice == "Exit":
                break
            elif user_choice in user_data:
                username = next(iter(user_data[user_choice]))
                rand_password = ''.join(rd.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
                user_data[user_choice][username] = rand_password

                print(f"\nPassword for {user_choice} has been updated.")
                print(f"New Password: {rand_password}")
                break
            else:
                print(f"\n{user_choice} does not exist in your saved credentials. Try again.")
    else:
        print("\nNo credentials entered. Please try again.")


if __name__ == "__main__":
    main()