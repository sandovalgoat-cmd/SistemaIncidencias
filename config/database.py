import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="127.0.0.2",
        port=3306,
        user="root",
        password="",
        database="SistemaIncidencias"
    )