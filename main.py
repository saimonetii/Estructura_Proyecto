"""PROYECTO INTEGRADOR DE ESTRUCTURAS DE DATOS

Este es el ÚNICO archivo que hay que ejecutar. Abre un menú gráfico con los
6 proyectos de la materia; cada botón abre la ventana de ese proyecto:

    1. Navegador web ............ Pilas (LIFO)
    2. Resistencias eléctricas .. Arreglos / tuplas y listas (ya traía Tkinter)
    3. Cola de impresión ........ Colas (FIFO) de capacidad limitada
    4. Carrito de compras ....... Listas de objetos y búsqueda
    5. Directorio de alumnos .... Árbol binario de búsqueda
    6. Ruta Mágica .............. Grafos ponderados + Dijkstra

Uso:
    python main.py            -> menú gráfico (Tkinter)
    python main.py --consola  -> menú en la terminal que corre los programas
                                 originales tal cual (con input/print)

El código de cada proyecto está en la carpeta `proyectos/` SIN CAMBIOS, y las
ventanas gráficas están en la carpeta `interfaz/` (solo usan esas clases).
"""

import subprocess
import sys
import tkinter as tk
from pathlib import Path

from interfaz import estilos as e

CARPETA_PROYECTOS = Path(__file__).resolve().parent / "proyectos"

# (número, título, estructura, descripción corta)
PROYECTOS = [
    (1, "Navegador web", "Pila (LIFO)",
     "Historial con botones Back y Forward usando dos pilas."),
    (2, "Resistencias eléctricas", "Arreglos y listas",
     "Bandas de color de una resistencia y suma en serie y en paralelo."),
    (3, "Cola de impresión", "Cola (FIFO)",
     "5 computadoras mandan trabajos a una impresora con capacidad de 6."),
    (4, "Carrito de compras", "Listas de objetos",
     "Catálogo, búsqueda por ID o nombre, carrito y total a pagar."),
    (5, "Directorio de alumnos", "Árbol binario de búsqueda",
     "Insertar, buscar y eliminar alumnos por matrícula y ver recorridos."),
    (6, "Ruta Mágica", "Grafo + Dijkstra",
     "Camino más corto entre Pueblos Mágicos de Puebla."),
]


# =============================================================== MODO GRÁFICO
class MenuPrincipal:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Proyecto Integrador - Estructuras de Datos")
        self.raiz.geometry("980x660")
        self.raiz.minsize(900, 640)
        self.raiz.configure(bg=e.FONDO)
        e.configurar_ttk(self.raiz)

        self.ventanas = {}           # número de proyecto -> ventana abierta
        self.proceso_resistencias = None

        # Encabezado
        arriba = tk.Frame(self.raiz, bg=e.PRIMARIO, padx=24, pady=16)
        arriba.pack(fill="x")
        tk.Label(arriba, text="Proyecto Integrador de Estructuras de Datos",
                 font=e.F_TITULO, bg=e.PRIMARIO, fg="white").pack(anchor="w")
        tk.Label(arriba, text="Elige un proyecto para abrirlo. Puedes tener varios abiertos a la vez.",
                 font=e.F_NORMAL, bg=e.PRIMARIO, fg="white").pack(anchor="w")

        # Tarjetas 3 x 2
        rejilla = tk.Frame(self.raiz, bg=e.FONDO, padx=18, pady=18)
        rejilla.pack(fill="both", expand=True)
        for i, datos in enumerate(PROYECTOS):
            fila, columna = divmod(i, 3)
            rejilla.columnconfigure(columna, weight=1, uniform="col")
            rejilla.rowconfigure(fila, weight=1, uniform="fila")
            self._tarjeta(rejilla, *datos).grid(row=fila, column=columna, sticky="nsew",
                                                padx=8, pady=8)

        # Pie
        abajo = tk.Frame(self.raiz, bg=e.FONDO, padx=26)
        abajo.pack(fill="x", pady=(0, 14))
        tk.Label(abajo, text="Tip: con  python main.py --consola  se corren las versiones "
                             "originales en la terminal.",
                 font=e.F_PEQUENA, bg=e.FONDO, fg=e.TEXTO_SUAVE).pack(side="left")
        e.boton(abajo, "Salir", self.raiz.destroy, color=e.PELIGRO).pack(side="right")

    def _tarjeta(self, padre, numero, titulo, estructura, descripcion):
        color = e.COLOR_PROYECTO[numero]
        tarjeta = tk.Frame(padre, bg=e.TARJETA, highlightbackground=e.BORDE, highlightthickness=1)
        tk.Frame(tarjeta, bg=color, height=6).pack(fill="x")
        contenido = tk.Frame(tarjeta, bg=e.TARJETA, padx=14, pady=10)
        contenido.pack(fill="both", expand=True)

        tk.Label(contenido, text=str(numero), font=(e.FUENTE, 26, "bold"), bg=e.TARJETA,
                 fg=color).pack(anchor="w")
        tk.Label(contenido, text=titulo, font=e.F_SUBTITULO, bg=e.TARJETA,
                 fg=e.TEXTO).pack(anchor="w")
        tk.Label(contenido, text=estructura, font=e.F_NEGRITA, bg=e.TARJETA,
                 fg=color).pack(anchor="w")
        tk.Label(contenido, text=descripcion, font=e.F_PEQUENA, bg=e.TARJETA, fg=e.TEXTO_SUAVE,
                 wraplength=260, justify="left").pack(anchor="w", pady=(4, 8))
        e.boton(contenido, "Abrir", lambda: self.abrir(numero),
                color=color).pack(anchor="w", side="bottom")
        return tarjeta

    def abrir(self, numero):
        # El proyecto 2 ya era una ventana Tkinter completa: se ejecuta su
        # archivo original tal cual, en su propio proceso.
        if numero == 2:
            if self.proceso_resistencias is None or self.proceso_resistencias.poll() is not None:
                self.proceso_resistencias = subprocess.Popen(
                    [sys.executable, str(CARPETA_PROYECTOS / "p2_resistencias.py")])
            return

        # Si la ventana ya está abierta, solo se trae al frente
        abierta = self.ventanas.get(numero)
        if abierta is not None and abierta.ventana.winfo_exists():
            abierta.ventana.deiconify()
            abierta.ventana.lift()
            abierta.ventana.focus_force()
            return

        # Se importan aquí para que el menú abra rápido
        if numero == 1:
            from interfaz.ventana_navegador import VentanaNavegador as Ventana
        elif numero == 3:
            from interfaz.ventana_cola import VentanaCola as Ventana
        elif numero == 4:
            from interfaz.ventana_carrito import VentanaCarrito as Ventana
        elif numero == 5:
            from interfaz.ventana_arbol import VentanaArbol as Ventana
        else:
            from interfaz.ventana_pueblos import VentanaPueblos as Ventana
        self.ventanas[numero] = Ventana(self.raiz)

    def ejecutar(self):
        self.raiz.mainloop()


# ================================================================ MODO CONSOLA
def menu_consola():
    """Corre los programas ORIGINALES en la terminal, tal como fueron entregados."""
    from proyectos import p1_navegador_web, p3_cola_impresion, p5_arbol_alumnos
    from proyectos.p4_carrito_compras import SistemaCarrito
    from proyectos.p6_pueblos_magicos import RutaMagicaApp, construir_grafo_puebla

    while True:
        print("\n=== PROYECTO INTEGRADOR DE ESTRUCTURAS DE DATOS ===")
        for numero, titulo, estructura, _ in PROYECTOS:
            print(f"{numero}. {titulo} ({estructura})")
        print("0. Salir")
        opcion = input("Selecciona un proyecto: ").strip()

        if opcion == "1":
            p1_navegador_web.menu()
        elif opcion == "2":
            print("Abriendo la ventana de Resistencias... ciérrala para volver al menú.")
            subprocess.run([sys.executable, str(CARPETA_PROYECTOS / "p2_resistencias.py")])
        elif opcion == "3":
            p3_cola_impresion.menu()
        elif opcion == "4":
            SistemaCarrito().ejecutar()
        elif opcion == "5":
            p5_arbol_alumnos.menu()
        elif opcion == "6":
            RutaMagicaApp(construir_grafo_puebla()).ejecutar()
        elif opcion == "0":
            print("Cerrando la aplicación. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    if "--consola" in sys.argv:
        menu_consola()
    else:
        MenuPrincipal().ejecutar()
