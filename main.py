#Aqui se presenta el codigo completo con el uso completo que se pidio en el proyecto 

import tkinter as tk
from tkinter import messagebox
import random

class Resistencia:
    def __init__(self):
        # Arreglos de colores 
        self.colores = ["Negro", "Marrón", "Rojo", "Naranja", "Amarillo", 
                        "Verde", "Azul", "Violeta", "Gris", "Blanco"]
        self.codigos_hex = ["#000000", "#8B4513", "#FF0000", "#FFA500", "#FFFF00", 
                            "#008000", "#0000FF", "#EE82EE", "#808080", "#FFFFFF"]

    def obtener_colores(self, valor):
        valor_str = str(valor)
        if len(valor_str) < 2:
            return None, None
            
        digito1 = int(valor_str[0])
        digito2 = int(valor_str[1])
        multiplicador = len(valor_str) - 2 # Cantidad de ceros restantes
        
        if multiplicador > 9:
            return None, None

        nombres = (self.colores[digito1], self.colores[digito2], self.colores[multiplicador])
        hexa = (self.codigos_hex[digito1], self.codigos_hex[digito2], self.codigos_hex[multiplicador])
        
        return nombres, hexa

    def generar_resistencias_aleatorias(self, n):
        # Genera valor de resistencias aleatorias entre 10 y 100000000
        return [random.randint(10, 1000000000) for _ in range(n)]

    def sumar_serie(self, n):
        resistencias = self.generar_resistencias_aleatorias(n)
        return sum(resistencias), resistencias

    def sumar_paralelo(self, n):
        resistencias = self.generar_resistencias_aleatorias(n)
        inversas = sum([1/r for r in resistencias])
        return 1/inversas, resistencias

#Interfaz para la aplicacion
def calcular_grafico():
    try:
        r = Resistencia()
        
        #Calculo de colores
        valor_resistencia = int(entry_valor.get())
        nombres_colores, codigos_hex = r.obtener_colores(valor_resistencia)
        
        if nombres_colores:
            lbl_color1.config(bg=codigos_hex[0], text=nombres_colores[0], fg="white" if codigos_hex[0]=="#000000" else "black")
            lbl_color2.config(bg=codigos_hex[1], text=nombres_colores[1], fg="white" if codigos_hex[1]=="#000000" else "black")
            lbl_color3.config(bg=codigos_hex[2], text=nombres_colores[2], fg="white" if codigos_hex[2]=="#000000" else "black")
            resultado_colores.config(text=f"Colores: {nombres_colores[0]}, {nombres_colores[1]}, {nombres_colores[2]}")
        else:
            messagebox.showerror("Error", "Valor no válido para el cálculo básico de 3 bandas.")

        #Sumas en serie y paralelo
        n = int(entry_n.get())
        if n > 0:
            total_serie, res_serie = r.sumar_serie(n)
            total_paralelo, res_paralelo = r.sumar_paralelo(n)
            
            resultado_sumas.config(text=f"Suma Serie: {total_serie} Ω\n"
                                        f"Suma Paralelo: {total_paralelo:.4f} Ω")
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa números válidos.")

#Tkinter
root = tk.Tk()
root.title("Proyecto Resistencia Eléctrica")
root.geometry("400x450")

tk.Label(root, text="Valor de la Resistencia (Ohmios):").pack(pady=5)
entry_valor = tk.Entry(root)
entry_valor.pack(pady=5)

tk.Label(root, text="Cantidad de resistencias (n):").pack(pady=5)
entry_n = tk.Entry(root)
entry_n.pack(pady=5)

tk.Button(root, text="Calcular", command=calcular_grafico).pack(pady=15)

# Visualización de grafica de colores
frame_colores = tk.Frame(root)
frame_colores.pack(pady=10)

lbl_color1 = tk.Label(frame_colores, width=10, height=2, borderwidth=2, relief="groove")
lbl_color1.grid(row=0, column=0, padx=5)
lbl_color2 = tk.Label(frame_colores, width=10, height=2, borderwidth=2, relief="groove")
lbl_color2.grid(row=0, column=1, padx=5)
lbl_color3 = tk.Label(frame_colores, width=10, height=2, borderwidth=2, relief="groove")
lbl_color3.grid(row=0, column=2, padx=5)

resultado_colores = tk.Label(root, text="")
resultado_colores.pack(pady=5)

resultado_sumas = tk.Label(root, text="", justify=tk.LEFT)
resultado_sumas.pack(pady=15)

root.mainloop()
