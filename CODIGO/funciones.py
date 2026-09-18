
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
