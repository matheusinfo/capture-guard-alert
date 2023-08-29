from database.connection import connect_database

def seed_tables():
    try:
        database_connection = connect_database()
        query = database_connection.cursor()

        query.execute("""
            INSERT INTO person (name, email, password)
                VALUES ('admin', 'admin@example.com', 'admin_password')
            ON CONFLICT (email) DO NOTHING;
        """)

        database_connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if database_connection is not None:
            database_connection.close()