# Mini Optimizer

Optimizador de código de tres direcciones implementado en Python. El proyecto
recibe un archivo TAC, lo representa internamente por bloques básicos y aplica
varios pases de optimización hasta que el resultado deja de cambiar o se
alcanza el máximo de iteraciones.

## Pases de optimización

- **Peephole:** elimina asignaciones redundantes, simplifica operaciones
  algebraicas (`x + 0`, `x - 0`, `x * 1`), redirige saltos, fusiona labels
  consecutivos y elimina saltos hacia el siguiente label.
- **Propagation:** propaga expresiones dentro de cada bloque.
- **SubExpression:** reutiliza subexpresiones comunes y propaga alias.
- **DeadCode:** elimina temporales calculados que ya no se utilizan.

El orden de ejecución está definido en [main.py](./main.py). El programa
reporta el número de líneas antes y después de optimizar, además del porcentaje
de reducción.

## Requisitos

- Python 3.9 o posterior.
- No se requieren dependencias externas para el optimizador.
- Para ejecutar el compilador se necesita `ply`; sus instrucciones están en
  [Compiler/README.md](./Compiler/README.md).

## Uso

Coloca el código TAC de entrada en `code.tac` y ejecuta:

```bash
python3 main.py
```

El resultado se imprime en la terminal y se escribe en `optimized.tac`.

Ejemplo de salida:

```text
Iteraciones: 2
Líneas: 90 -> 65
Optimización: 27.78% (eliminadas 25)
```

Los archivos `code.tac` y `optimized.tac` son salidas generadas y están
excluidos del repositorio mediante `.gitignore`.

## Flujo completo

1. Escribe o modifica el programa de alto nivel en
   [Compiler/main.py](./Compiler/main.py).
2. Genera el código de tres direcciones:

   ```bash
   cd Compiler
   python3 main.py > ../code.tac
   cd ..
   ```

3. Optimiza el TAC:

   ```bash
   python3 main.py
   ```

4. Copia el contenido de `optimized.tac` al simulador para ejecutarlo.

## Simulador

El código TAC generado y optimizado se puede probar en el siguiente simulador:

[Simple C3D Playground](https://diegocali.github.io/simple-c3d-playground/)

## Estructura

```text
Compiler/       Compilador de alto nivel a código de tres direcciones
IRepresentation/Representación de programas, bloques y líneas TAC
Pipeline/       Pases de optimización
main.py         Punto de entrada del optimizador
```

