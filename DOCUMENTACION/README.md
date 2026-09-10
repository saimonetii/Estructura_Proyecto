# Estructura_Proyecto
Esta es la documentacion del proyecto de estructuras de datos que se entregara el 20 de septiembre del año 2026
Este proyecto es una aplicacion grafica que permite determinar los colores de una resistencia y obtener las sumas de resistencias en serie y paralelos esto con ayuda de arreglos

Este proyecto usa arreglos y listas para poder representar:
- Los nombres de los colores de la tabla de codigos y resistencias.
- Codigos Hexadecimales que se usan para poder pintar los resultados en la interfaz grafica
- los valores de N resistencias generadas aleatoriamente donde se calcula suma en serie y paralelo

#TABLA DE COLORES QUE SE USO EN EL PROYECTO
<img width="965" height="419" alt="image" src="https://github.com/user-attachments/assets/fd485875-72f0-4c62-87c3-881506c48f41" />

#Funcion del codigo
Con un valor entero este tiene que ser un numero mayor a 3 digitos se puede presentar graficammente en la interfaz esto mostrando sus respectivos colores. Un ejemplo de esto es que yo ponga el numero respecto a la tabla 123
el calculo asumira que el valor agregado correspondera a dos digitos estos seguidos de ceros.

#la suma en serie
Usando funciones generamos una resistencia aleatoria esto con numeros entre el numero 10 y 1000000000 y se calcula con la formula.
RTS: R1 + R2 + R3... + RN
#la suma en paralelo
Lo mismo que en la serie solo que con la diferencia es en la formula que es.
RTP: 1/R1 + 1/R2 + 1/R3 + ... + 1/RN

