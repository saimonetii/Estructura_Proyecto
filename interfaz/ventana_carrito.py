"""Ventana gráfica del Proyecto 4: Carrito de compras (listas de objetos y búsqueda).

Usa las clases originales `SistemaCarrito`, `Carrito`, `ElementoCarrito` y
`Producto` sin modificarlas: el catálogo y las búsquedas vienen de
`SistemaCarrito`, y las operaciones del carrito de `Carrito`.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from proyectos.p4_carrito_compras import SistemaCarrito
from interfaz import estilos as e


class VentanaCarrito:
    def __init__(self, padre: tk.Misc):
        self.sistema = SistemaCarrito()          # <- objeto del código original
        self.carrito = self.sistema.carrito      # lista de ElementoCarrito

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Proyecto 4 - Carrito de compras (Listas)")
        self.ventana.geometry("1060x600")
        self.ventana.configure(bg=e.FONDO)

        e.encabezado(self.ventana, 4, "Carrito de compras",
                     "Listas de objetos + búsqueda por ID y por nombre")
        self.estado = e.barra_estado(self.ventana)

        cuerpo = tk.Frame(self.ventana, bg=e.FONDO, padx=16, pady=12)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(0, weight=2)
        cuerpo.columnconfigure(1, weight=3)
        cuerpo.rowconfigure(0, weight=1)

        self._armar_catalogo(cuerpo)
        self._armar_carrito(cuerpo)
        self.mostrar_catalogo(self.sistema.catalogo)
        self.actualizar_carrito()

    # ============================================================ CATÁLOGO
    def _armar_catalogo(self, cuerpo):
        izq = e.panel(cuerpo, "Catálogo de productos")
        izq.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        busqueda = tk.Frame(izq, bg=e.TARJETA)
        busqueda.pack(fill="x", pady=(0, 6))
        tk.Label(busqueda, text="Buscar (ID o nombre):", bg=e.TARJETA,
                 font=e.F_NORMAL).pack(side="left")
        self.texto_busqueda = tk.StringVar()
        self.texto_busqueda.trace_add("write", lambda *_: self.buscar())
        tk.Entry(busqueda, textvariable=self.texto_busqueda, font=e.F_NORMAL,
                 relief="solid", bd=1).pack(side="left", fill="x", expand=True, padx=6, ipady=3)

        self.tabla_catalogo = ttk.Treeview(izq, columns=("id", "nombre", "precio"),
                                           show="headings", height=10, selectmode="browse")
        for col, titulo, ancho, alin in (("id", "ID", 60, "center"),
                                         ("nombre", "Producto", 170, "w"),
                                         ("precio", "Precio", 90, "e")):
            self.tabla_catalogo.heading(col, text=titulo)
            self.tabla_catalogo.column(col, width=ancho, anchor=alin)
        self.tabla_catalogo.pack(fill="both", expand=True)
        self.tabla_catalogo.bind("<Double-1>", lambda _evento: self.agregar())

        abajo = tk.Frame(izq, bg=e.TARJETA)
        abajo.pack(fill="x", pady=(8, 0))
        tk.Label(abajo, text="Cantidad:", bg=e.TARJETA, font=e.F_NORMAL).pack(side="left")
        self.cantidad = tk.Spinbox(abajo, from_=1, to=999, width=5, font=e.F_NORMAL)
        self.cantidad.pack(side="left", padx=6)
        e.boton(abajo, "Agregar al carrito ➜", self.agregar, color=e.EXITO).pack(side="right")

    def mostrar_catalogo(self, productos):
        self.tabla_catalogo.delete(*self.tabla_catalogo.get_children())
        for p in productos:
            self.tabla_catalogo.insert("", "end", iid=str(p.id_producto),
                                       values=(p.id_producto, p.nombre, f"${p.precio:.2f}"))

    def buscar(self):
        texto = self.texto_busqueda.get().strip()
        if not texto:
            self.mostrar_catalogo(self.sistema.catalogo)
            e.mensaje(self.estado, "Mostrando el catálogo completo.")
            return
        if texto.isdigit():   # búsqueda por ID
            producto = self.sistema.buscar_producto_por_id(int(texto))
            resultados = [producto] if producto else []
        else:                 # búsqueda por nombre (o parte del nombre)
            resultados = self.sistema.buscar_productos_por_nombre(texto)
        self.mostrar_catalogo(resultados)
        if resultados:
            e.mensaje(self.estado, f"{len(resultados)} coincidencia(s) para '{texto}'.", "ok")
        else:
            e.mensaje(self.estado, f"No se encontraron productos para '{texto}'.", "error")

    def _leer_cantidad(self, spin):
        try:
            cantidad = int(spin.get())
        except ValueError:
            cantidad = 0
        if cantidad < 1:
            e.mensaje(self.estado, "La cantidad debe ser un número entero mayor o igual a 1.",
                      "error")
            return None
        return cantidad

    def agregar(self):
        seleccion = self.tabla_catalogo.selection()
        if not seleccion:
            e.mensaje(self.estado, "Selecciona un producto del catálogo primero.", "error")
            return
        cantidad = self._leer_cantidad(self.cantidad)
        if cantidad is None:
            return
        producto = self.sistema.buscar_producto_por_id(int(seleccion[0]))
        ya_estaba = self.carrito.buscar_por_id(producto.id_producto) is not None
        self.carrito.agregar_producto(producto, cantidad)
        if ya_estaba:
            total = self.carrito.buscar_por_id(producto.id_producto).cantidad
            e.mensaje(self.estado, f"La cantidad de {producto.nombre} se actualizó a {total}.", "ok")
        else:
            e.mensaje(self.estado, f"{producto.nombre} se agregó al carrito.", "ok")
        self.actualizar_carrito(seleccionar=producto.id_producto)

    # ============================================================= CARRITO
    def _armar_carrito(self, cuerpo):
        der = e.panel(cuerpo, "Mi carrito")
        der.grid(row=0, column=1, sticky="nsew")

        columnas = ("id", "nombre", "cantidad", "unitario", "subtotal")
        self.tabla_carrito = ttk.Treeview(der, columns=columnas, show="headings",
                                          height=10, selectmode="browse")
        for col, titulo, ancho, alin in (("id", "ID", 50, "center"),
                                         ("nombre", "Producto", 160, "w"),
                                         ("cantidad", "Cant.", 60, "center"),
                                         ("unitario", "P. unitario", 100, "e"),
                                         ("subtotal", "Subtotal", 100, "e")):
            self.tabla_carrito.heading(col, text=titulo)
            self.tabla_carrito.column(col, width=ancho, anchor=alin)
        self.tabla_carrito.pack(fill="both", expand=True)
        self.tabla_carrito.bind("<<TreeviewSelect>>", lambda _evento: self._copiar_cantidad())

        fila = tk.Frame(der, bg=e.TARJETA)
        fila.pack(fill="x", pady=(8, 0))
        tk.Label(fila, text="Nueva cantidad:", bg=e.TARJETA, font=e.F_NORMAL).pack(side="left")
        self.nueva_cantidad = tk.Spinbox(fila, from_=1, to=999, width=5, font=e.F_NORMAL)
        self.nueva_cantidad.pack(side="left", padx=6)
        e.boton(fila, "Modificar", self.modificar).pack(side="left")
        e.boton(fila, "Eliminar", self.eliminar, color=e.PELIGRO).pack(side="left", padx=6)
        e.boton(fila, "Vaciar carrito", self.vaciar, color=e.TEXTO_SUAVE).pack(side="left")

        totales = tk.Frame(der, bg=e.TARJETA)
        totales.pack(fill="x", pady=(10, 0))
        self.lbl_total = tk.Label(totales, font=e.F_SUBTITULO, bg=e.TARJETA, fg=e.TEXTO)
        self.lbl_total.pack(side="left")
        e.boton(totales, "Finalizar compra ✔", self.finalizar, color=e.EXITO).pack(side="right")

    def actualizar_carrito(self, seleccionar=None):
        self.tabla_carrito.delete(*self.tabla_carrito.get_children())
        for elemento in self.carrito.elementos:
            p = elemento.producto
            self.tabla_carrito.insert("", "end", iid=str(p.id_producto), values=(
                p.id_producto, p.nombre, elemento.cantidad,
                f"${p.precio:.2f}", f"${elemento.calcular_subtotal():.2f}"))
        if seleccionar is not None and self.tabla_carrito.exists(str(seleccionar)):
            self.tabla_carrito.selection_set(str(seleccionar))
        self.lbl_total.config(
            text=f"Artículos: {self.carrito.calcular_cantidad_total()}    "
                 f"Total: ${self.carrito.calcular_total():.2f}")

    def _elemento_seleccionado(self):
        seleccion = self.tabla_carrito.selection()
        if not seleccion:
            if self.carrito.esta_vacio():
                e.mensaje(self.estado, "El carrito está vacío.", "error")
            else:
                e.mensaje(self.estado, "Selecciona un producto del carrito primero.", "error")
            return None
        return self.carrito.buscar_por_id(int(seleccion[0]))

    def _copiar_cantidad(self):
        elemento = self._elemento_seleccionado()
        if elemento is not None:
            self.nueva_cantidad.delete(0, "end")
            self.nueva_cantidad.insert(0, str(elemento.cantidad))

    def modificar(self):
        elemento = self._elemento_seleccionado()
        if elemento is None:
            return
        cantidad = self._leer_cantidad(self.nueva_cantidad)
        if cantidad is None:
            return
        self.carrito.modificar_cantidad(elemento, cantidad)
        e.mensaje(self.estado, f"Cantidad actualizada. Subtotal: ${elemento.calcular_subtotal():.2f}",
                  "ok")
        self.actualizar_carrito(seleccionar=elemento.producto.id_producto)

    def eliminar(self):
        elemento = self._elemento_seleccionado()
        if elemento is None:
            return
        self.carrito.eliminar_producto(elemento)
        e.mensaje(self.estado, f"{elemento.producto.nombre} se eliminó del carrito.", "ok")
        self.actualizar_carrito()

    def vaciar(self):
        if self.carrito.esta_vacio():
            e.mensaje(self.estado, "El carrito ya está vacío.", "error")
            return
        if messagebox.askyesno("Vaciar carrito", "¿Vaciar todo el carrito?", parent=self.ventana):
            self.carrito.vaciar()
            e.mensaje(self.estado, "El carrito se vació correctamente.", "ok")
            self.actualizar_carrito()
        else:
            e.mensaje(self.estado, "La operación se canceló.")

    def finalizar(self):
        if self.carrito.esta_vacio():
            e.mensaje(self.estado, "No es posible finalizar una compra con el carrito vacío.", "error")
            return
        lineas = [f"{el.cantidad} x {el.producto.nombre}  =  ${el.calcular_subtotal():.2f}"
                  for el in self.carrito.elementos]
        resumen = ("\n".join(lineas)
                   + f"\n\nCantidad total de artículos: {self.carrito.calcular_cantidad_total()}"
                   + f"\nMonto total a pagar: ${self.carrito.calcular_total():.2f}")
        messagebox.showinfo("Resumen final de compra", resumen, parent=self.ventana)
        e.mensaje(self.estado, "Compra finalizada. Puedes seguir modificando el carrito o vaciarlo.",
                  "ok")
