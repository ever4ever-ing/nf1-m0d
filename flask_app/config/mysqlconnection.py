import pymysql.cursors
import os
from dotenv import load_dotenv
env_file = os.getenv('ENV_FILE', '.env')  # Por defecto, carga .env
load_dotenv(dotenv_path=env_file)

# Asegurarse de que las variables de entorno estén configuradas
DB_HOST = os.getenv('MYSQLHOST')
DB_USER = os.getenv('MYSQLUSER')
DB_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
DATABASE = os.getenv('MYSQL_DATABASE')


class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)