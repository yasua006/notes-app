import mariadb

from test_config import test_db_name, db_config

# with mariadb.connect(**db_config) as conn:
#     print(conn.character_set)


def create_test(cursor) -> None:
    print(f"Connected to database {test_db_name}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL
        )
    """)
    print("Executed creation of Notes")

def insert_test(cursor) -> None:
    print("Inserting rows...")

    insert_query = "INSERT INTO Notes (title, description) VALUES (?, ?)"

    # parametized - no SQL injection attack
    cursor.execute(insert_query, ("Notat", "test test her"))
    cursor.execute(insert_query, ("Temp 2FA kode", "Falsk nyhet?"))
    print(f"Row count inserted: {cursor.rowcount}")

def select_test(cursor) -> None:
    select_query = "SELECT * FROM Notes"

    cursor.execute(select_query)

    for row in cursor:
        print("Note:", row)

def delete_test(cursor) -> None:
    print("Deleting row...")

    delete_query = "DELETE FROM Notes WHERE id = ?"
    cursor.execute(delete_query, [2])
    cursor.execute(delete_query, [3])  # data argument as list, as tuple doesn't work

def main() -> None:
    cursor = None
    conn = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        create_test(cursor)
        # insert_test(cursor)
        # delete_test(cursor)
        # select_test(cursor)
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