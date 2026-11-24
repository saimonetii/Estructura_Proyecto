import random

CAPACIDAD_MAXIMA = 6
COMPUTADORAS = ["PC1", "PC2", "PC3", "PC4", "PC5"]


class ColaImpresion:

    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def esta_llena(self):
        return len(self.items) >= self.capacidad

    def encolar(self, elemento):
        if self.esta_llena():
            return False
        self.items.append(elemento)
        return True

    def desencolar(self):
        if self.esta_vacia():
            return None
        return self.items.pop(0)


def mostrar_cola(cola):
    print("\n================ COLA ACTUAL ================")
    if cola.esta_vacia():
        print("[ VACIA ]")
    else:
        print(" -> ".join(cola.items))
    print(f"Capacidad: {len(cola.items)}/{CAPACIDAD_MAXIMA}")
    print("=============================================\n")


def menu():
    cola = ColaImpresion(CAPACIDAD_MAXIMA)

    while True:
        print("--- PROYECTO COLA DE IMPRESION ---")
        print("1. Agregar trabajo (PC Aleatoria)")
        print("2. Agregar trabajo (Seleccionar PC)")
        print("3. Imprimir documento")
        print("4. Mostrar cola de impresion")
        print("5. Salir")

        opcion = input("Selecciona una opcion (1-5): ")

        if opcion == "1":
            if cola.esta_llena():
                print("\nLa cola de impresion esta LLENA")
            else:
                pc = random.choice(COMPUTADORAS)
                cola.encolar(pc)
                print(f"\nTrabajo agregado desde {pc}")
            mostrar_cola(cola)

        elif opcion == "2":
            if cola.esta_llena():
                print("\nLa cola de impresion esta LLENA")
                mostrar_cola(cola)
            else:
                print("\nPCs disponibles:", ", ".join(COMPUTADORAS))
                pc = input("Ingresa el nombre de la PC: ").strip().upper()
                if pc in COMPUTADORAS:
                    cola.encolar(pc)
                    print(f"\nTrabajo agregado desde {pc}")
                else:
                    print("\nPC no valida.")
                mostrar_cola(cola)

        elif opcion == "3":
            if cola.esta_vacia():
                print("\nLa cola de impresion esta VACIA")
            else:
                pc_atendida = cola.desencolar()
                print(f"\nImpresion {pc_atendida}")
            mostrar_cola(cola)

        elif opcion == "4":
            mostrar_cola(cola)

        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("\nOpcion no valida. Intenta de nuevo.\n")


if __name__ == "__main__":
    menu()
