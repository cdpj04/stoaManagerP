import random as rd
import string
import json
import csv

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
    global user_data
    while True:
        print("\nPlease choose an option:")
        print("1. Save passwords to a file")
        print("2. Load passwords from a file")
        print("3. Create a backup")
        print("0. Exit")

        user_choice = get_input("Your choice: ")

        match user_choice:
            case "1":
                file_name = get_input("Enter the file name to save passwords (e.g., passwords.json or passwords.csv): ").strip()
                if not (file_name.endswith(".json") or file_name.endswith(".csv")):
                    print("Invalid file format. Please use a .json or .csv file.")
                    continue
                try:
                    if file_name.endswith(".json"):
                        with open(file_name, "w") as file:
                            json.dump(user_data, file, indent=4)
                        print(f"\nPasswords successfully saved to '{file_name}'!")
                    elif file_name.endswith(".csv"):
                        with open(file_name, "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow(["Website", "Username", "Password"])
                            for website, credentials in user_data.items():
                                for username, password in credentials.items():
                                    writer.writerow([website, username, password])
                        print(f"\nPasswords successfully saved to '{file_name}'!")
                except Exception as e:
                    print(f"\nAn error occurred while saving passwords: {e}")
            case "2":
                file_name = get_input("Enter the file name to load passwords (e.g., passwords.json or passwords.csv): ").strip()
                if not (file_name.endswith(".json") or file_name.endswith(".csv")):
                    print("Invalid file format. Please use a .json or .csv file.")
                    continue
                try:
                    if file_name.endswith(".json"):
                        with open(file_name, "r") as file:
                            user_data = json.load(file)
                        print(f"\nPasswords successfully loaded from '{file_name}'!")
                    elif file_name.endswith(".csv"):
                        with open(file_name, "r") as file:
                            reader = csv.reader(file)
                            next(reader)
                            user_data = {}
                            for row in reader:
                                if len(row) == 3:
                                    website, username, password = row
                                    user_data[website] = {username: password}
                        print(f"\nPasswords successfully loaded from '{file_name}'!")
                except FileNotFoundError:
                    print(f"\nFile '{file_name}' not found. Please check the file name and try again.")
                except json.JSONDecodeError:
                    print("\nThe file could not be decoded. It might be corrupted.")
                except Exception as e:
                    print(f"\nAn error occurred while loading passwords: {e}")
            case "3":
                file_name = get_input("Enter the name of the file to back up (e.g., passwords.json or passwords.csv): ").strip()
                if not (file_name.endswith(".json") or file_name.endswith(".csv")):
                    print("Invalid file format. Please use a .json or .csv file.")
                    continue
                backup_name = f"backup_{file_name}"
                try:
                    with open(file_name, "r") as original, open(backup_name, "w") as backup:
                        backup.write(original.read())
                    print(f"\nBackup created successfully as '{backup_name}'!")
                except FileNotFoundError:
                    print(f"\nFile '{file_name}' not found. Please check the file name and try again.")
                except Exception as e:
                    print(f"\nAn error occurred while creating a backup: {e}")
            case "0":
                break
            case _:
                print("\nInvalid input. Please try again.")

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