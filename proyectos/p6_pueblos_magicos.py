import heapq
from typing import Dict, List, Optional, Tuple


class PuebloMagico:
    """Representa un Pueblo Mágico (vértice del grafo)."""

    def __init__(self, indice: int, nombre: str, clave: str):
        self.indice = indice
        self.nombre = nombre
        self.clave = clave

    def __str__(self) -> str:
        return f"{self.nombre} ({self.clave})"


class Arista:
    """Representa una carretera directa entre dos Pueblos Mágicos con distancia en km."""

    def __init__(self, destino: str, distancia_km: float):
        self.destino = destino
        self.distancia_km = distancia_km

    def __repr__(self) -> str:
        return f"Arista(destino={self.destino!r}, distancia_km={self.distancia_km})"


class GrafoPueblosMagicos:
    """Modela los Pueblos Mágicos de un estado como un grafo ponderado no dirigido."""

    def __init__(self, estado: str):
        self.estado = estado
        self.pueblos: Dict[str, PuebloMagico] = {}
        self.adyacencia: Dict[str, List[Arista]] = {}

    def agregar_pueblo(self, nombre: str, clave: str) -> PuebloMagico:
        if nombre not in self.pueblos:
            nuevo_indice = len(self.pueblos) + 1
            self.pueblos[nombre] = PuebloMagico(nuevo_indice, nombre, clave)
            self.adyacencia[nombre] = []
        return self.pueblos[nombre]

    def agregar_carretera(
        self, origen: str, destino: str, distancia_km: float, bidireccional: bool = True
    ) -> None:
        if origen not in self.adyacencia or destino not in self.adyacencia:
            raise ValueError("Ambos Pueblos Mágicos deben existir antes de agregar una carretera.")
        self.adyacencia[origen].append(Arista(destino, distancia_km))
        if bidireccional:
            self.adyacencia[destino].append(Arista(origen, distancia_km))

    def obtener_pueblo_por_indice(self, indice: int) -> Optional[PuebloMagico]:
        for pueblo in self.pueblos.values():
            if pueblo.indice == indice:
                return pueblo
        return None

    def dijkstra(
        self, origen: str, destino: str
    ) -> Tuple[Optional[float], List[str], List[Tuple[str, str, float]]]:
        if origen not in self.adyacencia or destino not in self.adyacencia:
            return None, [], []

        distancias: Dict[str, float] = {nodo: float("inf") for nodo in self.adyacencia}
        anteriores: Dict[str, Optional[str]] = {nodo: None for nodo in self.adyacencia}
        distancias[origen] = 0.0

        cola_prioridad: List[Tuple[float, str]] = [(0.0, origen)]

        while cola_prioridad:
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

            if distancia_actual > distancias[nodo_actual]:
                continue

            if nodo_actual == destino:
                break

            for arista in self.adyacencia[nodo_actual]:
                nueva_distancia = distancia_actual + arista.distancia_km
                if nueva_distancia < distancias[arista.destino]:
                    distancias[arista.destino] = nueva_distancia
                    anteriores[arista.destino] = nodo_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, arista.destino))

        if distancias[destino] == float("inf"):
            return None, [], []

        camino: List[str] = []
        actual: Optional[str] = destino
        while actual is not None:
            camino.append(actual)
            actual = anteriores[actual]
        camino.reverse()

        tramos: List[Tuple[str, str, float]] = []
        for i in range(len(camino) - 1):
            u = camino[i]
            v = camino[i + 1]
            peso_tramo = next(a.distancia_km for a in self.adyacencia[u] if a.destino == v)
            tramos.append((u, v, peso_tramo))

        return distancias[destino], camino, tramos


class RutaMagicaApp:
    """Maneja la interacción en consola para consultar rutas entre Pueblos Mágicos."""

    def __init__(self, grafo: GrafoPueblosMagicos):
        self.grafo = grafo

    def mostrar_menu_pueblos(self) -> None:
        print("\nPueblos Magicos disponibles:")
        for pueblo in sorted(self.grafo.pueblos.values(), key=lambda p: p.indice):
            print(f"{pueblo.indice}. {pueblo.nombre}")

    def ejecutar(self) -> None:
        print("RUTA MAGICA")
        print(self.grafo.estado.upper())
        print("Camino mas corto entre Pueblos Magicos")

        while True:
            self.mostrar_menu_pueblos()
            total = len(self.grafo.pueblos)

            try:
                idx_origen = int(input(f"\nSeleccione pueblo de ORIGEN (1-{total}): ").strip())
                pueblo_origen = self.grafo.obtener_pueblo_por_indice(idx_origen)
                if not pueblo_origen:
                    print("[!] Opcion de origen invalida.")
                    continue
                print(f"-> Origen: {pueblo_origen.nombre}")

                idx_destino = int(input(f"Seleccione pueblo de DESTINO (1-{total}): ").strip())
                pueblo_destino = self.grafo.obtener_pueblo_por_indice(idx_destino)
                if not pueblo_destino:
                    print("[!] Opcion de destino invalida.")
                    continue
                print(f"-> Destino: {pueblo_destino.nombre}")

            except ValueError:
                print("[!] Ingrese un numero valido.")
                continue

            print("Algoritmo utilizado: Dijkstra")
            print("Calculando ruta mas corta...")

            distancia_total, camino, tramos = self.grafo.dijkstra(
                pueblo_origen.nombre, pueblo_destino.nombre
            )

            if distancia_total is None:
                print("[X] No existe ruta conectada entre esos pueblos.")
            else:
                print("[OK] RUTA ENCONTRADA")
                for u, v, km in tramos:
                    km_fmt = int(km) if km.is_integer() else km
                    print(f"{u} --({km_fmt} km)--> {v}")
                print("Ruta completa:")
                print(" -> ".join(camino))
                dist_fmt = int(distancia_total) if distancia_total.is_integer() else distancia_total
                print(f"Distancia total: {dist_fmt} km")

            repetir = input("\nDesea consultar otra ruta? (S/N): ").strip().upper()
            if repetir != "S":
                print("Programa finalizado.")
                break


def construir_grafo_puebla() -> GrafoPueblosMagicos:
    """Crea el grafo con los Pueblos Mágicos de Puebla (Sierra Norte) y sus distancias."""
    grafo = GrafoPueblosMagicos("Puebla")

    pueblos = [
        ("Zacatlan de las Manzanas", "ZAC"),
        ("Chignahuapan", "CHI"),
        ("Tetela de Ocampo", "TET"),
        ("Cuetzalan del Progreso", "CUE"),
        ("Tlatlauquitepec", "TLA"),
        ("Xicotepec de Juarez", "XIC"),
        ("Pahuatlan", "PAH"),
    ]
    for nombre, clave in pueblos:
        grafo.agregar_pueblo(nombre, clave)

    carreteras = [
        ("Zacatlan de las Manzanas", "Chignahuapan", 22),
        ("Zacatlan de las Manzanas", "Tetela de Ocampo", 48),
        ("Chignahuapan", "Tetela de Ocampo", 42),
        ("Tetela de Ocampo", "Cuetzalan del Progreso", 68),
        ("Cuetzalan del Progreso", "Tlatlauquitepec", 38),
        ("Zacatlan de las Manzanas", "Xicotepec de Juarez", 55),
        ("Xicotepec de Juarez", "Pahuatlan", 32),
        ("Pahuatlan", "Zacatlan de las Manzanas", 60),
        ("Chignahuapan", "Tlatlauquitepec", 90),
        ("Xicotepec de Juarez", "Cuetzalan del Progreso", 115),
    ]
    for origen, destino, km in carreteras:
        grafo.agregar_carretera(origen, destino, km, bidireccional=True)

    return grafo


if __name__ == "__main__":
    grafo_puebla = construir_grafo_puebla()
    app = RutaMagicaApp(grafo_puebla)
    app.ejecutar()
