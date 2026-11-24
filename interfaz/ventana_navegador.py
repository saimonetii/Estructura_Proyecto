"""Ventana gráfica del Proyecto 1: Navegador web con pilas (LIFO).

Usa las clases originales `Pila` y `NavegadorWeb` sin modificarlas.
La ventana solo llama a sus métodos y dibuja el contenido de las dos pilas.
"""

import tkinter as tk

from proyectos.p1_navegador_web import NavegadorWeb
from interfaz import estilos as e

ALTO_CAJA = 34
MAX_CAJAS = 7


class VentanaNavegador:
    def __init__(self, padre: tk.Misc):
        self.navegador = NavegadorWeb()  # <- objeto del código original

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Proyecto 1 - Navegador web (Pilas)")
        self.ventana.geometry("820x680")
        self.ventana.configure(bg=e.FONDO)

        e.encabezado(self.ventana, 1, "Navegador web", "Pila (LIFO: último en entrar, primero en salir)")
        self.estado = e.barra_estado(self.ventana)

        cuerpo = tk.Frame(self.ventana, bg=e.FONDO, padx=16, pady=12)
        cuerpo.pack(fill="both", expand=True)

        # --- Barra tipo navegador: Back, Forward, URL, Visitar
        barra = e.panel(cuerpo)
        barra.pack(fill="x")
        self.btn_atras = e.boton(barra, "◀ Back", self.retroceder)
        self.btn_atras.pack(side="left")
        self.btn_adelante = e.boton(barra, "Forward ▶", self.avanzar)
        self.btn_adelante.pack(side="left", padx=(6, 12))
        self.entrada_url = tk.Entry(barra, font=e.F_NORMAL, relief="solid", bd=1)
        self.entrada_url.pack(side="left", fill="x", expand=True, ipady=5)
        self.entrada_url.bind("<Return>", lambda _evento: self.visitar())
        e.boton(barra, "Visitar", self.visitar, color=e.EXITO).pack(side="left", padx=(8, 0))

        # --- Página actual
        actual = e.panel(cuerpo, "Página actual")
        actual.pack(fill="x", pady=10)
        self.lbl_actual = tk.Label(actual, text="(ninguna todavía)", font=e.F_SUBTITULO,
                                   bg=e.TARJETA, fg=e.PRIMARIO)
        self.lbl_actual.pack(anchor="w")

        # --- Las dos pilas dibujadas
        pilas = tk.Frame(cuerpo, bg=e.FONDO)
        pilas.pack(fill="both", expand=True)
        self.canvas_atras = self._crear_pila(pilas, "Pila ATRÁS (historial anterior)")
        self.canvas_adelante = self._crear_pila(pilas, "Pila ADELANTE (para Forward)")

        self.actualizar()
        self.entrada_url.focus_set()

    # ------------------------------------------------------------ acciones
    def visitar(self):
        url = self.entrada_url.get().strip()
        if not url:
            e.mensaje(self.estado, "Debes ingresar una URL válida.", "error")
            return
        self.navegador.visitar_pagina(url)
        self.entrada_url.delete(0, "end")
        e.mensaje(self.estado, f"Visitaste {url}. La página anterior se apiló en ATRÁS "
                               "y la pila ADELANTE se vació.", "ok")
        self.actualizar()

    def retroceder(self):
        if self.navegador.pila_atras.esta_vacia():
            e.mensaje(self.estado, "No hay páginas anteriores en el historial.", "error")
            return
        self.navegador.retroceder()
        e.mensaje(self.estado, "Back: se desapiló el tope de ATRÁS y la página que "
                               "estabas viendo se apiló en ADELANTE.", "ok")
        self.actualizar()

    def avanzar(self):
        if self.navegador.pila_adelante.esta_vacia():
            e.mensaje(self.estado, "No hay páginas siguientes en el historial.", "error")
            return
        self.navegador.avanzar()
        e.mensaje(self.estado, "Forward: se desapiló el tope de ADELANTE y la página "
                               "que estabas viendo se apiló en ATRÁS.", "ok")
        self.actualizar()

    # ------------------------------------------------------------- dibujo
    def _crear_pila(self, padre, titulo):
        marco = e.panel(padre, titulo)
        marco.pack(side="left", fill="both", expand=True, padx=(0, 8))
        canvas = tk.Canvas(marco, bg=e.TARJETA, highlightthickness=0,
                           height=ALTO_CAJA * MAX_CAJAS + 20)
        canvas.pack(fill="both", expand=True)
        canvas.bind("<Configure>", lambda _evento: self.actualizar())
        return canvas

    def _dibujar_pila(self, canvas: tk.Canvas, elementos):
        canvas.delete("all")
        ancho = max(canvas.winfo_width(), 300)
        alto = max(canvas.winfo_height(), 120)
        x1, x2 = 20, ancho - 90

        if not elementos:
            canvas.create_text(ancho / 2, alto / 2, text="[ VACÍA ]",
                               font=e.F_SUBTITULO, fill=e.TEXTO_SUAVE)
            return

        visibles = elementos[-MAX_CAJAS:]           # solo los de arriba si son muchos
        y = alto - 10                                # se dibuja de abajo hacia arriba
        for i, url in enumerate(visibles):
            es_tope = i == len(visibles) - 1
            color = e.RESALTE if es_tope else "#E3ECF7"
            canvas.create_rectangle(x1, y - ALTO_CAJA + 3, x2, y, fill=color, outline=e.BORDE)
            texto = url if len(url) <= 38 else url[:35] + "..."
            canvas.create_text(x1 + 10, y - ALTO_CAJA / 2 + 1, text=texto, anchor="w",
                               font=e.F_NORMAL, fill=e.TEXTO)
            if es_tope:
                canvas.create_text(x2 + 8, y - ALTO_CAJA / 2 + 1, text="← TOPE", anchor="w",
                                   font=e.F_NEGRITA, fill=e.PELIGRO)
            y -= ALTO_CAJA
        if len(elementos) > MAX_CAJAS:
            canvas.create_text(x1, 8, anchor="nw", font=e.F_PEQUENA, fill=e.TEXTO_SUAVE,
                               text=f"... y {len(elementos) - MAX_CAJAS} más abajo")

    def actualizar(self):
        actual = self.navegador.pagina_actual
        self.lbl_actual.config(text=actual if actual else "(ninguna todavía)")
        self.btn_atras.config(state="disabled" if self.navegador.pila_atras.esta_vacia() else "normal")
        self.btn_adelante.config(state="disabled" if self.navegador.pila_adelante.esta_vacia() else "normal")
        self._dibujar_pila(self.canvas_atras, self.navegador.pila_atras.elementos)
        self._dibujar_pila(self.canvas_adelante, self.navegador.pila_adelante.elementos)
