"""Ventana gráfica del Proyecto 3: Cola de impresión (FIFO de capacidad limitada).

Usa la clase original `ColaImpresion` y las constantes `CAPACIDAD_MAXIMA`
y `COMPUTADORAS` sin modificarlas.
"""

import random
import tkinter as tk
from tkinter import ttk

from proyectos.p3_cola_impresion import CAPACIDAD_MAXIMA, COMPUTADORAS, ColaImpresion
from interfaz import estilos as e

# Un color por computadora para distinguir los trabajos en la cola
COLOR_PC = {"PC1": "#90CAF9", "PC2": "#A5D6A7", "PC3": "#FFCC80",
            "PC4": "#CE93D8", "PC5": "#EF9A9A"}


class VentanaCola:
    def __init__(self, padre: tk.Misc):
        self.cola = ColaImpresion(CAPACIDAD_MAXIMA)  # <- objeto del código original
        self.impresos = 0

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Proyecto 3 - Cola de impresión (FIFO)")
        self.ventana.geometry("860x580")
        self.ventana.configure(bg=e.FONDO)

        e.encabezado(self.ventana, 3, "Cola de impresión",
                     "Cola (FIFO: primero en entrar, primero en salir)")
        self.estado = e.barra_estado(self.ventana)

        cuerpo = tk.Frame(self.ventana, bg=e.FONDO, padx=16, pady=12)
        cuerpo.pack(fill="both", expand=True)

        # --- Controles
        controles = e.panel(cuerpo, "Agregar trabajos e imprimir")
        controles.pack(fill="x")
        fila = tk.Frame(controles, bg=e.TARJETA)
        fila.pack(fill="x")
        e.boton(fila, "Agregar (PC aleatoria)", self.agregar_aleatorio).pack(side="left")
        tk.Label(fila, text="   o elegir PC:", bg=e.TARJETA, font=e.F_NORMAL).pack(side="left")
        self.combo_pc = ttk.Combobox(fila, values=COMPUTADORAS, state="readonly", width=8)
        self.combo_pc.current(0)
        self.combo_pc.pack(side="left", padx=6)
        e.boton(fila, "Agregar PC elegida", self.agregar_seleccionado).pack(side="left")
        e.boton(fila, "🖨  Imprimir documento", self.imprimir,
                color=e.EXITO).pack(side="right")

        # --- Dibujo de la cola
        dibujo = e.panel(cuerpo, "Cola actual")
        dibujo.pack(fill="x", pady=10)
        self.lbl_capacidad = tk.Label(dibujo, font=e.F_NEGRITA, bg=e.TARJETA, fg=e.TEXTO)
        self.lbl_capacidad.pack(anchor="w")
        self.canvas = tk.Canvas(dibujo, height=150, bg=e.TARJETA, highlightthickness=0)
        self.canvas.pack(fill="x")
        self.canvas.bind("<Configure>", lambda _evento: self.dibujar())

        # --- Historial de impresión
        historial = e.panel(cuerpo, "Historial de impresión (en el orden en que salieron)")
        historial.pack(fill="both", expand=True)
        self.lista = tk.Listbox(historial, font=e.F_MONO, height=6, relief="flat",
                                bg="#FAFBFC", highlightthickness=0)
        self.lista.pack(fill="both", expand=True)

        self.dibujar()

    # ------------------------------------------------------------ acciones
    def _encolar(self, pc: str):
        if self.cola.esta_llena():
            e.mensaje(self.estado, "La cola de impresión está LLENA. Imprime un documento primero.",
                      "error")
            return
        self.cola.encolar(pc)
        e.mensaje(self.estado, f"Trabajo agregado desde {pc} al FINAL de la cola.", "ok")
        self.dibujar()

    def agregar_aleatorio(self):
        self._encolar(random.choice(COMPUTADORAS))

    def agregar_seleccionado(self):
        self._encolar(self.combo_pc.get())

    def imprimir(self):
        if self.cola.esta_vacia():
            e.mensaje(self.estado, "La cola de impresión está VACÍA. No hay nada que imprimir.",
                      "error")
            return
        pc = self.cola.desencolar()
        self.impresos += 1
        self.lista.insert("end", f"{self.impresos:>3}. Impreso documento de {pc}")
        self.lista.see("end")
        e.mensaje(self.estado, f"Se imprimió el documento de {pc} (el que estaba al FRENTE).", "ok")
        self.dibujar()

    # ------------------------------------------------------------- dibujo
    def dibujar(self):
        c = self.canvas
        c.delete("all")
        ancho = max(c.winfo_width(), 700)
        n = self.cola.capacidad
        margen = 70
        espacio = (ancho - 2 * margen) / n
        y1, y2 = 45, 115

        self.lbl_capacidad.config(text=f"Capacidad: {len(self.cola.items)}/{CAPACIDAD_MAXIMA}")

        c.create_text(margen - 10, (y1 + y2) / 2, text="FRENTE\n(sale)", anchor="e",
                      font=e.F_NEGRITA, fill=e.EXITO, justify="center")
        c.create_text(ancho - margen + 10, (y1 + y2) / 2, text="FINAL\n(entra)", anchor="w",
                      font=e.F_NEGRITA, fill=e.PRIMARIO, justify="center")

        for i in range(n):
            x1 = margen + i * espacio + 4
            x2 = x1 + espacio - 8
            if i < len(self.cola.items):
                pc = self.cola.items[i]
                c.create_rectangle(x1, y1, x2, y2, fill=COLOR_PC.get(pc, "#DDD"), outline=e.TEXTO)
                c.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 8, text="📄", font=(e.FUENTE, 14))
                c.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 18, text=pc, font=e.F_NEGRITA)
            else:
                c.create_rectangle(x1, y1, x2, y2, outline=e.BORDE, dash=(4, 3))
                c.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="libre",
                              font=e.F_PEQUENA, fill=e.TEXTO_SUAVE)
            c.create_text((x1 + x2) / 2, y2 + 14, text=f"posición {i + 1}",
                          font=e.F_PEQUENA, fill=e.TEXTO_SUAVE)

        if self.cola.esta_vacia():
            c.create_text(ancho / 2, 18, text="[ VACÍA ]", font=e.F_SUBTITULO, fill=e.TEXTO_SUAVE)
        elif self.cola.esta_llena():
            c.create_text(ancho / 2, 18, text="[ LLENA ]", font=e.F_SUBTITULO, fill=e.PELIGRO)
