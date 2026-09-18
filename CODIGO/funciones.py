
def obtener_colores(self, valor):
        valor_str = str(valor)
        if len(valor_str) <= 2:
            return None, None
        digito1 = int(valor_str[0])
        digito2 = int(valor_str[1])
        multiplicador = len(valor_str) - 2 # Cantidad de ceros restantes 
        if multiplicador > 9:
            return None, None

        nombres = (self.colores[digito1], self.colores[digito2], self.colores[multiplicador])
        hexa = (self.codigos_hex[digito1], self.codigos_hex[digito2], self.codigos_hex[multiplicador]).      
        return nombres, hexa

    def generar_resistencias_aleatorias(self, n):
        return [random.randint(10, 1000000000) for _ in range(n)]
    def sumar_serie(self, resistencias):
        return sum(resistencias)
    def sumar_paralelo(self, resistencias):
        return 1 / sum(1 / r for r in resistencias)
def calcular_grafico():
    try:
        r = Resistencia()
        
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
            resistencias = r.generar_resistencias_aleatorias(n)
            total_serie = r.sumar_serie(resistencias)
            total_paralelo = r.sumar_paralelo(resistencias)
            
            resultado_sumas.config(text=f"Resistencias: {resistencias} Ω\n"
                                        f"Suma Serie: {total_serie:,} Ω\n"
                                        f"Suma paralelo: {total_paralelo:,.4f} Ω")
        else:
            messagebox.showerror("Error", "n debe ser mayor que 0.")
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa números válidos.")
