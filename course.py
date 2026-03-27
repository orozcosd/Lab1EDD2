# course.py
# Clase que representa un curso de Udemy
#Sección docuemtada por : Keymer Peréz.


class Course:
    """
    Esta clase es el "molde" para crear objetos que representan
    cada curso del dataset de Udemy.
    Cada vez que se lee una fila del CSV, se crea un objeto Course con esos datos.
    El nivel de satisfacción es la métrica usada para ordenar los cursos en el árbol AVL.
    Representa un curso del dataset de Udemy.
    El nivel de satisfacción es la métrica usada para comparación en el árbol AVL.
    """

    def __init__(self, id, title, url, rating, num_reviews, num_published_lectures,
                 created, last_update_date, duration, instructors_id, image,
                 positive_reviews, negative_reviews, neutral_reviews):
        
        """
        Constructor: se ejecuta automáticamente al crear un objeto Course.
        Recibe todos los datos del curso como texto (strings) provenientes del CSV,
        y los convierte al tipo de dato adecuado para cada atributo.

        Si un campo viene vacío (''), se asigna un valor por defecto (0 o 0.0)
        para evitar errores al hacer cálculos.
        """    
        #Identificación del curso
        self.id = int(id) #Id
        self.title = str(title)#Titulo del curso
        self.url = str(url)#Enlace al curso en Udemy

        #Métricas de calidad
        #Si el rating esta vacío se asume 0.0 para no romper el caculo
        self.rating = float(rating) if rating != '' else 0.0

        #Reseñas
        self.num_reviews = int(num_reviews) if num_reviews != '' else 0
        self.positive_reviews = int(positive_reviews) if positive_reviews != '' else 0
        self.negative_reviews = int(negative_reviews) if negative_reviews != '' else 0
        self.neutral_reviews = int(neutral_reviews) if neutral_reviews != '' else 0

        #Contenido del curso
        #Número de clases publicadas(si es vaciop se asume 0)
        self.num_published_lectures = int(num_published_lectures) if num_published_lectures != '' else 0
        self.duration = str(duration)#duracion total curso
        
        #Fechas
        self.created = str(created) #Fecha de creación
        self.last_update_date = str(last_update_date) #Fecha de última actualización
  
        #Información del instructor
        self.instructors_id = str(instructors_id) #id instructor
        self.image = str(image) #ruta de la imagen

        #Metrica principal para el árbl AVL
        #se calcula al final, una vez que todos los atributos ya están asignados
        self.satisfaction = self._calculate_satisfaction()

    def _calculate_satisfaction(self):
        """
        Calcula el nivel de satisfacción del curso con 5 decimales de precisión.
        Fórmula: satisfaction = rating * 0.7 +
                 ((5*positive + 3*neutral + negative) / num_reviews) * 0.3
        Caso especial: si el curso no tiene reseñas, se usa solo el rating * 0.7
        para no dividir entre cero. 
        El resultado se redondea a 5 decimales de precisión como es requerido por el profe        
        """
        if self.num_reviews == 0:
            return round(self.rating * 0.7, 5)
        review_score = (
            5 * self.positive_reviews +
            3 * self.neutral_reviews +
            self.negative_reviews
        ) / self.num_reviews
        return round(self.rating * 0.7 + review_score * 0.3, 5)

    def __str__(self):
        """
        Define cómo se ve un objeto Course cuando se imprime con print().
        Muestra toda la información del curso de forma legible.

        Ejemplo de uso:
            curso = Course(...)
            print(curso)   ← llama automáticamente a este método
        """        
        return (f"ID: {self.id}\n"
                f"Título: {self.title}\n"
                f"URL: {self.url}\n"
                f"Rating: {self.rating}\n"
                f"Satisfacción: {self.satisfaction}\n"
                f"Reseñas totales: {self.num_reviews}\n"
                f"Reseñas positivas: {self.positive_reviews}\n"
                f"Reseñas negativas: {self.negative_reviews}\n"
                f"Reseñas neutras: {self.neutral_reviews}\n"
                f"Clases publicadas: {self.num_published_lectures}\n"
                f"Creado: {self.created}\n"
                f"Última actualización: {self.last_update_date}\n"
                f"Duración: {self.duration}\n"
                f"Instructor ID: {self.instructors_id}")