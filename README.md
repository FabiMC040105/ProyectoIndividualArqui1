# Codificador Educativo de Instrucciones RISC-V

Proyecto individual del curso CE-4301 Arquitectura de Computadores I.

Esta herramienta recibe una instrucción del subconjunto RV32I definido para el proyecto y genera su codificación binaria de 32 bits, su representación hexadecimal y un desglose de los campos que forman la instrucción.

## Requisitos

Para ejecutar la herramienta se necesita:

- Python 3
- Bash
- Un entorno Linux o compatible con Bash

Para realizar las pruebas de verificación contra RISC-V también se necesita el toolchain utilizado durante el desarrollo.

La implementación no requiere librerías externas de Python.

## Preparación de la herramienta

Después de clonar o descargar el repositorio, ubicarse en la carpeta raíz del proyecto.

Dar permiso de ejecución al archivo `run.sh`:

```bash
chmod +x run.sh
```

El programa debe ejecutarse utilizando el punto de entrada definido para el proyecto:

```bash
./run.sh "<instruccion>"
```

Por ejemplo:

```bash
./run.sh "add x5, x6, x7"
```

También se pueden utilizar instrucciones con inmediatos o acceso a memoria:

```bash
./run.sh "addi x5, x6, -12"
./run.sh "lw x5, 8(x6)"
./run.sh "sw x8, -4(x2)"
./run.sh "beq x1, x2, 8"
```

La salida de la herramienta muestra el formato identificado, la representación binaria de 32 bits, el desglose de sus campos y la codificación hexadecimal.

Además, siempre se genera una línea con el siguiente formato:

```text
HEX: 0xXXXXXXXX
```

Esta línea es utilizada para permitir la verificación automática de la herramienta.

## Instalación del toolchain RISC-V utilizado

Para las pruebas de verificación se utilizó Ubuntu mediante WSL2.

Primero se actualiza la lista de paquetes:

```bash
sudo apt update
```

Luego se instala el toolchain utilizado:

```bash
sudo apt install binutils-riscv64-unknown-elf gcc-riscv64-unknown-elf -y
```

La instalación se puede comprobar con:

```bash
riscv64-unknown-elf-as --version
riscv64-unknown-elf-objdump --version
```

Aunque las herramientas instaladas utilizan el prefijo `riscv64-unknown-elf`, durante la verificación las instrucciones se ensamblan específicamente para RV32I mediante las opciones:

```text
-march=rv32i -mabi=ilp32
```

## Verificación con los vectores de ejemplo

El archivo `test_vectores.py` permite comprobar automáticamente el funcionamiento del codificador utilizando el archivo `vectores_ejemplo.txt` proporcionado con el proyecto.

La prueba se ejecuta con:

```bash
python3 test_vectores.py
```

Durante el desarrollo se obtuvo el siguiente resultado:

```text
Resultado: 36/36 correctos
```

Estos vectores se utilizaron como una comprobación inicial del funcionamiento del modelo y no como sustituto de los 36 casos propios utilizados para la validación contra el toolchain.

## Verificación contra el toolchain RISC-V

Para la validación propia se utiliza el archivo:

```text
validar_toolchain.py
```

El script contiene 36 casos de prueba propios, correspondientes a:

- 12 instrucciones soportadas.
- 3 casos diferentes para cada instrucción.

Los casos incluyen distintos registros y, cuando corresponde, valores cero, positivos, negativos y valores límite.

Para cada caso, el script realiza el siguiente proceso:

1. Obtiene la codificación producida por el codificador desarrollado.
2. Ensambla la misma instrucción utilizando `riscv64-unknown-elf-as`.
3. Obtiene la codificación de referencia utilizando `riscv64-unknown-elf-objdump`.
4. Compara ambas codificaciones hexadecimales.
5. Indica si el resultado coincide o no.

La validación se ejecuta con:

```bash
python3 validar_toolchain.py
```

El resultado final obtenido fue:

```text
Resultado final: 36/36 correctos
```

Como parte de la ejecución también se genera el archivo:

```text
validacion_36.md
```

Este archivo contiene la evidencia de los 36 casos probados, mostrando para cada uno:

- La instrucción utilizada.
- La codificación obtenida por el modelo propio.
- La codificación obtenida mediante `objdump`.
- El resultado de la comparación.

## Archivos relacionados con la ejecución y verificación

- `encoder_skeleton.py`: implementación principal del codificador.
- `run.sh`: punto de entrada de la herramienta.
- `test_vectores.py`: prueba automática utilizando los vectores de ejemplo.
- `vectores_ejemplo.txt`: vectores de comprobación proporcionados para el proyecto.
- `validar_toolchain.py`: validación de los 36 casos propios contra el toolchain RISC-V.
- `validacion_36.md`: evidencia generada de la validación contra `objdump`.

La documentación técnica de la implementación se encuentra en `DOCUMENTACION.md`.
