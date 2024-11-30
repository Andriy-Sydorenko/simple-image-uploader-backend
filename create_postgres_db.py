import psycopg2
from psycopg2 import sql

import config


def create_database():
    conn = None
    try:
        # Connect to the default 'postgres' database
        conn = psycopg2.connect(
            dbname="postgres",
            user=config.LOCAL_POSTGRES_SUPERUSER,
            password=config.LOCAL_POSTGRES_PASSWORD,
            host=config.LOCAL_DB_HOST,
            port=config.LOCAL_DB_PORT,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Create the database
        cursor.execute(sql.SQL("CREATE DATABASE {dbname};").format(dbname=sql.Identifier(config.LOCAL_DB_NAME)))
        print(f"Database '{config.LOCAL_DB_NAME}' created successfully.")

        # Create the user
        cursor.execute(
            sql.SQL("CREATE USER {user} WITH PASSWORD %s;").format(user=sql.Identifier(config.LOCAL_DB_USER)),
            [config.LOCAL_DB_PASSWORD],
        )
        print(f"User '{config.LOCAL_DB_USER}' created successfully.")

        # Grant privileges to the user
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {user};").format(
                dbname=sql.Identifier(config.LOCAL_DB_NAME),
                user=sql.Identifier(config.LOCAL_DB_USER),
            )
        )
        print(f"Privileges granted to user '{config.LOCAL_DB_USER}' on database '{config.LOCAL_DB_NAME}'.")

        # Close connections
        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"An error occurred while creating the database: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_database()
