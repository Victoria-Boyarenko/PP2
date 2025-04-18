import psycopg2
import csv

def connect():
    return psycopg2.connect(
        database="PP2", user="postgres", password="V12$34i67#89v", host="localhost", port="5432"
    )

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE,   
            phone VARCHAR(20)
        )
    ''')
    conn.commit()
    conn.close()

def insert_from_csv(filename='data.csv'):
    conn = connect()
    cur = conn.cursor()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    conn.close()

def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    conn.close()

def update_user():
    username = input("Enter username to update: ")
    new_username = input("New username (leave empty to skip): ")
    new_phone = input("New phone (leave empty to skip): ")
    conn = connect()
    cur = conn.cursor()
    if new_username:
        cur.execute("UPDATE phonebook SET username = %s WHERE username = %s", (new_username, username))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (new_phone, username))
    conn.commit()
    conn.close()

def query_data():
    print("Available filters:")
    print("1 - username (the exact name)")
    print("2 - phone (the exact number)")
    print("3 - id ")
    print("4 - like (part of the name)")

    filter_option = input("Choose filter: ")

    conn = connect()
    cur = conn.cursor()

    if filter_option == "1":
        value = input("Enter username: ")
        cur.execute("SELECT * FROM phonebook WHERE username = %s", (value,))
    elif filter_option == "2":
        value = input("Enter phone: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (value,))
    elif filter_option == "3":
        value = input("Enter id: ")
        cur.execute("SELECT * FROM phonebook WHERE id = %s", (value,))
    elif filter_option == "4":
        value = input("Enter part of the username: ")
        cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s", (f"%{value}%",))
    else:
        print("Invalid choice")
        conn.close()
        return

    rows = cur.fetchall()
    if rows:
        print("\nResults:")
        for row in rows:
            print(row)
    else:
        print("Nothing was found")

    conn.close()


def delete_user():
    by = input("Delete by (username/phone): ")
    value = input(f"Enter {by}: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM phonebook WHERE {by} = %s", (value,))
    conn.commit()
    conn.close()

def menu():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update user")
        print("4. Query data")
        print("5. Delete user")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_user()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_user()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

menu()
