
# aqui presentamos que hace cada funcion 
#la funcion obtener_colores recibe un numero podemos decir como 333 y se convierte en un string 
def obtener_colores(self, valor):
        valor_str = str(valor)
        if len(valor_str) <= 2:
            return None, None
#si el numero registrado tiene menos de dos digitos no se podra hacer el calculo necesitarias por lo menos 2 digitos para poder usar el codigo
        digito1 = int(valor_str[0])
        digito2 = int(valor_str[1])
#el str 0 y el str 1 es el primer y segundo caracter del texto y estos se convierten de vuelta a un numero entero
        multiplicador = len(valor_str) - 2 # Cantidad de ceros restantes
 # el len valor str es la cantidad de digitos que tendra en total y se resta 2 ya que se usaron los dos primeros digitos y lo que queda es la cantidad restante      
        if multiplicador > 9:
            return None, None
#si el multiplicador es mayor a 9 no representara ningun color 
        nombres = (self.colores[digito1], self.colores[digito2], self.colores[multiplicador])
        hexa = (self.codigos_hex[digito1], self.codigos_hex[digito2], self.codigos_hex[multiplicador])
 #con esta formula se usa 2 elementos una con los nombres para mostrar el texto otra para mostrar el color .      
        return nombres, hexa

    def generar_resistencias_aleatorias(self, n):
        # Genera valor de resistencias aleatorias entre 10 y 100000000
        return [random.randint(10, 1000000000) for _ in range(n)]
#recibe cuantas resistencias quieres generar y cada repeticion se genera en un valor de entre 10 y 1000000000

    def sumar_serie(self, n):
        resistencias = self.generar_resistencias_aleatorias(n)
        return sum(resistencias), resistencias
#llama a la funcion anterior para guardar esas resistencias y suma todos los valores del arreglo

    def sumar_paralelo(self, n):
        resistencias = self.generar_resistencias_aleatorias(n)
        inversas = sum([1/r for r in resistencias])
        return 1/inversas, resistencias
#llama a la funcion anterior para guardar esas resistencias y suma todos los valores del arreglo
