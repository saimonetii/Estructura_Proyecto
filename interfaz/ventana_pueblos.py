"""Ventana gráfica del Proyecto 6: Ruta Mágica (grafo ponderado + Dijkstra).

Usa `construir_grafo_puebla()` y el método `dijkstra()` del código original
sin modificarlos. Esta ventana solo dibuja el grafo y pinta la ruta encontrada.
"""

import tkinter as tk
from tkinter import ttk

from proyectos.p6_pueblos_magicos import construir_grafo_puebla
from interfaz import estilos as e

# Posición de cada pueblo en el dibujo, como fracción del ancho y alto del
# lienzo (0 = izquierda/arriba, 1 = derecha/abajo). Es un acomodo aproximado
# parecido al mapa real de la Sierra Norte; el algoritmo NO usa estas posiciones.
POSICIONES = {
    "Pahuatlan": (0.10, 0.08),
    "Xicotepec de Juarez": (0.45, 0.08),
    "Zacatlan de las Manzanas": (0.28, 0.48),
    "Cuetzalan del Progreso": (0.82, 0.40),
    "Tetela de Ocampo": (0.52, 0.66),
    "Chignahuapan": (0.10, 0.90),
    "Tlatlauquitepec": (0.92, 0.90),
}
RADIO = 26
# Pueblos cuyo nombre se escribe a la izquierda del círculo para no tapar aristas
ETIQUETA_IZQUIERDA = {"Zacatlan de las Manzanas"}


def km_texto(km: float) -> str:
    """Igual que en el código original: 22.0 se muestra como 22."""
    return str(int(km)) if float(km).is_integer() else str(km)


class VentanaPueblos:
    def __init__(self, padre: tk.Misc):
        self.grafo = construir_grafo_puebla()    # <- objeto del código original
        self.ruta = []                           # lista de nombres de la ruta encontrada

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Proyecto 6 - Ruta Mágica (Grafos y Dijkstra)")
        self.ventana.geometry("1100x700")
        self.ventana.configure(bg=e.FONDO)

        e.encabezado(self.ventana, 6, f"Ruta Mágica - {self.grafo.estado}",
                     "Grafo ponderado no dirigido + algoritmo de Dijkstra")
        self.estado = e.barra_estado(self.ventana)

        cuerpo = tk.Frame(self.ventana, bg=e.FONDO, padx=16, pady=12)
        cuerpo.pack(fill="both", expand=True)

        # ------------------------------------------------ controles y resultado
        izq = e.panel(cuerpo, "Consultar ruta más corta")
        izq.pack(side="left", fill="y", padx=(0, 10))

        nombres = [p.nombre for p in sorted(self.grafo.pueblos.values(), key=lambda p: p.indice)]
        tk.Label(izq, text="Origen:", bg=e.TARJETA, font=e.F_NORMAL).pack(anchor="w")
        self.combo_origen = ttk.Combobox(izq, values=nombres, state="readonly", width=28)
        self.combo_origen.current(0)
        self.combo_origen.pack(anchor="w", pady=(0, 8))
        tk.Label(izq, text="Destino:", bg=e.TARJETA, font=e.F_NORMAL).pack(anchor="w")
        self.combo_destino = ttk.Combobox(izq, values=nombres, state="readonly", width=28)
        self.combo_destino.current(3)
        self.combo_destino.pack(anchor="w", pady=(0, 10))

        e.boton(izq, "Calcular ruta (Dijkstra)", self.calcular,
                color=e.COLOR_PROYECTO[6]).pack(fill="x")
        e.boton(izq, "Limpiar", self.limpiar, color=e.TEXTO_SUAVE).pack(fill="x", pady=(4, 0))

        tk.Label(izq, text="Resultado", font=e.F_SUBTITULO, bg=e.TARJETA,
                 fg=e.TEXTO).pack(anchor="w", pady=(14, 4))
        self.resultado = tk.Text(izq, width=34, height=14, font=e.F_MONO, relief="flat",
                                 bg="#FAFBFC", wrap="word", state="disabled")
        self.resultado.pack(fill="both", expand=True)

        # ------------------------------------------------ dibujo del grafo
        der = e.panel(cuerpo, "Mapa del grafo (distancias en km)")
        der.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(der, bg=e.TARJETA, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _evento: self.dibujar())

    # ------------------------------------------------------------- acciones
    def _escribir(self, texto: str):
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", texto)
        self.resultado.config(state="disabled")

    def calcular(self):
        origen, destino = self.combo_origen.get(), self.combo_destino.get()
        distancia_total, camino, tramos = self.grafo.dijkstra(origen, destino)

        if distancia_total is None:
            self.ruta = []
            self._escribir("[X] No existe ruta conectada entre esos pueblos.")
            e.mensaje(self.estado, "No existe ruta entre esos pueblos.", "error")
        else:
            lineas = ["[OK] RUTA ENCONTRADA",
                      f"Distancia total: {km_texto(distancia_total)} km", "", "Tramos:"]
            for u, v, km in tramos:
                lineas.append(f"{u}\n   --({km_texto(km)} km)--> {v}")
            lineas += ["", "Ruta completa:", " -> ".join(camino)]
            self.ruta = camino
            self._escribir("\n".join(lineas))
            e.mensaje(self.estado, f"Ruta más corta de {origen} a {destino}: "
                                   f"{km_texto(distancia_total)} km.", "ok")
        self.dibujar()

    def limpiar(self):
        self.ruta = []
        self._escribir("")
        e.mensaje(self.estado, "Listo.")
        self.dibujar()

    # --------------------------------------------------------------- dibujo
    def _posiciones(self, ancho, alto):
        margen_x, margen_y = 90, 50
        return {nombre: (margen_x + fx * (ancho - 2 * margen_x),
                         margen_y + fy * (alto - 2 * margen_y))
                for nombre, (fx, fy) in POSICIONES.items()}

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        ancho, alto = max(c.winfo_width(), 500), max(c.winfo_height(), 400)
        pos = self._posiciones(ancho, alto)
        tramos_ruta = {frozenset(par) for par in zip(self.ruta, self.ruta[1:])}

        # Aristas (cada carretera aparece dos veces en la lista de adyacencia,
        # una por sentido; con 'dibujadas' se dibuja solo una vez)
        dibujadas = set()
        for origen, aristas in self.grafo.adyacencia.items():
            for arista in aristas:
                par = frozenset((origen, arista.destino))
                if par in dibujadas:
                    continue
                dibujadas.add(par)
                (x1, y1), (x2, y2) = pos[origen], pos[arista.destino]
                en_ruta = par in tramos_ruta
                c.create_line(x1, y1, x2, y2, width=5 if en_ruta else 2,
                              fill=e.COLOR_PROYECTO[6] if en_ruta else "#B0BEC5")
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                c.create_rectangle(mx - 22, my - 10, mx + 22, my + 10, fill=e.TARJETA,
                                   outline=e.COLOR_PROYECTO[6] if en_ruta else e.BORDE)
                c.create_text(mx, my, text=f"{km_texto(arista.distancia_km)} km",
                              font=e.F_PEQUENA, fill=e.TEXTO)

        # Vértices
        for nombre, pueblo in self.grafo.pueblos.items():
            x, y = pos[nombre]
            en_ruta = nombre in self.ruta
            es_extremo = bool(self.ruta) and nombre in (self.ruta[0], self.ruta[-1])
            relleno = e.RESALTE if es_extremo else ("#FFE0B2" if en_ruta else "#ECEFF1")
            c.create_oval(x - RADIO, y - RADIO, x + RADIO, y + RADIO, fill=relleno,
                          outline=e.COLOR_PROYECTO[6] if en_ruta else "#78909C", width=2)
            c.create_text(x, y, text=pueblo.clave, font=e.F_NEGRITA, fill=e.TEXTO)
            if nombre in ETIQUETA_IZQUIERDA:
                c.create_text(x - RADIO - 6, y, text=nombre, anchor="e",
                              font=e.F_PEQUENA, fill=e.TEXTO)
            else:
                c.create_text(x, y + RADIO + 12, text=nombre, font=e.F_PEQUENA, fill=e.TEXTO)
