from database.connection import connect_database

def insert_picture(base64_str):
    try:
        database_connection = connect_database()
        query = database_connection.cursor()

        query.execute("""
            INSERT INTO picture (person_id, base64_image)
            VALUES (
            (SELECT id FROM person WHERE email = 'admin@example.com'),
            %(base64)s
            )
        """, {'base64': base64_str})

        database_connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if database_connection is not None:
            database_connection.close()