# Arquitectura del proyecto integrador

[← Volver al README](../README.md)

## 1. Objetivo

Juntar los 6 proyectos de la materia en **un solo programa** que, al ejecutarse, deje **elegir cuál de los 6 abrir**, con **interfaz gráfica**, y **sin cambiar el código original** de cada proyecto.

## 2. Las tres capas

```
            ┌──────────────────────────────┐
            │           main.py            │   Menú principal (6 botones)
            └──────────────┬───────────────┘
                           │ abre
            ┌──────────────▼───────────────┐
            │          interfaz/           │   Una ventana Tkinter por proyecto
            │  ventana_navegador.py, ...   │   (botones, tablas, dibujos)
            └──────────────┬───────────────┘
                           │ importa y usa las clases
            ┌──────────────▼───────────────┐
            │          proyectos/          │   Código original de cada proyecto
            │  p1_navegador_web.py, ...    │   (las estructuras de datos)
            └──────────────────────────────┘
```

| Capa | Qué contiene | ¿Se modificó? |
|------|--------------|---------------|
| `proyectos/` | Las clases y la lógica (Pila, ColaImpresion, Carrito, ArbolBinarioBusqueda, GrafoPueblosMagicos…) y su menú de consola | **No.** Son los códigos entregados tal cual. El 5 es nuevo. |
| `interfaz/` | Las ventanas gráficas | Es código nuevo |
| `main.py` | El menú con las 6 opciones | Es código nuevo |

A esto se le llama **separar la lógica de la presentación**: la estructura de datos no sabe nada de botones ni ventanas, y la ventana no reimplementa la estructura, solo la usa.

## 3. `main.py` paso a paso

1. **`PROYECTOS`**: lista con número, nombre, estructura y descripción de cada proyecto. Con ella se dibujan las 6 tarjetas del menú (y el menú de consola), así no se repite texto.
2. **`MenuPrincipal.__init__`**: crea la ventana raíz (`tk.Tk()`), el encabezado azul y una rejilla de 3 × 2 tarjetas.
3. **`MenuPrincipal.abrir(numero)`**:
   - Si es el **2**, ejecuta `proyectos/p2_resistencias.py` con `subprocess.Popen`, porque ese archivo ya crea su propia ventana Tkinter al ejecutarse (crea `tk.Tk()` desde el inicio del archivo, así que no se puede importar sin que se abra).
   - Si la ventana del proyecto **ya está abierta**, solo la trae al frente (no abre otra).
   - Si no, importa la ventana correspondiente de `interfaz/` y la crea como `Toplevel` (ventana secundaria de la principal).
4. **`menu_consola()`**: con `python main.py --consola` se muestra un menú en la terminal que llama directamente a los menús originales (`p1_navegador_web.menu()`, `SistemaCarrito().ejecutar()`, etc.). Sirve para demostrar que los programas originales siguen funcionando igual.

## 4. Cómo está hecha cada ventana (`interfaz/`)

Todas siguen el mismo patrón:

```python
class VentanaX:
    def __init__(self, padre):
        self.objeto = ClaseOriginal()           # 1. se crea el objeto del proyecto
        self.ventana = tk.Toplevel(padre)       # 2. se crea la ventana
        e.encabezado(...)                       # 3. barra de color con el título
        self.estado = e.barra_estado(...)       # 4. barra inferior de mensajes
        ...                                     # 5. botones, tablas y Canvas

    def accion(self):                           # cada botón:
        # a) valida lo que escribió el usuario
        # b) llama al método ORIGINAL (encolar, insertar, dijkstra...)
        # c) escribe un mensaje en la barra de estado
        # d) vuelve a dibujar
```

- Los **mensajes** que en consola eran `print(...)` aquí aparecen en la **barra de estado** de abajo (verde si salió bien y rojo si hubo un error).
- Los métodos originales todavía hacen sus `print`, que aparecen en la terminal desde donde se ejecutó `main.py`. Es normal y no afecta.
- Los **dibujos** (pilas, cola, árbol, grafo) se hacen con `tk.Canvas` leyendo el estado del objeto: `pila.elementos`, `cola.items`, `arbol.raiz`, `grafo.adyacencia`.
- **`estilos.py`** tiene los colores y funciones como `boton()`, `panel()` y `encabezado()` para que las 6 ventanas se vean iguales.

## 5. ¿Por qué no se pegó todo en un solo `.py`?

Se intentó respetar la idea de "todo en uno" pero sin romper nada:

- Dos archivos originales tienen una función llamada `menu()` (Navegador y Cola) y se pisarían entre sí.
- `p2_resistencias.py` abre su ventana en cuanto se ejecuta el archivo, así que al pegarlo se abriría solo.
- Separado en archivos es más fácil de explicar: cada integrante puede abrir **su** archivo y verlo igual que como lo entregó.

Aun así, el programa **se ejecuta desde un solo archivo** (`main.py`) y desde ahí se elige cualquiera de los 6.
