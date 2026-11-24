"""Colores, fuentes y pequeños ayudantes de Tkinter compartidos por todas las ventanas.

Tenerlos en un solo lugar hace que las 6 ventanas se vean iguales y que,
si se quiere cambiar un color, solo se cambie aquí.
"""

import tkinter as tk
from tkinter import ttk

# ----------------------------------------------------------------- COLORES
FONDO = "#F4F6FA"          # fondo general de las ventanas
TARJETA = "#FFFFFF"        # fondo de los paneles
BORDE = "#D9DEE7"
TEXTO = "#1E2733"
TEXTO_SUAVE = "#5B6675"
PRIMARIO = "#1F4E79"       # azul de los botones principales
PRIMARIO_HOVER = "#163A5A"
EXITO = "#2E7D32"
PELIGRO = "#C62828"
RESALTE = "#F9A825"        # amarillo para resaltar (ruta, nodo encontrado, etc.)

# Un color por proyecto (se usa en el menú y en el encabezado de cada ventana)
COLOR_PROYECTO = {
    1: "#1F77B4",  # Navegador - Pila
    2: "#8C564B",  # Resistencias - Arreglos
    3: "#2CA02C",  # Cola de impresión - Cola
    4: "#D62728",  # Carrito - Listas
    5: "#9467BD",  # Árbol binario
    6: "#FF7F0E",  # Pueblos Mágicos - Grafo
}

# ----------------------------------------------------------------- FUENTES
FUENTE = "Segoe UI"
F_TITULO = (FUENTE, 18, "bold")
F_SUBTITULO = (FUENTE, 12, "bold")
F_NORMAL = (FUENTE, 10)
F_NEGRITA = (FUENTE, 10, "bold")
F_PEQUENA = (FUENTE, 9)
F_MONO = ("Consolas", 10)


def configurar_ttk(raiz: tk.Misc) -> None:
    """Da a los Treeview y Combobox de ttk un estilo parecido al resto."""
    estilo = ttk.Style(raiz)
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass
    estilo.configure("Treeview", font=F_NORMAL, rowheight=24, background=TARJETA,
                     fieldbackground=TARJETA, foreground=TEXTO)
    estilo.configure("Treeview.Heading", font=F_NEGRITA, background=BORDE, foreground=TEXTO)
    estilo.map("Treeview", background=[("selected", PRIMARIO)],
               foreground=[("selected", "white")])
    estilo.configure("TCombobox", padding=4)


def encabezado(ventana: tk.Misc, numero: int, titulo: str, estructura: str) -> tk.Frame:
    """Barra de color con el número, nombre del proyecto y la estructura usada."""
    barra = tk.Frame(ventana, bg=COLOR_PROYECTO[numero], padx=16, pady=10)
    barra.pack(fill="x")
    tk.Label(barra, text=f"Proyecto {numero}: {titulo}", font=F_TITULO,
             bg=COLOR_PROYECTO[numero], fg="white").pack(anchor="w")
    tk.Label(barra, text=f"Estructura de datos: {estructura}", font=F_NORMAL,
             bg=COLOR_PROYECTO[numero], fg="white").pack(anchor="w")
    return barra


def boton(padre: tk.Misc, texto: str, comando, color: str = PRIMARIO, **kwargs) -> tk.Button:
    """Botón plano con color de fondo y texto blanco."""
    b = tk.Button(padre, text=texto, command=comando, bg=color, fg="white",
                  activebackground=PRIMARIO_HOVER, activeforeground="white",
                  font=F_NEGRITA, relief="flat", bd=0, padx=12, pady=6,
                  cursor="hand2", disabledforeground="#E0E0E0", **kwargs)
    return b


def panel(padre: tk.Misc, titulo: str = "") -> tk.Frame:
    """Recuadro blanco con borde y un título opcional."""
    marco = tk.Frame(padre, bg=TARJETA, highlightbackground=BORDE,
                     highlightthickness=1, padx=12, pady=10)
    if titulo:
        tk.Label(marco, text=titulo, font=F_SUBTITULO, bg=TARJETA,
                 fg=TEXTO).pack(anchor="w", pady=(0, 6))
    return marco


def barra_estado(ventana: tk.Misc) -> tk.Label:
    """Etiqueta inferior donde cada ventana escribe lo que acaba de pasar."""
    etiqueta = tk.Label(ventana, text="Listo.", anchor="w", font=F_NORMAL,
                        bg=BORDE, fg=TEXTO, padx=12, pady=6)
    etiqueta.pack(fill="x", side="bottom")
    return etiqueta


def mensaje(etiqueta: tk.Label, texto: str, tipo: str = "info") -> None:
    """Escribe un mensaje en la barra de estado con color según el tipo."""
    colores = {"info": TEXTO, "ok": EXITO, "error": PELIGRO}
    etiqueta.config(text=texto, fg=colores.get(tipo, TEXTO))
