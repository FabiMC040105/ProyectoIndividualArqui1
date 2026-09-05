# Documentación técnica
## Codificador Educativo de Instrucciones RISC-V

**Curso:** CE-4301 Arquitectura de Computadores I  
**Proyecto:** Codificador Educativo de Instrucciones RISC-V  
**ISA utilizada:** RV32I

---

## 1. Descripción general

El proyecto consiste en una herramienta que recibe una única instrucción del subconjunto RV32I definido para el proyecto y genera su codificación de 32 bits.

Además del valor binario y hexadecimal, la herramienta muestra los diferentes campos que forman la instrucción, su posición dentro de los 32 bits y una breve explicación de su función.

El proyecto soporta los formatos R, I, S y B.

Las instrucciones implementadas son:

- `add`
- `sub`
- `and`
- `or`
- `addi`
- `andi`
- `lw`
- `lb`
- `sw`
- `sb`
- `beq`
- `bne`

---

## 2. Fuente utilizada para la codificación

Los valores de `opcode`, `funct3` y `funct7` fueron consultados en la documentación oficial de la ISA RISC-V.

La referencia utilizada fue:

**Andrew Waterman y Krste Asanović. The RISC-V Instruction Set Manual, Volume I: User-Level ISA. RISC-V Foundation.**

Se consultaron principalmente las secciones correspondientes al conjunto base RV32I y a las instrucciones:

- Integer Register-Register Instructions
- Integer Register-Immediate Instructions
- Load and Store Instructions
- Conditional Branch Instructions

A partir de estas tablas se obtuvieron los campos necesarios para cada una de las 12 instrucciones utilizadas en el proyecto.

---

## 3. Instrucciones soportadas

| Instrucción | Formato | opcode | funct3 | funct7 |
|---|---|---|---|---|
| `add` | R | `0110011` | `000` | `0000000` |
| `sub` | R | `0110011` | `000` | `0100000` |
| `and` | R | `0110011` | `111` | `0000000` |
| `or` | R | `0110011` | `110` | `0000000` |
| `addi` | I | `0010011` | `000` | No aplica |
| `andi` | I | `0010011` | `111` | No aplica |
| `lw` | I | `0000011` | `010` | No aplica |
| `lb` | I | `0000011` | `000` | No aplica |
| `sw` | S | `0100011` | `010` | No aplica |
| `sb` | S | `0100011` | `000` | No aplica |
| `beq` | B | `1100011` | `000` | No aplica |
| `bne` | B | `1100011` | `001` | No aplica |

---

## 4. Arquitectura del código

La implementación se encuentra principalmente en el archivo `encoder_skeleton.py`.

El funcionamiento general se dividió en varias etapas:

```text
Instrucción recibida
        ↓
Normalización y parser
        ↓
Identificación del mnemónico
        ↓
Consulta de la tabla de instrucciones
        ↓
Identificación del formato R / I / S / B
        ↓
Interpretación de los operandos
        ↓
Codificación de los campos
        ↓
Construcción de la palabra de 32 bits
        ↓
Generación de la salida explicativa
        ↓
Representación hexadecimal
```

### 4.1 Tabla de instrucciones

Se utilizó un diccionario llamado `INSTRUCTIONS`.

Este diccionario permite guardar para cada mnemónico la información necesaria para codificarlo, como:

- Formato.
- `opcode`.
- `funct3`.
- `funct7`, cuando aplica.
- Tipo de instrucción I cuando es necesario distinguir entre una operación aritmética y una carga.

La idea de utilizar un diccionario fue evitar crear una implementación completamente separada para cada una de las 12 instrucciones.

Por ejemplo, `add`, `sub`, `and` y `or` comparten la misma estructura de formato R, por lo que pueden utilizar la misma lógica de codificación cambiando solamente los valores de sus campos de función.

---

## 5. Procesamiento de la entrada

La función `parse_instruction()` recibe la instrucción como texto.

Antes de separar sus componentes se reemplazan:

- Comas.
- Paréntesis.

por espacios.

De esta forma una instrucción como:

```text
lw x5, -8(x6)
```

se puede transformar en elementos equivalentes a:

```text
["lw", "x5", "-8", "x6"]
```

Esto permite procesar con la misma idea tanto instrucciones aritméticas como instrucciones que utilizan la sintaxis `offset(registro)`.

También se implementó la función `parse_register()`, encargada de convertir un registro escrito como:

```text
x5
```

al valor entero:

```text
5
```

La función además verifica que el registro se encuentre entre `x0` y `x31`.

---

## 6. Codificación de los formatos

### 6.1 Formato R

El formato R utiliza la siguiente distribución:

```text
[funct7][rs2][rs1][funct3][rd][opcode]
```

Los campos ocupan:

| Campo | Bits |
|---|---|
| funct7 | 31-25 |
| rs2 | 24-20 |
| rs1 | 19-15 |
| funct3 | 14-12 |
| rd | 11-7 |
| opcode | 6-0 |

Para colocar los campos en su posición se utilizaron operaciones de desplazamiento de bits.

Por ejemplo:

```python
rd << 7
```

desplaza el número de registro hasta los bits 11-7.

Posteriormente los campos se combinan mediante OR bit a bit.

---

### 6.2 Formato I

El formato I utiliza:

```text
[imm[11:0]][rs1][funct3][rd][opcode]
```

El inmediato tiene 12 bits con signo, por lo que su rango es:

```text
-2048 a 2047
```

Para los inmediatos negativos se conserva su representación de 12 bits en complemento a dos.

Dentro de las instrucciones tipo I se distinguen dos formas de operandos.

Las instrucciones aritméticas como:

```text
addi x5, x6, -12
```

se interpretan como:

```text
rd = x5
rs1 = x6
imm = -12
```

Mientras que una carga como:

```text
lw x5, 8(x6)
```

se interpreta como:

```text
rd = x5
imm = 8
rs1 = x6
```

---

### 6.3 Formato S

El formato S se utiliza para las instrucciones `sw` y `sb`.

Su estructura es:

```text
[imm11:5][rs2][rs1][funct3][imm4:0][opcode]
```

Una diferencia importante de este formato es que el inmediato de 12 bits no se almacena de forma continua.

Se divide en:

```text
imm[11:5]
imm[4:0]
```

Por ejemplo:

```text
sw x8, -4(x2)
```

utiliza:

```text
rs2 = x8
rs1 = x2
imm = -4
```

El registro `rs2` contiene el dato que se desea almacenar y `rs1` funciona como registro base para calcular la dirección de memoria.

---

### 6.4 Formato B

Las instrucciones `beq` y `bne` utilizan formato B.

La distribución del inmediato es:

```text
[imm12][imm10:5][rs2][rs1][funct3][imm4:1][imm11][opcode]
```

El desplazamiento de branch se interpreta como un inmediato de 13 bits, aunque solamente 12 bits se almacenan en la instrucción.

El bit:

```text
imm[0]
```

no se almacena debido a que es implícitamente cero.

Los bits del inmediato se reorganizan de la siguiente manera:

```text
imm[12]   → bit 31
imm[10:5] → bits 30-25
imm[4:1]  → bits 11-8
imm[11]   → bit 7
```

El rango utilizado para estos desplazamientos es:

```text
-4096 a 4094
```

y solamente se aceptan desplazamientos pares.

---

## 7. Construcción de la palabra de 32 bits

Una vez obtenidos los campos de la instrucción, estos se desplazan hasta la posición que les corresponde.

Por ejemplo, para formato R:

```python
word = (
    (funct7 << 25)
    | (rs2 << 20)
    | (rs1 << 15)
    | (funct3 << 12)
    | (rd << 7)
    | opcode
)
```

El operador `<<` permite colocar cada campo en su posición y el operador `|` permite combinarlos en una sola palabra de 32 bits.

Este mismo principio se utiliza para los formatos I, S y B, cambiando la posición y distribución de los campos.

---

## 8. Generación de la salida explicativa

La función `explain_instruction()` recibe la palabra de 32 bits generada por el codificador.

La función identifica nuevamente el formato de la instrucción y extrae cada campo utilizando desplazamientos a la derecha y máscaras de bits.

Esto puede verse como el proceso contrario a la codificación:

```text
encode_instruction()
campos → palabra de 32 bits

explain_instruction()
palabra de 32 bits → campos
```

La salida muestra:

- Instrucción recibida.
- Formato.
- Binario completo de 32 bits.
- Posición de cada campo.
- Valor binario.
- Valor decimal.
- Función del campo.
- Codificación hexadecimal.

---

# 9. Ejemplos de salida

## 9.1 Formato R

Entrada:

```bash
./run.sh "add x5, x6, x7"
```

Salida:

```text
Instrucción: add x5, x6, x7
Formato: R
Binario: 00000000011100110000001010110011

Campos:
Bits 31-25 | funct7 | 0000000 (0) | Selecciona la operación junto con funct3.
Bits 24-20 | rs2    | 00111 (7) | Segundo registro fuente: x7.
Bits 19-15 | rs1    | 00110 (6) | Primer registro fuente: x6.
Bits 14-12 | funct3 | 000 (0) | Selecciona la operación junto con funct7.
Bits 11-7  | rd     | 00101 (5) | Registro destino: x5.
Bits 6-0   | opcode | 0110011 (51) | Identifica la familia de la instrucción.

HEX: 0x007302b3
```

---

## 9.2 Formato I

Entrada:

```bash
./run.sh "addi x5, x6, -12"
```

Salida:

```text
Instrucción: addi x5, x6, -12
Formato: I
Binario: 11111111010000110000001010010011

Campos:
Bits 31-20 | imm    | 111111110100 (-12) | Valor inmediato utilizado por la operación aritmética.
Bits 19-15 | rs1    | 00110 (6) | Registro fuente: x6.
Bits 14-12 | funct3 | 000 (0) | Identifica la operación específica.
Bits 11-7  | rd     | 00101 (5) | Registro destino: x5.
Bits 6-0   | opcode | 0010011 (19) | Identifica la familia de la instrucción.

HEX: 0xff430293
```

---

## 9.3 Formato S

Entrada:

```bash
./run.sh "sw x8, -4(x2)"
```

Salida:

```text
Instrucción: sw x8, -4(x2)
Formato: S
Binario: 11111110100000010010111000100011

Campos:
Bits 31-25 | imm[11:5] | 1111111 (127) | Parte superior del inmediato.
Bits 24-20 | rs2       | 01000 (8) | Registro cuyo dato se almacena: x8.
Bits 19-15 | rs1       | 00010 (2) | Registro base de la dirección: x2.
Bits 14-12 | funct3    | 010 (2) | Identifica el tipo de almacenamiento.
Bits 11-7  | imm[4:0]  | 11100 (28) | Parte inferior del inmediato.
Bits 6-0   | opcode    | 0100011 (35) | Identifica la familia de almacenamiento.

Inmediato reconstruido: -4.
HEX: 0xfe812e23
```

---

## 9.4 Formato B

Entrada:

```bash
./run.sh "bne x4, x7, -16"
```

Salida:

```text
Instrucción: bne x4, x7, -16
Formato: B
Binario: 11111110011100100001100011100011

Campos:
Bit 31     | imm[12]   | 1 (1) | Bit de signo del desplazamiento.
Bits 30-25 | imm[10:5] | 111111 (63) | Parte del desplazamiento.
Bits 24-20 | rs2       | 00111 (7) | Segundo registro a comparar: x7.
Bits 19-15 | rs1       | 00100 (4) | Primer registro a comparar: x4.
Bits 14-12 | funct3    | 001 (1) | Define la condición del salto.
Bits 11-8  | imm[4:1]  | 1000 (8) | Parte del desplazamiento.
Bit 7      | imm[11]   | 1 (1) | Parte reorganizada del desplazamiento.
Bits 6-0   | opcode    | 1100011 (99) | Identifica una instrucción de branch.

Inmediato reconstruido: -16. El bit imm[0] es implícitamente 0.
HEX: 0xfe7218e3
```

---

# 10. Validación

La herramienta se verificó de dos formas.

## 10.1 Vectores de ejemplo

Primero se utilizaron los 36 vectores proporcionados con el proyecto mediante el archivo:

```text
test_vectores.py
```

El resultado obtenido fue:

```text
Resultado: 36/36 correctos
```

---

## 10.2 Validación contra el toolchain RISC-V

Posteriormente se construyeron 36 casos propios:

```text
12 instrucciones × 3 casos por instrucción
```

Los casos fueron comparados contra:

```text
riscv64-unknown-elf-as
riscv64-unknown-elf-objdump
```

utilizando:

```text
-march=rv32i
-mabi=ilp32
```

Para las instrucciones de branch fue necesario expresar el destino al ensamblador como una dirección relativa al PC.

Por ejemplo:

```text
beq x1, x2, .+8
```

representa un desplazamiento de 8 bytes con respecto a la posición actual.

Esto se utilizó solamente para realizar una comparación equivalente con el toolchain. La entrada de la herramienta desarrollada continúa utilizando directamente:

```text
beq x1, x2, 8
```

El resultado final de la validación fue:

```text
Resultado final: 36/36 correctos
```

La tabla completa de resultados se encuentra en:

```text
validacion_36.md
```

En dicho archivo se muestra para cada caso:

- La instrucción.
- Codificación producida por el modelo.
- Codificación obtenida con `objdump`.
- Resultado de la comparación.

---

## 11. Decisiones de diseño principales

Durante la implementación se tomaron las siguientes decisiones:

1. Utilizar una tabla de instrucciones para separar la información propia de cada mnemónico de la lógica general de codificación.

2. Reutilizar la lógica de cada formato en lugar de implementar un codificador completamente distinto para cada instrucción.

3. Normalizar la entrada antes de procesarla para manejar de forma sencilla comas, paréntesis y espacios.

4. Trabajar internamente con valores enteros y operaciones de bits en lugar de construir la codificación concatenando strings binarios.

5. Validar el rango de registros e inmediatos antes de generar la codificación.

6. Separar la codificación de la representación educativa, utilizando `encode_instruction()` para generar la palabra y `explain_instruction()` para mostrar y explicar sus campos.

7. Automatizar la comparación contra el toolchain para reducir errores en la validación de los 36 casos.

---

## 12. Resultado final

Se implementaron correctamente las 12 instrucciones solicitadas y los cuatro formatos requeridos.

La herramienta pasó:

```text
36/36 vectores de ejemplo
```

y:

```text
36/36 casos propios comparados contra el toolchain RISC-V
```

El punto de entrada final utilizado por la herramienta es:

```bash
./run.sh "<instruccion>"
```

y la salida mantiene la línea:

```text
HEX: 0xXXXXXXXX
```

para permitir su verificación automática.