import psycopg2
import csv


conn = psycopg2.connect(
    dbname="phonebook",
    user="postgres",
    password="123",  
    host="localhost",
    port="5432"
)

cur = conn.cursor()


def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            phone VARCHAR(20) UNIQUE
        )
    """)
    conn.commit()

def insert_from_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute(
                """INSERT INTO contacts (first_name, phone)
                   VALUES (%s, %s)
                   ON CONFLICT (phone) DO NOTHING""",
                (row[0], row[1])
            )
    conn.commit()
    print("CSV data inserted successfully.")


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute(
        "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("Contact added.")

def update_contact():
    phone = input("Enter phone of contact to update: ")
    new_name = input("New name (leave empty to skip): ")
    new_phone = input("New phone (leave empty to skip): ")

    if new_name:
        cur.execute(
            "UPDATE contacts SET first_name=%s WHERE phone=%s",
            (new_name, phone)
        )

    if new_phone:
        cur.execute(
            "UPDATE contacts SET phone=%s WHERE phone=%s",
            (new_phone, phone)
        )

    conn.commit()
    print("Contact updated.")


def search_by_name():
    name = input("Enter name: ")
    cur.execute(
        "SELECT * FROM contacts WHERE first_name ILIKE %s",
        (f"%{name}%",)
    )
    results = cur.fetchall()
    for row in results:
        print(row)

def search_by_prefix():
    prefix = input("Enter phone prefix: ")
    cur.execute(
        "SELECT * FROM contacts WHERE phone LIKE %s",
        (f"{prefix}%",)
    )
    results = cur.fetchall()
    for row in results:
        print(row)


def delete_contact():
    choice = input("Delete by (1) name or (2) phone: ")

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "DELETE FROM contacts WHERE first_name=%s",
            (name,)
        )
    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute(
            "DELETE FROM contacts WHERE phone=%s",
            (phone,)
        )

    conn.commit()
    print("Contact deleted.")


def menu():
    create_table()

    while True:
        print("\n===== PHONEBOOK =====")
        print("1. Insert from CSV")
        print("2. Insert manually")
        print("3. Update contact")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_by_name()
        elif choice == "5":
            search_by_prefix()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    menu()
    cur.close()
    conn.close()
    print("Connection closed.")