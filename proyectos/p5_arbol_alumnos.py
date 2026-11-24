from typing import List, Optional, Tuple


class Nodo:
    """Representa un nodo del árbol: un alumno con su matrícula (llave) y nombre."""

    def __init__(self, matricula: int, nombre: str):
        self.matricula = matricula
        self.nombre = nombre
        self.izquierdo: Optional["Nodo"] = None
        self.derecho: Optional["Nodo"] = None

    def __str__(self) -> str:
        return f"{self.matricula} - {self.nombre}"


class ArbolBinarioBusqueda:
    """Árbol Binario de Búsqueda (ABB) ordenado por matrícula.

    Regla del ABB: para cada nodo, todas las matrículas del subárbol
    izquierdo son menores y todas las del subárbol derecho son mayores.
    """

    def __init__(self):
        self.raiz: Optional[Nodo] = None
        self.cantidad = 0

    def esta_vacio(self) -> bool:
        return self.raiz is None

    # ---------------------------------------------------------------- INSERTAR
    def insertar(self, matricula: int, nombre: str) -> bool:
        """Inserta un alumno. Regresa False si la matrícula ya existe."""
        if self.raiz is None:
            self.raiz = Nodo(matricula, nombre)
            self.cantidad += 1
            return True

        actual = self.raiz
        while True:
            if matricula == actual.matricula:
                return False
            if matricula < actual.matricula:
                if actual.izquierdo is None:
                    actual.izquierdo = Nodo(matricula, nombre)
                    self.cantidad += 1
                    return True
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = Nodo(matricula, nombre)
                    self.cantidad += 1
                    return True
                actual = actual.derecho

    # ------------------------------------------------------------------ BUSCAR
    def buscar(self, matricula: int) -> Tuple[Optional[Nodo], List[int]]:
        """Busca una matrícula. Regresa (nodo encontrado o None, camino recorrido)."""
        camino: List[int] = []
        actual = self.raiz
        while actual is not None:
            camino.append(actual.matricula)
            if matricula == actual.matricula:
                return actual, camino
            if matricula < actual.matricula:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None, camino

    # ---------------------------------------------------------------- ELIMINAR
    def eliminar(self, matricula: int) -> bool:
        """Elimina un alumno. Regresa False si la matrícula no existe."""
        nodo, _ = self.buscar(matricula)
        if nodo is None:
            return False
        self.raiz = self._eliminar(self.raiz, matricula)
        self.cantidad -= 1
        return True

    def _eliminar(self, nodo: Optional[Nodo], matricula: int) -> Optional[Nodo]:
        if nodo is None:
            return None
        if matricula < nodo.matricula:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, matricula)
        elif matricula > nodo.matricula:
            nodo.derecho = self._eliminar(nodo.derecho, matricula)
        else:
            # Caso 1 y 2: el nodo tiene 0 o 1 hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: el nodo tiene 2 hijos -> se reemplaza por su sucesor
            # (el menor del subárbol derecho)
            sucesor = self._minimo_desde(nodo.derecho)
            nodo.matricula = sucesor.matricula
            nodo.nombre = sucesor.nombre
            nodo.derecho = self._eliminar(nodo.derecho, sucesor.matricula)
        return nodo

    # -------------------------------------------------------------- RECORRIDOS
    def inorden(self) -> List[Nodo]:
        """Izquierdo -> Raíz -> Derecho (sale ordenado por matrícula)."""
        resultado: List[Nodo] = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo: Optional[Nodo], resultado: List[Nodo]) -> None:
        if nodo is not None:
            self._inorden(nodo.izquierdo, resultado)
            resultado.append(nodo)
            self._inorden(nodo.derecho, resultado)

    def preorden(self) -> List[Nodo]:
        """Raíz -> Izquierdo -> Derecho."""
        resultado: List[Nodo] = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo: Optional[Nodo], resultado: List[Nodo]) -> None:
        if nodo is not None:
            resultado.append(nodo)
            self._preorden(nodo.izquierdo, resultado)
            self._preorden(nodo.derecho, resultado)

    def postorden(self) -> List[Nodo]:
        """Izquierdo -> Derecho -> Raíz."""
        resultado: List[Nodo] = []
        self._postorden(self.raiz, resultado)
        return resultado

    def _postorden(self, nodo: Optional[Nodo], resultado: List[Nodo]) -> None:
        if nodo is not None:
            self._postorden(nodo.izquierdo, resultado)
            self._postorden(nodo.derecho, resultado)
            resultado.append(nodo)

    # ----------------------------------------------------------- ESTADÍSTICAS
    def altura(self) -> int:
        """Número de niveles del árbol (0 si está vacío)."""
        return self._altura(self.raiz)

    def _altura(self, nodo: Optional[Nodo]) -> int:
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def _minimo_desde(self, nodo: Nodo) -> Nodo:
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def minimo(self) -> Optional[Nodo]:
        if self.raiz is None:
            return None
        return self._minimo_desde(self.raiz)

    def maximo(self) -> Optional[Nodo]:
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo


def cargar_alumnos_ejemplo(arbol: ArbolBinarioBusqueda) -> None:
    """Carga algunos alumnos de ejemplo para no empezar con el árbol vacío."""
    alumnos = [
        (50, "Ana"),
        (30, "Luis"),
        (70, "Sofia"),
        (20, "Carlos"),
        (40, "Maria"),
        (60, "Jorge"),
        (80, "Valeria"),
    ]
    for matricula, nombre in alumnos:
        arbol.insertar(matricula, nombre)


def mostrar_lista(titulo: str, nodos: List[Nodo]) -> None:
    print(f"\n{titulo}:")
    if not nodos:
        print("[ ARBOL VACIO ]")
    else:
        print(" -> ".join(str(n.matricula) for n in nodos))


def pedir_matricula(mensaje: str) -> Optional[int]:
    try:
        matricula = int(input(mensaje).strip())
    except ValueError:
        print("Matricula no valida. Debe ser un numero entero.")
        return None
    if matricula <= 0:
        print("La matricula debe ser mayor que 0.")
        return None
    return matricula


def menu():
    arbol = ArbolBinarioBusqueda()
    cargar_alumnos_ejemplo(arbol)

    while True:
        print("\n--- PROYECTO ARBOL BINARIO DE BUSQUEDA: DIRECTORIO DE ALUMNOS ---")
        print("1. Insertar alumno")
        print("2. Buscar alumno por matricula")
        print("3. Eliminar alumno")
        print("4. Mostrar recorridos (inorden, preorden, postorden)")
        print("5. Mostrar estadisticas (cantidad, altura, minimo, maximo)")
        print("6. Salir")

        opcion = input("Selecciona una opcion (1-6): ").strip()

        if opcion == "1":
            matricula = pedir_matricula("Matricula: ")
            if matricula is None:
                continue
            nombre = input("Nombre: ").strip()
            if not nombre:
                print("El nombre no puede quedar vacio.")
                continue
            if arbol.insertar(matricula, nombre):
                print(f"\nAlumno {nombre} insertado con matricula {matricula}.")
            else:
                print(f"\nYa existe un alumno con la matricula {matricula}.")

        elif opcion == "2":
            matricula = pedir_matricula("Matricula a buscar: ")
            if matricula is None:
                continue
            nodo, camino = arbol.buscar(matricula)
            print("Camino recorrido: " + " -> ".join(str(m) for m in camino))
            if nodo is None:
                print(f"No se encontro la matricula {matricula}.")
            else:
                print(f"Encontrado: {nodo} (en {len(camino)} comparaciones)")

        elif opcion == "3":
            matricula = pedir_matricula("Matricula a eliminar: ")
            if matricula is None:
                continue
            if arbol.eliminar(matricula):
                print(f"\nLa matricula {matricula} se elimino del arbol.")
            else:
                print(f"\nNo existe la matricula {matricula}.")

        elif opcion == "4":
            mostrar_lista("Inorden (ordenado)", arbol.inorden())
            mostrar_lista("Preorden", arbol.preorden())
            mostrar_lista("Postorden", arbol.postorden())

        elif opcion == "5":
            print(f"\nCantidad de alumnos: {arbol.cantidad}")
            print(f"Altura del arbol: {arbol.altura()}")
            minimo = arbol.minimo()
            maximo = arbol.maximo()
            print(f"Matricula menor: {minimo if minimo else '-'}")
            print(f"Matricula mayor: {maximo if maximo else '-'}")

        elif opcion == "6":
            print("Saliendo del directorio de alumnos...")
            break
        else:
            print("\nOpcion no valida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()
