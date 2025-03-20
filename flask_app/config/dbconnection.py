import psycopg2
from psycopg2.extras import RealDictCursor

class PostgreSQLConnection:
    def __init__(self, db):
        self.connection = psycopg2.connect(
            host='localhost',
            user='postgres',  # Cambia esto si usas otro usuario
            password='password',  # Cambia esto por tu contraseña
            database=db
        )
        self.connection.autocommit = True

    def query_db(self, query, data=None):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(query, data)
                if query.lower().startswith("insert"):
                    return cursor.fetchone()['id'] if cursor.description else None
                elif query.lower().startswith("select"):
                    return cursor.fetchall()
                else:
                    return None
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                self.connection.close()

def connectToPostgreSQL(db):
    return PostgreSQLConnection(db)