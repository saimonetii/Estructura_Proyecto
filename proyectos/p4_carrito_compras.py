from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Producto:

    id_producto: int
    nombre: str
    precio: float

@dataclass
class ElementoCarrito:
    producto: Producto
    cantidad: int
    def calcular_subtotal(self) -> float:
        return self.producto.precio * self.cantidad

    def actualizar_cantidad(self, nueva_cantidad: int) -> None:
        self.cantidad = nueva_cantidad


class Carrito:
    def __init__(self) -> None:
        self.elementos: List[ElementoCarrito] = []

    def buscar_por_id(self, id_producto: int) -> Optional[ElementoCarrito]:
        for elemento in self.elementos:
            if elemento.producto.id_producto == id_producto:
                return elemento
        return None

    def buscar_por_nombre(self, nombre: str) -> Optional[ElementoCarrito]:
        nombre_normalizado = nombre.strip().casefold()
        for elemento in self.elementos:
            if elemento.producto.nombre.casefold() == nombre_normalizado:
                return elemento
        return None

    def agregar_producto(self, producto: Producto, cantidad: int) -> None:
        elemento = self.buscar_por_id(producto.id_producto)
        if elemento is None:
            self.elementos.append(ElementoCarrito(producto, cantidad))
            print(f"\n{producto.nombre} se agregó al carrito.")
        else:
            elemento.cantidad += cantidad
            print(
                f"\nLa cantidad de {producto.nombre} se actualizó a "
                f"{elemento.cantidad}."
            )

    def modificar_cantidad(self, elemento: ElementoCarrito, cantidad: int) -> None:
        elemento.actualizar_cantidad(cantidad)
        print(f"\nCantidad actualizada. Subtotal: ${elemento.calcular_subtotal():.2f}")

    def eliminar_producto(self, elemento: ElementoCarrito) -> None:
        self.elementos.remove(elemento)
        print(f"\n{elemento.producto.nombre} se eliminó del carrito.")

    def vaciar(self) -> None:
        self.elementos.clear()

    def esta_vacio(self) -> bool:
        return len(self.elementos) == 0

    def calcular_total(self) -> float:
        return sum(elemento.calcular_subtotal() for elemento in self.elementos)

    def calcular_cantidad_total(self) -> int:
        return sum(elemento.cantidad for elemento in self.elementos)

    def mostrar_detalle(self) -> None:
        if self.esta_vacio():
            print("\nEl carrito está vacío.")
            return

        print("\n" + "=" * 73)
        print("CARRITO DE COMPRAS")
        print("=" * 73)
        print(f"{'ID':<8}{'Producto':<25}{'Cant.':>8}{'P. unitario':>15}{'Subtotal':>15}")
        print("-" * 73)
        for elemento in self.elementos:
            producto = elemento.producto
            print(
                f"{producto.id_producto:<8}{producto.nombre:<25}{elemento.cantidad:>8} "
                f"${producto.precio:>13.2f}  ${elemento.calcular_subtotal():>13.2f}"
            )
        print("-" * 73)
        print(f"Total acumulado: ${self.calcular_total():.2f}")


class SistemaCarrito:
    def __init__(self) -> None:
        self.catalogo: List[Producto] = []
        self.carrito = Carrito()
        self.cargar_catalogo()

    def cargar_catalogo(self) -> None:
        self.catalogo = [
            Producto(101, "Leche", 28.50),
            Producto(102, "Pan integral", 42.00),
            Producto(103, "Huevos", 58.00),
            Producto(104, "Arroz", 31.50),
            Producto(105, "Manzanas", 49.90),
        ]

    @staticmethod
    def pedir_entero(mensaje: str, minimo: Optional[int] = None) -> int:
        while True:
            try:
                valor = int(input(mensaje).strip())
                if minimo is not None and valor < minimo:
                    print(f"El valor debe ser mayor o igual a {minimo}.")
                    continue
                return valor
            except ValueError:
                print("Entrada no válida. Escribe un número entero.")

    @staticmethod
    def pedir_texto(mensaje: str) -> str:
        while True:
            texto = input(mensaje).strip()
            if texto:
                return texto
            print("La entrada no puede quedar vacía.")

    def mostrar_catalogo(self) -> None:
        print("\n" + "=" * 48)
        print("CATÁLOGO DE PRODUCTOS")
        print("=" * 48)
        print(f"{'ID':<8}{'Producto':<25}{'Precio':>15}")
        print("-" * 48)
        for producto in self.catalogo:
            print(f"{producto.id_producto:<8}{producto.nombre:<25}${producto.precio:>13.2f}")

    def buscar_producto_por_id(self, id_producto: int) -> Optional[Producto]:
        for producto in self.catalogo:
            if producto.id_producto == id_producto:
                return producto
        return None

    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        criterio = nombre.strip().casefold()
        return [
            producto
            for producto in self.catalogo
            if criterio in producto.nombre.casefold()
        ]

    @staticmethod
    def mostrar_producto(producto: Producto) -> None:
        print(
            f"ID: {producto.id_producto} | Producto: {producto.nombre} | "
            f"Precio: ${producto.precio:.2f}"
        )

    def consultar_catalogo(self) -> None:
        print("\nBuscar producto por")
        print("1. ID")
        print("2. Nombre")
        opcion = self.pedir_entero("Opción: ", 1)
        if opcion == 1:
            producto = self.buscar_producto_por_id(self.pedir_entero("ID del producto: ", 1))
            if producto is None:
                print("\nNo se encontró un producto con ese ID.")
            else:
                self.mostrar_producto(producto)
        elif opcion == 2:
            coincidencias = self.buscar_productos_por_nombre(
                self.pedir_texto("Nombre o parte del nombre: ")
            )
            if not coincidencias:
                print("\nNo se encontraron productos con ese nombre.")
            else:
                print("\nCoincidencias encontradas:")
                for producto in coincidencias:
                    self.mostrar_producto(producto)
        else:
            print("\nOpción no válida.")

    def seleccionar_producto_catalogo(self) -> Optional[Producto]:
        print("\nSeleccionar producto por")
        print("1. ID")
        print("2. Nombre")
        opcion = self.pedir_entero("Opción: ", 1)
        if opcion == 1:
            return self.buscar_producto_por_id(self.pedir_entero("ID del producto: ", 1))
        if opcion == 2:
            coincidencias = self.buscar_productos_por_nombre(
                self.pedir_texto("Nombre o parte del nombre: ")
            )
            if len(coincidencias) == 1:
                return coincidencias[0]
            if len(coincidencias) > 1:
                print("\nSelecciona uno de los resultados mediante su ID:")
                for producto in coincidencias:
                    self.mostrar_producto(producto)
                return self.buscar_producto_por_id(self.pedir_entero("ID elegido: ", 1))
            return None
        print("\nOpción no válida.")
        return None

    def agregar_al_carrito(self) -> None:
        producto = self.seleccionar_producto_catalogo()
        if producto is None:
            print("\nEl producto no existe en el catálogo.")
            return
        cantidad = self.pedir_entero("Cantidad: ", 1)
        self.carrito.agregar_producto(producto, cantidad)

    def seleccionar_elemento_carrito(self) -> Optional[ElementoCarrito]:
        if self.carrito.esta_vacio():
            print("\nEl carrito está vacío.")
            return None
        print("\nBuscar producto del carrito por")
        print("1. ID")
        print("2. Nombre")
        opcion = self.pedir_entero("Opción: ", 1)
        if opcion == 1:
            return self.carrito.buscar_por_id(self.pedir_entero("ID del producto: ", 1))
        if opcion == 2:
            return self.carrito.buscar_por_nombre(self.pedir_texto("Nombre del producto: "))
        print("\nOpción no válida.")
        return None

    def modificar_carrito(self) -> None:
        elemento = self.seleccionar_elemento_carrito()
        if elemento is None:
            print("\nNo se encontró el producto en el carrito.")
            return
        nueva_cantidad = self.pedir_entero("Nueva cantidad: ", 1)
        self.carrito.modificar_cantidad(elemento, nueva_cantidad)

    def eliminar_del_carrito(self) -> None:
        elemento = self.seleccionar_elemento_carrito()
        if elemento is None:
            print("\nNo se encontró el producto en el carrito.")
            return
        self.carrito.eliminar_producto(elemento)

    def vaciar_carrito(self) -> None:
        if self.carrito.esta_vacio():
            print("\nEl carrito ya está vacío.")
            return
        respuesta = self.pedir_texto("¿Vaciar todo el carrito? (S/N): ").casefold()
        if respuesta == "s":
            self.carrito.vaciar()
            print("\nEl carrito se vació correctamente.")
        else:
            print("\nLa operación se canceló.")

    def finalizar_compra(self) -> None:
        if self.carrito.esta_vacio():
            print("\nNo es posible finalizar una compra con el carrito vacío.")
            return
        print("\n" + "=" * 73)
        print("RESUMEN FINAL DE COMPRA")
        self.carrito.mostrar_detalle()
        print(f"Cantidad total de artículos: {self.carrito.calcular_cantidad_total()}")
        print(f"Monto total a pagar: ${self.carrito.calcular_total():.2f}")
        print("=" * 73)

    @staticmethod
    def mostrar_menu() -> None:
        print("SISTEMA DE CARRITO DE COMPRAS")
        print("=------------------------------=")
        print("\n1. Ver catálogo completo")
        print("2. Buscar producto en el catálogo")
        print("3. Agregar producto al carrito")
        print("4. Ver carrito de compras")
        print("5. Modificar cantidad de un producto")
        print("6. Eliminar producto del carrito")
        print("7. Vaciar carrito")
        print("8. Finalizar compra")
        print("0. Salir")

    def ejecutar(self) -> None:
        acciones = {
            1: self.mostrar_catalogo,
            2: self.consultar_catalogo,
            3: self.agregar_al_carrito,
            4: self.carrito.mostrar_detalle,
            5: self.modificar_carrito,
            6: self.eliminar_del_carrito,
            7: self.vaciar_carrito,
            8: self.finalizar_compra,
        }
        while True:
            self.mostrar_menu()
            opcion = self.pedir_entero("Selecciona una opción: ", 0)
            if opcion == 0:
                print("\nGracias por usar el sistema de carrito de compras.")
                break
            accion = acciones.get(opcion)
            if accion is None:
                print("\nOpción no válida. Intenta de nuevo.")
            else:
                accion()
                
if __name__ == "__main__":
    SistemaCarrito().ejecutar()