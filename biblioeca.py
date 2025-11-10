import sqlite3

# ============================================================
# Aplicación de Biblioteca Personal
# Autor: Kayder Murillo
# Descripción: Programa de línea de comandos que administra
# libros en una base de datos SQLite.
# ============================================================

def conectar():
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            estado TEXT CHECK(estado IN ('Leído','No leído')) NOT NULL
        )
    ''')
    conexion.commit()
    return conexion

def agregar_libro(conexion):
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado (Leído/No leído): ")
    
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO libros (titulo, autor, genero, estado) VALUES (?, ?, ?, ?)",
        (titulo, autor, genero, estado)
    )
    conexion.commit()
    print("Libro agregado correctamente.\n")

def actualizar_libro(conexion):
    ver_libros(conexion)
    id_libro = input("Ingrese el ID del libro que desea actualizar: ")
    nuevo_titulo = input("Nuevo título: ")
    nuevo_autor = input("Nuevo autor: ")
    nuevo_genero = input("Nuevo género: ")
    nuevo_estado = input("Nuevo estado (Leído/No leído): ")
    
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE libros
        SET titulo = ?, autor = ?, genero = ?, estado = ?
        WHERE id = ?
    ''', (nuevo_titulo, nuevo_autor, nuevo_genero, nuevo_estado, id_libro))
    conexion.commit()
    print("Libro actualizado exitosamente.\n")

def eliminar_libro(conexion):
    ver_libros(conexion)
    id_libro = input("Ingrese el ID del libro que desea eliminar: ")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
    conexion.commit()
    print("Libro eliminado.\n")

def ver_libros(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    
    if libros:
        print("\nLISTADO DE LIBROS:")
        print("-" * 60)
        for libro in libros:
            print(f"ID: {libro[0]} | Título: {libro[1]} | Autor: {libro[2]} | Género: {libro[3]} | Estado: {libro[4]}")
        print("-" * 60 + "\n")
    else:
        print("\nNo hay libros registrados.\n")

def buscar_libro(conexion):
    campo = input("Buscar por (titulo/autor/genero): ").lower()
    termino = input(f"Ingrese el {campo} que desea buscar: ")
    
    cursor = conexion.cursor()
    consulta = f"SELECT * FROM libros WHERE {campo} LIKE ?"
    cursor.execute(consulta, (f"%{termino}%",))
    resultados = cursor.fetchall()
    
    if resultados:
        print("\nRESULTADOS DE BÚSQUEDA:")
        for libro in resultados:
            print(f"ID: {libro[0]} | Título: {libro[1]} | Autor: {libro[2]} | Género: {libro[3]} | Estado: {libro[4]}")
        print()
    else:
        print("No se encontraron libros que coincidan.\n")

def menu():
    conexion = conectar()
    while True:
        print("========= MENÚ BIBLIOTECA PERSONAL =========")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")
        print("=============================================")
        
        opcion = input("Seleccione una opción (1-6): ")
        print()
        
        if opcion == "1":
            agregar_libro(conexion)
        elif opcion == "2":
            actualizar_libro(conexion)
        elif opcion == "3":
            eliminar_libro(conexion)
        elif opcion == "4":
            ver_libros(conexion)
        elif opcion == "5":
            buscar_libro(conexion)
        elif opcion == "6":
            print("Saliendo del programa...")
            conexion.close()
            break
        else:
            print("Opción inválida. Intente de nuevo.\n")

if __name__ == "__main__":
    menu()
