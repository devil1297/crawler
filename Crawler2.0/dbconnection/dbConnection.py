import mysql.connector
host = 'localhost'
user = 'root'
password = '@q18I0V6zDyaxFLJ'
db = 'CHIENSI3'

def connect():
    connection = mysql.connector.connect(host=host, database=db, user=user, password=password)
    return connection.cursor(buffered=True)

