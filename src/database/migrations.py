from database.connection import connect_database

def create_tables():
    try:
        database_connection = connect_database()
        query = database_connection.cursor()

        query.execute("""
            CREATE TABLE IF NOT EXISTS person (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)

        query.execute("""
            CREATE TABLE IF NOT EXISTS picture (
                id SERIAL PRIMARY KEY,
                person_id INTEGER REFERENCES person(id),
                base64_image TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        database_connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if database_connection is not None:
            database_connection.close()