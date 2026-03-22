# data_loader.py
# Módulo para cargar el dataset CSV de cursos de Udemy


import pandas as pd
from course import Course


def load_courses(csv_path):
    """
    Carga el dataset CSV y retorna un diccionario {id: Course}.
    Maneja valores faltantes con valores por defecto.
    """
    df = pd.read_csv(csv_path, low_memory=False)

    # Rellenar valores faltantes
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)
    df['num_reviews'] = pd.to_numeric(df['num_reviews'], errors='coerce').fillna(0).astype(int)
    df['num_published_lectures'] = pd.to_numeric(df['num_published_lectures'], errors='coerce').fillna(0).astype(int)
    df['positive_reviews'] = pd.to_numeric(df['positive_reviews'], errors='coerce').fillna(0).astype(int)
    df['negative_reviews'] = pd.to_numeric(df['negative_reviews'], errors='coerce').fillna(0).astype(int)
    df['neutral_reviews'] = pd.to_numeric(df['neutral_reviews'], errors='coerce').fillna(0).astype(int)
    df['created'] = df['created'].fillna('').astype(str)
    df['last_update_date'] = df['last_update_date'].fillna('').astype(str)
    df['duration'] = df['duration'].fillna('').astype(str)
    df['instructors_id'] = df['instructors_id'].fillna('').astype(str)
    df['image'] = df['image'].fillna('').astype(str)
    df['title'] = df['title'].fillna('Sin título').astype(str)
    df['url'] = df['url'].fillna('').astype(str)

    courses = {}
    for _, row in df.iterrows():
        try:
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
            courses[course.id] = course
        except Exception as e:
            print(f"Error al cargar fila con id={row.get('id', '?')}: {e}")

    print(f"✅ Dataset cargado: {len(courses)} cursos.")
    return courses