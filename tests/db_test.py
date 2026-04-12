import mariadb
from typing import Literal

Show_What = Literal["Notes", "TODOs"]

from test_config import test_db_name, db_config

# with mariadb.connect(**db_config) as conn:
#     print(conn.character_set)


def create_test(cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL UNIQUE
        )
    """)
    print("Executed creation of Users")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL
        )
    """)
    print("Executed creation of Notes")
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TODOs(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            task_done BOOLEAN NOT NULL
        )
    """)
    print("Executed creation of TODOs \n")

def insert_test(cursor) -> None:
    print("Inserting rows...")

    insert_query = "INSERT INTO Notes (title, description) VALUES (?, ?)"

    # parametized - no SQL injection attack
    cursor.execute(insert_query, ("Notat", "test test her"))
    cursor.execute(insert_query, ("Temp 2FA kode", "Falsk nyhet?"))
    print(f"Row count inserted: {cursor.rowcount}")

def select_test(cursor, show_what: Show_What):
    select_query = f"SELECT * FROM {show_what}"

    cursor.execute(select_query)
    return cursor.fetchall()
    
    # for row in cursor:
        # print(row)

def patch_test(cursor) -> None:
    print("Patching row...")

    patch_query = "UPDATE Notes SET title = ?, description = ? WHERE id = ?"
    cursor.execute(patch_query, ("Tester igjen", "testing igjen", 1))
    print("Patched row")

def delete_test(cursor) -> None:
    print("Deleting row...")

    delete_query = "DELETE FROM Notes WHERE id = ?"
    cursor.execute(delete_query, [2])
    cursor.execute(delete_query, [3])  # data argument as list. As tuple doesn't work
    print("Deleted row")

def main() -> None:
    cursor = None
    conn = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        create_test(cursor)
        # insert_test(cursor)
        # patch_test(cursor)
        # delete_test(cursor)
        todos = select_test(cursor, show_what="TODOs")
        print(f"TODOs: {todos}")

        todo_tasks = {"tasks": []}
        partial_todos = []

        for parent in todos:
            # print(parent)

            todo_tasks["tasks"].append({
                "description": parent.get("description"),
                "task_done": parent.get("task_done")
            })
            partial_todos.append({
                "id": parent.get("id"),
                "title": parent.get("title")
            })

        # print(f"Attempting tasks list over description and task done: tasks: {todos_tasks}")
        updated_todos = {
            "id_title": partial_todos,
            "tasks": todo_tasks["tasks"]
        }
        
        print(updated_todos, "\n")
    except mariadb.IntegrityError as ierr:
        print("NULL value detected while inserting?", ierr)
        conn.rollback()
    except mariadb.Error as err:
        print("Database test failed!", err)
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
            print("Closed cursor")
        if conn:
            conn.close()
            print("Closed connection")


if __name__ == "__main__":
    main()
