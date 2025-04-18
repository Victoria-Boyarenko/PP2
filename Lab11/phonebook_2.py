import psycopg2
import csv

def connect():
    return psycopg2.connect(
        database="PP2_11", user="postgres", password="V12$34i67#89v", host="localhost", port="5432"
    )

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebook_lab11 (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            phone VARCHAR(20)
        );
    ''')
    conn.commit()
    conn.close()

def insert_from_csv(filename='data.csv'):
    conn = connect()
    cur = conn.cursor()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2:
                print(f"Skipping invalid row (wrong format): {row}")
                continue
            username, phone = row[0], row[1]
            if not phone.isdigit() or len(phone) != 11 or not phone.startswith(('7', '8')):
                print(f"Invalid phone format for user {username}: {phone}")
                continue
            try:
                cur.execute("CALL insert_or_update_user(%s, %s);", (username, phone))
            except Exception as e:
                print(f"Error inserting {username}: {e}")
                continue
    conn.commit()
    conn.close()

def search_phonebook(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_phonebook(%s);", (pattern,))
    results = cur.fetchall()
    conn.close()
    return results

def insert_or_update_user(username, phone):
    if not phone.isdigit() or len(phone) != 11 or not phone.startswith(('7', '8')):
        print(f"Invalid phone number format: {phone}")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL insert_or_update_user(%s, %s);", (username, phone))
        conn.commit()
    except Exception as e:
        print(f"Insert/update error for {username}: {e}")
    finally:
        conn.close()

def insert_many_users(user_list):
    conn = connect()
    cur = conn.cursor()

    valid_users = []
    invalid_users = []

    for user in user_list:
        if len(user) != 2 or not user[1].isdigit() or len(user[1]) != 11 or not user[1].startswith(('7', '8')):
            invalid_users.append(user)
        else:
            valid_users.append(user)

    print("\nInvalid users:")
    for username, phone in invalid_users:
        print(f"{username} -> {phone}")

    print("\nInserted/Updated users:")
    for username, phone in valid_users:
        try:
            cur.execute("CALL insert_or_update_user(%s, %s);", (username, phone))
            print(f"{username} -> {phone}")
        except Exception as e:
            print(f"Error for {username}: {e}")

    conn.commit()
    conn.close()

def get_users_paginated(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_users_paginated(%s, %s);", (limit, offset))
    results = cur.fetchall()
    conn.close()
    return results

def delete_user(value):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_user(%s);", (value,))
    conn.commit()
    conn.close()

def menu():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Search by pattern")
        print("2. Insert or update user")
        print("3. Insert many users")
        print("4. Paginated output")
        print("5. Delete user")
        print("6. Insert from CSV")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            pattern = input("Enter part of name or phone: ")
            results = search_phonebook(pattern)
            if results:
                for row in results:
                    print(row)
            else:
                print("No matches found.")

        elif choice == "2":
            username = input("Enter username: ")
            phone = input("Enter phone: ")
            insert_or_update_user(username, phone)

        elif choice == "3":
            user_list = []
            print("Enter user data (blank username to stop):")
            while True:
                username = input("Username: ")
                if not username:
                    break
                phone = input("Phone: ")
                user_list.append([username, phone])
            insert_many_users(user_list)

        elif choice == "4":
            limit = int(input("Enter limit: "))
            offset = int(input("Enter offset: "))
            results = get_users_paginated(limit, offset)
            if results:
                for row in results:
                    print(row)
            else:
                print("No records found.")

        elif choice == "5":
            value = input("Enter username or phone to delete: ")
            delete_user(value)
            print("User deleted.")

        elif choice == "6":
            insert_from_csv()
            print("Users inserted from CSV.")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")

menu()
