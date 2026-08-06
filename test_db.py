from config.database import conectar

try:

    conexion = conectar()

    print("Conexión exitosa")

    conexion.close()

except Exception as e:

    print(e)
    