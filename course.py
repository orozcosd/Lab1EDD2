# course.py
# Clase que representa un curso de Udemy
# Autores: [Tu equipo aquí]

class Course:
    """
    Representa un curso del dataset de Udemy.
    El nivel de satisfacción es la métrica usada para comparación en el árbol AVL.
    """

    def __init__(self, id, title, url, rating, num_reviews, num_published_lectures,
                 created, last_update_date, duration, instructors_id, image,
                 positive_reviews, negative_reviews, neutral_reviews):
        self.id = int(id)
        self.title = str(title)
        self.url = str(url)
        self.rating = float(rating) if rating != '' else 0.0
        self.num_reviews = int(num_reviews) if num_reviews != '' else 0
        self.num_published_lectures = int(num_published_lectures) if num_published_lectures != '' else 0
        self.created = str(created)
        self.last_update_date = str(last_update_date)
        self.duration = str(duration)
        self.instructors_id = str(instructors_id)
        self.image = str(image)
        self.positive_reviews = int(positive_reviews) if positive_reviews != '' else 0
        self.negative_reviews = int(negative_reviews) if negative_reviews != '' else 0
        self.neutral_reviews = int(neutral_reviews) if neutral_reviews != '' else 0
        self.satisfaction = self._calculate_satisfaction()

    def _calculate_satisfaction(self):
        """
        Calcula el nivel de satisfacción del curso con 5 decimales de precisión.
        Fórmula: satisfaction = rating * 0.7 +
                 ((5*positive + 3*neutral + negative) / num_reviews) * 0.3
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