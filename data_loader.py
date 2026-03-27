# data_loader.py
# Módulo para cargar el dataset CSV de cursos de Udemy
#Sección documentada por : Santiago Orozco


import pandas as pd   # Librería que facilita leer y manejar archivos CSV
from course import Course   # Clase que representa un curso


def load_courses(csv_path):
    """
    Esta función recibe la ruta del archivo CSV
    y devuelve un diccionario con esta forma:

        { id_del_curso : objeto_Course }

    Es decir, convierte cada fila del CSV en un objeto Course.
    También limpia datos faltantes para evitar errores.
    """

    # Leemos el archivo CSV usando pandas
    df = pd.read_csv(csv_path, low_memory=False)
    # ─────────────────────────────────────────────────────
    # LIMPIEZA DE DATOS (muy importante)
    # ─────────────────────────────────────────────────────
    # Muchas filas del CSV pueden tener datos vacíos o mal escritos.
    # Aquí los corregimos para que el programa no se dañe.

    # Convertimos a número la columna 'rating'.
    # Si hay errores, los reemplaza por 0.0
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)

    # Convertimos a enteros varias columnas numéricas
    df['num_reviews'] = pd.to_numeric(df['num_reviews'], errors='coerce').fillna(0).astype(int)
    df['num_published_lectures'] = pd.to_numeric(df['num_published_lectures'], errors='coerce').fillna(0).astype(int)
    df['positive_reviews'] = pd.to_numeric(df['positive_reviews'], errors='coerce').fillna(0).astype(int)
    df['negative_reviews'] = pd.to_numeric(df['negative_reviews'], errors='coerce').fillna(0).astype(int)
    df['neutral_reviews'] = pd.to_numeric(df['neutral_reviews'], errors='coerce').fillna(0).astype(int)

    # Para las columnas de texto, si están vacías, ponemos valores por defecto
    df['created'] = df['created'].fillna('').astype(str)
    df['last_update_date'] = df['last_update_date'].fillna('').astype(str)
    df['duration'] = df['duration'].fillna('').astype(str)
    df['instructors_id'] = df['instructors_id'].fillna('').astype(str)
    df['image'] = df['image'].fillna('').astype(str)
    df['title'] = df['title'].fillna('Sin título').astype(str)
    df['url'] = df['url'].fillna('').astype(str)

    # ─────────────────────────────────────────────────────
    # CREACIÓN DE LOS OBJETOS COURSE
    # ─────────────────────────────────────────────────────

    courses = {} # Diccionario donde guardaremos todos los cursos

    # Recorremos fila por fila el datase
    for _, row in df.iterrows():
        try:
            # Creamos un objeto Course usando la información de la fila
            course = Course(
                id=int(row['id']),
                title=row['title'],
                url=row['url'],
                rating=row['rating'],
                num_reviews=row['num_reviews'],
                num_published_lectures=row['num_published_lectures'],
                created=row['created'],
                last_update_date=row['last_update_date'],
                duration=row['duration'],
                instructors_id=row['instructors_id'],
                image=row['image'],
                positive_reviews=row['positive_reviews'],
                negative_reviews=row['negative_reviews'],
                neutral_reviews=row['neutral_reviews']
            )
             # Guardamos el curso en el diccionario usando su ID como clave 
            courses[course.id] = course
        except Exception as e:
            # Si una fila tiene un problema, no detiene el programa.
            # Solo muestra el error y continúa con la siguiente.  
 
            print(f"Error al cargar fila con id={row.get('id', '?')}: {e}")
    # Mensaje final indicando cuántos cursos se cargaron correctamente
    print(f"Dataset cargado: {len(courses)} cursos.")


    # Retornamos el diccionario con todos los cursos
    return courses