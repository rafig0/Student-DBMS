import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

# Create demo tables with sample data
def create_demo_tables():
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, instructor TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, course_id INTEGER)")

    # Insert sample data
    cursor.execute("INSERT OR IGNORE INTO students (id, name, age) VALUES (1, 'Alice', 20), (2, 'Bob', 22), (3, 'Charlie', 21)")
    cursor.execute("INSERT OR IGNORE INTO courses (id, title, instructor) VALUES (1, 'Math', 'Dr. Smith'), (2, 'Physics', 'Dr. Brown')")
    cursor.execute("INSERT OR IGNORE INTO enrollments (id, student_id, course_id) VALUES (1, 1, 1), (2, 2, 2)")
    conn.commit()

# Display rows nicely aligned
def format_table(col_names, rows):
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(col_names, *rows)] if rows else [len(name) for name in col_names]
    header = " | ".join(f"{name:<{w}}" for name, w in zip(col_names, col_widths))
    print("\n" + header)
    print("-" * len(header))
    for row in rows:
        print(" | ".join(f"{str(cell):<{w}}" for cell, w in zip(row, col_widths)))
    print()

def list_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    return [row[0] for row in cursor.fetchall()]

# View table
def view_table():
    while True:
        tables = list_tables()
        if not tables:
            print("❌ No tables found.")
            return
        print("\n📋 Tables:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print(f"{len(tables)+1}. Go back")
        try:
            choice = int(input("Choose a table to view: "))
            if choice == len(tables)+1:
                return
            table_name = tables[choice - 1]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            if not rows:
                print(f"⚠️ Table '{table_name}' is empty.")
            else:
                format_table(col_names, rows)

            # Insert entry
            if input("Do you want to insert a new entry into this table? (y/n): ").lower() == 'y':
                values = [input(f"Value for '{col}': ") for col in col_names[1:]]
                placeholders = ','.join('?' * len(values))
                cursor.execute(f"INSERT INTO {table_name} ({', '.join(col_names[1:])}) VALUES ({placeholders})", values)
                conn.commit()
                print("✅ INSERTED")

            # Delete entry
            if input("Do you want to delete an entry from this table? (y/n): ").lower() == 'y':
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                format_table(col_names, rows)
                try:
                    row_num = int(input("Enter row number to delete (or 0 to go back): ")) - 1
                    if row_num == -1:
                        continue
                    id_val = rows[row_num][0]
                    cursor.execute(f"DELETE FROM {table_name} WHERE {col_names[0]} = ?", (id_val,))
                    conn.commit()
                    print("🗑️ Entry deleted successfully.")

                    # Resequence IDs
                    cursor.execute("BEGIN TRANSACTION;")
                    cursor.execute(f"CREATE TEMP TABLE temp_{table_name} AS SELECT * FROM {table_name};")
                    cursor.execute(f"DELETE FROM {table_name};")
                    columns_without_id = ', '.join(col_names[1:])
                    cursor.execute(f"INSERT INTO {table_name} ({columns_without_id}) SELECT {columns_without_id} FROM temp_{table_name};")
                    cursor.execute(f"DROP TABLE temp_{table_name};")
                    conn.commit()
                    print("🔄 IDs resequenced.")
                except Exception as e:
                    print("❌ Deletion failed:", e)
        except:
            print("❌ Invalid input.")

# Make a new table
def create_table():
    while True:
        name = input("Enter table name (or type 'back' to go back): ")
        if name.lower() == 'back':
            return
        cols = input("Enter columns (e.g., name TEXT, age INTEGER): ")
        try:
            cursor.execute(f"CREATE TABLE {name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {cols})")
            conn.commit()
            print(f"✅ Table '{name}' created.")
            return
        except Exception as e:
            print("❌ Error creating table:", e)

# Update a table
def update_table():
    while True:
        tables = list_tables()
        if not tables:
            print("❌ No tables found.")
            return
        print("\n📝 Tables:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print(f"{len(tables)+1}. Go back")
        try:
            choice = int(input("Choose a table to update: "))
            if choice == len(tables)+1:
                return
            table_name = tables[choice - 1]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            format_table(col_names, rows)

            row_num = int(input("Enter row number to update (or 0 to go back): ")) - 1
            if row_num == -1:
                return
            id_val = rows[row_num][0]
            for i in range(1, len(col_names)):
                new_val = input(f"New value for '{col_names[i]}' (leave blank to keep current): ")
                if new_val:
                    cursor.execute(f"UPDATE {table_name} SET {col_names[i]} = ? WHERE {col_names[0]} = ?", (new_val, id_val))
            conn.commit()
            print("✅ Entry updated.")
            return
        except Exception as e:
            print("❌ Update failed:", e)

# Delete a table
def delete_table():
    while True:
        tables = list_tables()
        if not tables:
            print("❌ No tables found.")
            return
        print("\n🗑️ Tables:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        print(f"{len(tables)+1}. Go back")
        try:
            choice = int(input("Choose a table to delete: "))
            if choice == len(tables)+1:
                return
            table_name = tables[choice - 1]
            confirm = input(f"⚠️ Are you sure you want to delete table '{table_name}'? (y/n): ")
            if confirm.lower() == 'y':
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                conn.commit()
                print(f"🗑️ Table '{table_name}' deleted.")
            return
        except Exception as e:
            print("❌ Error deleting table:", e)

# Main menu
def main_menu():
    create_demo_tables()
    while True:
        print("\n📚 UNIVERSITY STUDENT MANAGEMENT SYSTEM:")
        print("1. View a table")
        print("2. Make a new table")
        print("3. Update a table")
        print("4. Delete a table")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            view_table()
        elif choice == '2':
            create_table()
        elif choice == '3':
            update_table()
        elif choice == '4':
            delete_table()
        elif choice == '5':
            print("\nExiting...")
            break
        else:
            print("❌ Invalid option.")

main_menu()
