# Compilador

Este directorio contiene un compilador pequeño que transforma un lenguaje de
alto nivel en código de tres direcciones (TAC). El resultado es compatible con
el optimizador del proyecto y con el simulador
[Simple C3D Playground](https://diegocali.github.io/simple-c3d-playground/).

## Lenguaje soportado

El compilador permite:

- Asignaciones de variables.
- Literales numéricos y booleanos (`true` y `false`).
- Operaciones `+`, `-` y `*`.
- Comparaciones `==`, `<`, `>`, `<=` y `>=`.
- Operadores lógicos `&&` y `||`.
- Sentencias `print`.
- Estructuras `if`, `if/else` y `while`.
- Comentarios de una línea con `//`.

Ejemplo:

```text
score = 72;
bonus = 8;

if (score >= 90 || bonus >= 10) {
    print score + bonus;
} else {
    print score - bonus;
}
```

## Requisitos

Se necesita Python 3.9 o posterior y el paquete
[PLY](https://www.dabeaz.com/ply/). Desde el directorio raíz del proyecto:

```bash
python3 -m pip install ply
```

También puede utilizarse el entorno virtual local, si existe:

```bash
Compiler/venv/bin/python Compiler/main.py
```

El entorno virtual local está excluido de Git y no debe subirse al repositorio.

## Generar código TAC

El programa fuente de ejemplo está en [main.py](./main.py). Para generar el
código TAC desde el directorio raíz:

```bash
cd Compiler
python3 main.py > ../code.tac
```

El compilador escribe el TAC por la salida estándar. El archivo `code.tac` es
un artefacto generado y está excluido mediante el `.gitignore` de la raíz.

## Optimizar el resultado

Después de generar `code.tac`, vuelve al directorio raíz y ejecuta:

```bash
cd ..
python3 main.py
```

El optimizador leerá `code.tac`, mostrará el resultado en la terminal y
escribirá `optimized.tac`.

## Probar en el simulador

Para ejecutar el código generado:

1. Genera `code.tac` y, opcionalmente, `optimized.tac`.
2. Abre
   [Simple C3D Playground](https://diegocali.github.io/simple-c3d-playground/).
3. Copia el contenido de `optimized.tac` en el editor del simulador.
4. Ejecuta el programa para observar el resultado.

