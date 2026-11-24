"""Ventana gráfica del Proyecto 5: Directorio de alumnos con Árbol Binario de Búsqueda.

Usa la clase `ArbolBinarioBusqueda` de proyectos/p5_arbol_alumnos.py
y dibuja el árbol en un Canvas.
"""

import tkinter as tk

from proyectos.p5_arbol_alumnos import ArbolBinarioBusqueda, cargar_alumnos_ejemplo
from interfaz import estilos as e

RADIO = 22
SEPARACION_Y = 70
COLOR_NODO = "#E8DDF5"
COLOR_RECORRIDO = "#80DEEA"


class VentanaArbol:
    def __init__(self, padre: tk.Misc):
        self.arbol = ArbolBinarioBusqueda()
        cargar_alumnos_ejemplo(self.arbol)
        self.resaltados = {}          # matrícula -> color con el que se pinta
        self.animacion = None         # id del after() de la animación en curso
        self.orden_visita = {}        # matrícula -> número de visita en un recorrido

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Proyecto 5 - Directorio de alumnos (Árbol binario de búsqueda)")
        self.ventana.geometry("1060x720")
        self.ventana.configure(bg=e.FONDO)

        e.encabezado(self.ventana, 5, "Directorio de alumnos",
                     "Árbol Binario de Búsqueda (menores a la izquierda, mayores a la derecha)")
        self.estado = e.barra_estado(self.ventana)

        cuerpo = tk.Frame(self.ventana, bg=e.FONDO, padx=16, pady=12)
        cuerpo.pack(fill="both", expand=True)

        # ------------------------------------------------ panel de controles
        izq = e.panel(cuerpo, "Alumno")
        izq.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(izq, text="Matrícula (número):", bg=e.TARJETA, font=e.F_NORMAL).pack(anchor="w")
        self.entrada_matricula = tk.Entry(izq, font=e.F_NORMAL, relief="solid", bd=1, width=22)
        self.entrada_matricula.pack(anchor="w", ipady=3, pady=(0, 6))
        tk.Label(izq, text="Nombre (solo para insertar):", bg=e.TARJETA,
                 font=e.F_NORMAL).pack(anchor="w")
        self.entrada_nombre = tk.Entry(izq, font=e.F_NORMAL, relief="solid", bd=1, width=22)
        self.entrada_nombre.pack(anchor="w", ipady=3, pady=(0, 10))

        for texto, comando, color in (("Insertar", self.insertar, e.EXITO),
                                      ("Buscar", self.buscar, e.PRIMARIO),
                                      ("Eliminar", self.eliminar, e.PELIGRO)):
            e.boton(izq, texto, comando, color=color).pack(fill="x", pady=2)

        tk.Label(izq, text="Recorridos", font=e.F_SUBTITULO, bg=e.TARJETA,
                 fg=e.TEXTO).pack(anchor="w", pady=(14, 4))
        for nombre in ("Inorden", "Preorden", "Postorden"):
            e.boton(izq, nombre, lambda n=nombre: self.recorrer(n),
                    color=e.COLOR_PROYECTO[5]).pack(fill="x", pady=2)

        tk.Label(izq, text="Estadísticas", font=e.F_SUBTITULO, bg=e.TARJETA,
                 fg=e.TEXTO).pack(anchor="w", pady=(14, 4))
        self.lbl_stats = tk.Label(izq, bg=e.TARJETA, font=e.F_NORMAL, justify="left", fg=e.TEXTO)
        self.lbl_stats.pack(anchor="w")

        # ------------------------------------------------ dibujo del árbol
        der = e.panel(cuerpo, "Árbol")
        der.pack(side="left", fill="both", expand=True)
        self.lbl_resultado = tk.Label(der, text="", bg=e.TARJETA, font=e.F_MONO,
                                      fg=e.PRIMARIO, anchor="w", justify="left", wraplength=640)
        self.lbl_resultado.pack(fill="x")
        self.canvas = tk.Canvas(der, bg=e.TARJETA, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _evento: self.dibujar())

        self.entrada_matricula.bind("<Return>", lambda _evento: self.buscar())
        self.entrada_nombre.bind("<Return>", lambda _evento: self.insertar())
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.actualizar()

    # ------------------------------------------------------------ utilidades
    def _leer_matricula(self):
        texto = self.entrada_matricula.get().strip()
        if not texto.isdigit() or int(texto) <= 0:
            e.mensaje(self.estado, "La matrícula debe ser un número entero mayor que 0.", "error")
            return None
        return int(texto)

    def _detener_animacion(self):
        self.orden_visita = {}
        if self.animacion is not None:
            self.ventana.after_cancel(self.animacion)
            self.animacion = None

    def cerrar(self):
        self._detener_animacion()
        self.ventana.destroy()

    def actualizar(self):
        minimo, maximo = self.arbol.minimo(), self.arbol.maximo()
        self.lbl_stats.config(text=(
            f"Cantidad de alumnos: {self.arbol.cantidad}\n"
            f"Altura: {self.arbol.altura()}\n"
            f"Menor: {minimo if minimo else '-'}\n"
            f"Mayor: {maximo if maximo else '-'}"))
        self.dibujar()

    # ------------------------------------------------------------- acciones
    def insertar(self):
        self._detener_animacion()
        matricula = self._leer_matricula()
        if matricula is None:
            return
        nombre = self.entrada_nombre.get().strip()
        if not nombre:
            e.mensaje(self.estado, "Escribe el nombre del alumno para insertarlo.", "error")
            return
        if self.arbol.insertar(matricula, nombre):
            self.resaltados = {matricula: e.RESALTE}
            e.mensaje(self.estado, f"Alumno {nombre} insertado con matrícula {matricula}.", "ok")
            self.entrada_matricula.delete(0, "end")
            self.entrada_nombre.delete(0, "end")
            self.entrada_matricula.focus_set()
        else:
            self.resaltados = {matricula: e.PELIGRO}
            e.mensaje(self.estado, f"Ya existe un alumno con la matrícula {matricula}.", "error")
        self.lbl_resultado.config(text="")
        self.actualizar()

    def buscar(self):
        self._detener_animacion()
        matricula = self._leer_matricula()
        if matricula is None:
            return
        nodo, camino = self.arbol.buscar(matricula)
        self.resaltados = {m: COLOR_RECORRIDO for m in camino}
        recorrido = " -> ".join(str(m) for m in camino) or "(árbol vacío)"
        if nodo is None:
            self.lbl_resultado.config(text=f"Camino recorrido: {recorrido}")
            e.mensaje(self.estado, f"No se encontró la matrícula {matricula}.", "error")
        else:
            self.resaltados[matricula] = e.RESALTE
            self.lbl_resultado.config(text=f"Camino recorrido: {recorrido}")
            e.mensaje(self.estado, f"Encontrado: {nodo} (en {len(camino)} comparaciones).", "ok")
        self.dibujar()

    def eliminar(self):
        self._detener_animacion()
        matricula = self._leer_matricula()
        if matricula is None:
            return
        if self.arbol.eliminar(matricula):
            e.mensaje(self.estado, f"La matrícula {matricula} se eliminó del árbol.", "ok")
            self.entrada_matricula.delete(0, "end")
        else:
            e.mensaje(self.estado, f"No existe la matrícula {matricula}.", "error")
        self.resaltados = {}
        self.lbl_resultado.config(text="")
        self.actualizar()

    def recorrer(self, tipo):
        """Muestra el recorrido y lo anima nodo por nodo."""
        self._detener_animacion()
        metodo = {"Inorden": self.arbol.inorden, "Preorden": self.arbol.preorden,
                  "Postorden": self.arbol.postorden}[tipo]
        nodos = metodo()
        if not nodos:
            e.mensaje(self.estado, "El árbol está vacío.", "error")
            return
        self.resaltados = {}
        e.mensaje(self.estado, f"Recorrido {tipo} en curso...")

        def paso(i):
            if i == len(nodos):
                self.animacion = None
                e.mensaje(self.estado, f"Recorrido {tipo} terminado.", "ok")
                return
            self.resaltados[nodos[i].matricula] = COLOR_RECORRIDO
            self.orden_visita[nodos[i].matricula] = i + 1
            self.lbl_resultado.config(
                text=f"{tipo}: " + " -> ".join(str(n.matricula) for n in nodos[:i + 1]))
            self.dibujar()
            self.animacion = self.ventana.after(450, paso, i + 1)

        paso(0)

    # --------------------------------------------------------------- dibujo
    def dibujar(self):
        c = self.canvas
        c.delete("all")
        ancho = max(c.winfo_width(), 400)
        if self.arbol.esta_vacio():
            c.create_text(ancho / 2, 120, text="[ ÁRBOL VACÍO ]", font=e.F_SUBTITULO,
                          fill=e.TEXTO_SUAVE)
            return

        # x según la posición en inorden (así nunca se enciman), y según el nivel
        orden = self.arbol.inorden()
        paso_x = ancho / (len(orden) + 1)
        posiciones = {}

        def ubicar(nodo, nivel):
            if nodo is None:
                return
            ubicar(nodo.izquierdo, nivel + 1)
            posiciones[nodo.matricula] = (paso_x * (len(posiciones) + 1),
                                          40 + nivel * SEPARACION_Y)
            ubicar(nodo.derecho, nivel + 1)

        ubicar(self.arbol.raiz, 0)

        def lineas(nodo):
            if nodo is None:
                return
            x, y = posiciones[nodo.matricula]
            for hijo in (nodo.izquierdo, nodo.derecho):
                if hijo is not None:
                    hx, hy = posiciones[hijo.matricula]
                    c.create_line(x, y, hx, hy, fill=e.TEXTO_SUAVE, width=2)
                    lineas(hijo)

        lineas(self.arbol.raiz)

        visitas = self.orden_visita
        for nodo in orden:
            x, y = posiciones[nodo.matricula]
            color = self.resaltados.get(nodo.matricula, COLOR_NODO)
            c.create_oval(x - RADIO, y - RADIO, x + RADIO, y + RADIO, fill=color,
                          outline=e.COLOR_PROYECTO[5], width=2)
            c.create_text(x, y, text=str(nodo.matricula), font=e.F_NEGRITA, fill=e.TEXTO)
            c.create_text(x, y + RADIO + 10, text=nodo.nombre, font=e.F_PEQUENA,
                          fill=e.TEXTO_SUAVE)
            if nodo.matricula in visitas:
                c.create_text(x + RADIO, y - RADIO, text=str(visitas[nodo.matricula]),
                              font=e.F_NEGRITA, fill=e.PELIGRO)
        if self.arbol.raiz is not None:
            x, y = posiciones[self.arbol.raiz.matricula]
            c.create_text(x, y - RADIO - 10, text="RAÍZ", font=e.F_PEQUENA, fill=e.PELIGRO)
