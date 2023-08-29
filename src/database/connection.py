import os, psycopg2

def connect_database():
    # Load environment variables
    DB_DATABASE = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')

    # Connect to the database
    try:
        database_connection = psycopg2.connect(
            database=DB_DATABASE,
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
        )

        return database_connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)