import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Cargar un archivo .env específico
env_file = os.path.join(os.path.dirname(__file__), '.env')  # Busca el .env en el mismo directorio que este archivo
load_dotenv(dotenv_path=env_file)

# Asegurarse de que las variables de entorno estén configuradas
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE')

print("Variables de entorno:")
print(DB_HOST, DB_USER, DB_PASSWORD, DATABASE)

if not all([DB_HOST, DB_USER, DB_PASSWORD, DATABASE]):
    raise EnvironmentError("Faltan variables de entorno necesarias para la configuración de la base de datos.")

class PostgreSQLConnection:
    def __init__(self, db):
        self.connection = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
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