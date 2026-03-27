# avl_tree.py
# Implementación del árbol AVL auto-balanceado
# Sección documentada por : Juan Salcedo

from graphviz import Digraph
import os

class AVLNode:
    """
    Nodo del árbol AVL. Almacena un curso y metadatos del árbol.

    En este nodo se guarda:
    - La información de un curso
    - Una referencia a su hijo izquierdo (cursos con menor satisfacción)
    - Una referencia a su hijo derecho (cursos con mayor satisfacción)
    - Su propia altura dentro del árbol (para saber si está balanceado)
    """

    def __init__(self, course):
        self.course = course          # Objeto Course
        self.left = None              # Hijo izquierdo
        self.right = None             # Hijo derecho
        self.height = 1              # Altura del nodo (hoja = 1)


class AVLTree:
    """
    Árbol AVL auto-balanceado donde la clave de comparación
    es el nivel de satisfacción del curso. En caso de empate se usa el ID.
    """

    def __init__(self):
        self.root = None

    # ─────────────────────────────────────────────
    # Utilidades básicas
    # ─────────────────────────────────────────────

    def _height(self, node):
        """
        Retorna la altura de un nodo (0 si es None).
        Si el nodo no existe (None), su altura es 0.
        Si existe, devuelve la altura guardada en el nodo.
        """
        return node.height if node else 0

    def _balance_factor(self, node):
        """
        Factor de balanceo = altura(der) - altura(izq).
        Se calcula como: altura del lado derecho - altura del lado izquierdo.
        """
        if not node:
            return 0
        return self._height(node.right) - self._height(node.left)

    def _update_height(self, node):
        """
        Actualiza la altura de un nodo según sus hijos.
        Después de insertar o eliminar, recalcula la altura del nodo.
        La altura de un nodo = 1 + la altura del hijo más alto.
        """
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _compare(self, course_a, course_b):
        """
        Compara dos cursos por satisfacción. Primero compara por satisfacción. Si empatan, desempata por ID.
        Retorna: -1 si a < b, 0 si a == b, 1 si a > b
        """
        if course_a.satisfaction < course_b.satisfaction:
            return -1
        elif course_a.satisfaction > course_b.satisfaction:
            return 1
        else:
            if course_a.id < course_b.id:
                return -1
            elif course_a.id > course_b.id:
                return 1
            return 0

    # ─────────────────────────────────────────────
    # Rotaciones AVL
    # ─────────────────────────────────────────────

    def _rotate_right(self, y):
        """Rotación simple a la derecha."""
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        """Rotación simple a la izquierda."""
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node):
        """
        Aplica las rotaciones necesarias para mantener el balance AVL.
         1. Izquierda (I): el desequilibrio está hacia la izquierda.
           → Rotar a la derecha.

        2. Izquierda-Derecha (ID): el desequilibrio está en el hijo izquierdo, pero hacia su derecha.
           → Primero rotar izquierda el hijo, luego rotar derecha el nodo.

        3. Derecha (D): el desequilibrio está hacia la derecha.
           → Rotar a la izquierda.

        4. Derecha-Izquierda (DI): el desequilibrio está en el hijo derecho, pero hacia su izquierda.
           → Primero rotar derecha el hijo, luego rotar izquierda el nodo.
        """
        self._update_height(node)
        bf = self._balance_factor(node)

        # Caso Izquierda-Izquierda
        if bf > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)

        # Caso Izquierda-Derecha
        if bf > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Caso Derecha-Derecha
        if bf < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)

        # Caso Derecha-Izquierda
        if bf < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # ─────────────────────────────────────────────
    # Inserción
    # ─────────────────────────────────────────────

    def insert(self, course):
        """Inserta un curso en el árbol AVL."""
        self.root = self._insert(self.root, course)

    def _insert(self, node, course):
        """
        Inserción recursiva. Funciona así:
        1. Si el nodo actual está vacío, crea un nodo nuevo aquí.
        2. Si el curso es menor, va al subárbol izquierdo.
        3. Si el curso es mayor, va al subárbol derecho.
        4. Si es igual (mismo ID y satisfacción), actualiza el nodo existente.
        5. Al regresar de la recursión, rebalancea el árbol si es necesario.
        """        
        if not node:
            return AVLNode(course)
        cmp = self._compare(course, node.course)
        if cmp < 0:
            node.left = self._insert(node.left, course)
        elif cmp > 0:
            node.right = self._insert(node.right, course)
        else:
            # Curso duplicado: actualizar
            node.course = course
            return node
        return self._rebalance(node)

    # ─────────────────────────────────────────────
    # Eliminación
    # ─────────────────────────────────────────────

    def delete_by_id(self, course_id):
        """Elimina un nodo buscando por ID del curso."""
        node = self._find_by_id(self.root, course_id)
        if not node:
            return False
        self.root = self._delete(self.root, node.course)
        return True

    def delete_by_satisfaction(self, satisfaction):
        """Elimina un nodo buscando por satisfacción (elimina el primero encontrado)."""
        nodes = self._find_by_satisfaction(self.root, satisfaction, [])
        if not nodes:
            return False
        self.root = self._delete(self.root, nodes[0].course)
        return True

    def _delete(self, node, course):
        """
        
        Elimina un nodo del árbol y lo rebalancea.
        Hay tres situaciones posibles al encontrar el nodo:
        
        1. Solo tiene hijo derecho → el hijo derecho "sube" y lo reemplaza.
        2. Solo tiene hijo izquierdo → el hijo izquierdo "sube" y lo reemplaza.
        3. Tiene dos hijos → busca el "sucesor in-order" (el menor del subárbol derecho),
           copia sus datos en el nodo actual y elimina al sucesor.
        
        Al finalizar, rebalancea el árbol.        
        """
        if not node:
            return None
        cmp = self._compare(course, node.course)
        if cmp < 0:
            node.left = self._delete(node.left, course)
        elif cmp > 0:
            node.right = self._delete(node.right, course)
        else:
            # Nodo encontrado
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # Nodo con dos hijos: reemplazar con el sucesor in-order
            successor = self._min_node(node.right)
            node.course = successor.course
            node.right = self._delete(node.right, successor.course)
        return self._rebalance(node)

    def _min_node(self, node):
        """Retorna el nodo con el valor mínimo (más a la izquierda)."""
        while node.left:
            node = node.left
        return node

    # ─────────────────────────────────────────────
    # Búsqueda
    # ─────────────────────────────────────────────

    def search_by_id(self, course_id):
        """Busca un nodo por ID del curso. Retorna el AVLNode o None."""
        return self._find_by_id(self.root, course_id)

    def _find_by_id(self, node, course_id):
        """Búsqueda recursiva por ID."""
        if not node:
            return None
        if node.course.id == course_id:
            return node
        left_result = self._find_by_id(node.left, course_id)
        if left_result:
            return left_result
        return self._find_by_id(node.right, course_id)

    def search_by_satisfaction(self, satisfaction):
        """Busca nodos por nivel de satisfacción. Retorna lista de AVLNodes."""
        return self._find_by_satisfaction(self.root, satisfaction, [])

    def _find_by_satisfaction(self, node, satisfaction, results):
        """Búsqueda recursiva por satisfacción."""
        if not node:
            return results
        if abs(node.course.satisfaction - satisfaction) < 1e-9:
            results.append(node)
        self._find_by_satisfaction(node.left, satisfaction, results)
        self._find_by_satisfaction(node.right, satisfaction, results)
        return results

    # ─────────────────────────────────────────────
    # Búsquedas por criterios (operación 4)
    # ─────────────────────────────────────────────

    def search_positive_greater_than_neg_plus_neutral(self):
        """
        4a. Devuelve cursos donde: reseñas_positivas > (negativas + neutras)
        Es decir, cursos con más "pulgares arriba" que todo lo demás combinado.
        """
        results = []
        self._traverse_criteria_a(self.root, results)
        return results

    def _traverse_criteria_a(self, node, results):
        if not node:
            return
        c = node.course
        if c.positive_reviews > (c.negative_reviews + c.neutral_reviews):
            results.append(node)
        self._traverse_criteria_a(node.left, results)
        self._traverse_criteria_a(node.right, results)

    def search_created_after(self, date_str):
        """
        4b. Devuelve cursos creados DESPUÉS de una fecha dada.
        La fecha debe ser en formato "YYYY-MM-DD" (ej: "2020-01-01").
        Funciona comparando strings, lo cual es válido en formato ISO.
        """
        results = []
        self._traverse_criteria_b(self.root, date_str, results)
        return results

    def _traverse_criteria_b(self, node, date_str, results):
        if not node:
            return
        try:
            created = node.course.created[:10]  # Solo YYYY-MM-DD
            if created > date_str:
                results.append(node)
        except Exception:
            pass
        self._traverse_criteria_b(node.left, date_str, results)
        self._traverse_criteria_b(node.right, date_str, results)

    def search_lectures_in_range(self, min_lec, max_lec):
        """
        4c. Devuelve cursos cuya cantidad de clases esté dentro del rango [min_lec, max_lec].
        Por ejemplo: cursos con entre 10 y 50 clases.
        """
        results = []
        self._traverse_criteria_c(self.root, min_lec, max_lec, results)
        return results

    def _traverse_criteria_c(self, node, min_lec, max_lec, results):
        if not node:
            return
        lec = node.course.num_published_lectures
        if min_lec <= lec <= max_lec:
            results.append(node)
        self._traverse_criteria_c(node.left, min_lec, max_lec, results)
        self._traverse_criteria_c(node.right, min_lec, max_lec, results)

    def search_reviews_above_average(self, review_type):
        """
        4d. Devuelve cursos cuyas reseñas (positivas, negativas o neutras)
        estén por encima del promedio de todos los cursos del árbol.

        Pasos:
        1. Recolecta todos los nodos.
        2. Calcula el promedio del tipo de reseña pedido.
        3. Filtra los que superan ese promedio.
        """
        all_nodes = self._get_all_nodes(self.root, [])
        if not all_nodes:
            return []
        if review_type == 'positive':
            avg = sum(n.course.positive_reviews for n in all_nodes) / len(all_nodes)
            return [n for n in all_nodes if n.course.positive_reviews > avg]
        elif review_type == 'negative':
            avg = sum(n.course.negative_reviews for n in all_nodes) / len(all_nodes)
            return [n for n in all_nodes if n.course.negative_reviews > avg]
        elif review_type == 'neutral':
            avg = sum(n.course.neutral_reviews for n in all_nodes) / len(all_nodes)
            return [n for n in all_nodes if n.course.neutral_reviews > avg]
        return []

    def _get_all_nodes(self, node, results):
        if not node:
            return results
        results.append(node)
        self._get_all_nodes(node.left, results)
        self._get_all_nodes(node.right, results)
        return results

    # ─────────────────────────────────────────────
    # Recorrido por niveles 
    # ─────────────────────────────────────────────

    def level_order(self):
        """Recorre el árbol nivel por nivel, como si leyeras un libro renglón a renglón.
        Devuelve una lista de listas: cada lista interna = los IDs de un nivel."""
        levels = []
        self._level_order_recursive([self.root], levels)
        return levels

    def _level_order_recursive(self, current_level_nodes, levels):
        """
        Recorrido por niveles de manera recursiva.
        - Recibe la lista de nodos del nivel actual.
        - Extrae sus IDs.
        - Arma la lista de nodos del siguiente nivel.
        - Se llama a sí mismo con ese siguiente nivel.
        """
        if not current_level_nodes:
            return
        ids = []
        next_level = []
        for node in current_level_nodes:
            if node:
                ids.append(node.course.id)
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
        if ids:
            levels.append(ids)
        self._level_order_recursive(next_level, levels)

    # ─────────────────────────────────────────────
    # Operaciones sobre nodo seleccionado
    # ─────────────────────────────────────────────

    def get_node_level(self, target_node):
        """Obtiene el nivel del nodo en el árbol (raíz = nivel 0)."""
        return self._find_level(self.root, target_node.course, 0)

    def _find_level(self, node, course, level):
        """Búsqueda recursiva del nivel de un nodo: va bajando y sumando 1 por cada piso."""
        if not node:
            return -1
        if node.course.id == course.id:
            return level
        left = self._find_level(node.left, course, level + 1)
        if left != -1:
            return left
        return self._find_level(node.right, course, level + 1)

    def get_node_balance_factor(self, target_node):
        """Retorna el factor de balanceo de un nodo dado."""
        node = self._find_by_id(self.root, target_node.course.id)
        if node:
            return self._balance_factor(node)
        return None

    def get_parent(self, target_node):
        """Encuentra el padre del nodo de manera recursiva."""
        return self._find_parent(self.root, target_node.course.id, None)

    def _find_parent(self, node, course_id, parent):
        """Búsqueda recursiva del padre."""
        if not node:
            return None
        if node.course.id == course_id:
            return parent
        left = self._find_parent(node.left, course_id, node)
        if left is not None:
            return left
        return self._find_parent(node.right, course_id, node)

    def get_grandparent(self, target_node):
        """Encuentra el abuelo del nodo. Simplemente llama dos veces a get_parent."""
        parent = self.get_parent(target_node)
        if parent:
            return self.get_parent(parent)
        return None

    def get_uncle(self, target_node):
        """Encuentra el tío del nodo de manera recursiva."""
        parent = self.get_parent(target_node)
        if not parent:
            return None
        grandparent = self.get_grandparent(target_node)
        if not grandparent:
            return None
        if grandparent.left and grandparent.left.course.id == parent.course.id:
            return grandparent.right
        return grandparent.left

    # ─────────────────────────────────────────────
    # Visualización con Graphviz
    # ─────────────────────────────────────────────

    def visualize(self, filename="avl_tree", highlight_ids=None):
        """
        Dibuja el árbol como una imagen PNG usando la librería Graphviz.
        
        - Los nodos normales aparecen en azul claro.
        - Los nodos resaltados (highlight_ids) aparecen en dorado.
        - Cada nodo muestra: ID, título (primeros 25 caracteres) y satisfacción.
        """
        dot = Digraph(comment='AVL Tree', format='png')
        dot.attr(rankdir='TB', size='20,20')
        dot.attr('node', shape='box', style='filled', fontname='Arial', fontsize='10')

        if not self.root:
            dot.node('empty', 'Árbol vacío', fillcolor='#f0f0f0')
        else:
            highlight_ids = highlight_ids or []
            self._add_nodes_to_graph(dot, self.root, highlight_ids)

        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        dot.render(output_path, cleanup=True)
        return output_path + '.png'

    def _add_nodes_to_graph(self, dot, node, highlight_ids):
        """Agrega nodos y aristas al grafo de Graphviz. Recorre el árbol recursivamente y agrega cada nodo al grafo.
        También agrega las aristas (flechas) que conectan padres con hijos."""
        if not node:
            return
        c = node.course
        label = f"ID: {c.id}\n{c.title[:25]}...\nSat: {c.satisfaction}"
        node_id = str(c.id)

        # Color según si está resaltado o no
        if c.id in highlight_ids:
            dot.node(node_id, label, fillcolor='#FFD700', color='#FF8C00')
        else:
            dot.node(node_id, label, fillcolor='#AED6F1', color='#2874A6')

        if node.left:
            dot.edge(node_id, str(node.left.course.id))
            self._add_nodes_to_graph(dot, node.left, highlight_ids)

        if node.right:
            dot.edge(node_id, str(node.right.course.id))
            self._add_nodes_to_graph(dot, node.right, highlight_ids)