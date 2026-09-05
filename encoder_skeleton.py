#!/usr/bin/env python3
"""
Esqueleto del Codificador Educativo de Instrucciones RISC-V.
CE4301 Arquitectura de Computadores I — Proyecto Individual — 2026-II

Este esqueleto ya implementa el contrato de línea de comandos y de salida
requerido por la especificación. Usted debe completar las dos funciones
marcadas con TODO; puede modificar el resto del archivo si lo necesita,
siempre que se preserve el contrato de invocación y la línea "HEX: 0x...".

No es obligatorio usar este esqueleto ni Python: puede implementar su
propia herramienta desde cero, en el lenguaje que prefiera, siempre que
respete el mismo contrato (ver especificación, sección "Modo de operación").
"""
import sys

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",
              "lw", "lb", "sw", "sb", "beq", "bne"]


INSTRUCTIONS = {
    # Formato R
    "add": {
        "format": "R",
        "opcode": 0b0110011,
        "funct3": 0b000,
        "funct7": 0b0000000
    },
    "sub": {
        "format": "R",
        "opcode": 0b0110011,
        "funct3": 0b000,
        "funct7": 0b0100000
    },
    "and": {
        "format": "R",
        "opcode": 0b0110011,
        "funct3": 0b111,
        "funct7": 0b0000000
    },
    "or": {
        "format": "R",
        "opcode": 0b0110011,
        "funct3": 0b110,
        "funct7": 0b0000000
    },

    # Formato I - aritméticas
    "addi": {
        "format": "I",
        "kind": "arith",
        "opcode": 0b0010011,
        "funct3": 0b000
    },
    "andi": {
        "format": "I",
        "kind": "arith",
        "opcode": 0b0010011,
        "funct3": 0b111
    },

    # Formato I - cargas
    "lw": {
        "format": "I",
        "kind": "load",
        "opcode": 0b0000011,
        "funct3": 0b010
    },
    "lb": {
        "format": "I",
        "kind": "load",
        "opcode": 0b0000011,
        "funct3": 0b000
    },

    # Formato S
    "sw": {
        "format": "S",
        "opcode": 0b0100011,
        "funct3": 0b010
    },
    "sb": {
        "format": "S",
        "opcode": 0b0100011,
        "funct3": 0b000
    },

    # Formato B
    "beq": {
        "format": "B",
        "opcode": 0b1100011,
        "funct3": 0b000
    },
    "bne": {
        "format": "B",
        "opcode": 0b1100011,
        "funct3": 0b001
    }
}


def parse_instruction(instruction):
    texto = instruction.lower()

    texto = texto.replace(",", " ")
    texto = texto.replace("(", " ")
    texto = texto.replace(")", " ")

    tokens = texto.split()

    mnemonic = tokens[0]
    operands = tokens[1:]

    return mnemonic, operands


def parse_register(reg):
    if not reg.startswith("x"):
        raise ValueError(f"Registro inválido: {reg}")

    numero = int(reg[1:])

    if numero < 0 or numero > 31:
        raise ValueError(f"Registro fuera de rango: {reg}")

    return numero


def encode_instruction(instruction: str) -> int:
    mnemonic, operands = parse_instruction(instruction)

    if mnemonic not in INSTRUCTIONS:
        raise ValueError(f"Instrucción no soportada: {mnemonic}")

    info = INSTRUCTIONS[mnemonic]
    formato = info["format"]

    if formato == "R":
        if len(operands) != 3:
            raise ValueError("Una instrucción tipo R requiere 3 operandos")

        rd = parse_register(operands[0])
        rs1 = parse_register(operands[1])
        rs2 = parse_register(operands[2])

        opcode = info["opcode"]
        funct3 = info["funct3"]
        funct7 = info["funct7"]

        word = (
            (funct7 << 25)
            | (rs2 << 20)
            | (rs1 << 15)
            | (funct3 << 12)
            | (rd << 7)
            | opcode
        )

        return word

    elif formato == "I":
        if len(operands) != 3:
            raise ValueError("Una instrucción tipo I requiere 3 operandos")

        if info["kind"] == "arith":
            rd = parse_register(operands[0])
            rs1 = parse_register(operands[1])
            imm = int(operands[2])

        elif info["kind"] == "load":
            rd = parse_register(operands[0])
            imm = int(operands[1])
            rs1 = parse_register(operands[2])

        if imm < -2048 or imm > 2047:
            raise ValueError("Inmediato fuera de rango para formato I")

        opcode = info["opcode"]
        funct3 = info["funct3"]

        imm12 = imm & 0xFFF

        word = (
            (imm12 << 20)
            | (rs1 << 15)
            | (funct3 << 12)
            | (rd << 7)
            | opcode
        )

        return word

    elif formato == "S":
        if len(operands) != 3:
            raise ValueError("Una instrucción tipo S requiere 3 operandos")

        rs2 = parse_register(operands[0])
        imm = int(operands[1])
        rs1 = parse_register(operands[2])

        if imm < -2048 or imm > 2047:
            raise ValueError("Inmediato fuera de rango para formato S")

        opcode = info["opcode"]
        funct3 = info["funct3"]

        imm12 = imm & 0xFFF

        imm_11_5 = (imm12 >> 5) & 0x7F
        imm_4_0 = imm12 & 0x1F

        word = (
            (imm_11_5 << 25)
            | (rs2 << 20)
            | (rs1 << 15)
            | (funct3 << 12)
            | (imm_4_0 << 7)
            | opcode
        )

        return word

    elif formato == "B":
        if len(operands) != 3:
            raise ValueError("Una instrucción tipo B requiere 3 operandos")

        rs1 = parse_register(operands[0])
        rs2 = parse_register(operands[1])
        imm = int(operands[2])

        if imm < -4096 or imm > 4094:
            raise ValueError("Inmediato fuera de rango para formato B")

        if imm % 2 != 0:
            raise ValueError("El desplazamiento de una instrucción B debe ser par")

        opcode = info["opcode"]
        funct3 = info["funct3"]

        imm13 = imm & 0x1FFF

        imm_12 = (imm13 >> 12) & 0x1
        imm_10_5 = (imm13 >> 5) & 0x3F
        imm_4_1 = (imm13 >> 1) & 0xF
        imm_11 = (imm13 >> 11) & 0x1

        word = (
            (imm_12 << 31)
            | (imm_10_5 << 25)
            | (rs2 << 20)
            | (rs1 << 15)
            | (funct3 << 12)
            | (imm_4_1 << 8)
            | (imm_11 << 7)
            | opcode
        )

        return word

    raise NotImplementedError(f"Formato {formato} pendiente de implementar")
def explain_instruction(instruction: str, word: int) -> str:
    mnemonic, operands = parse_instruction(instruction)

    if mnemonic not in INSTRUCTIONS:
        raise ValueError(f"Instrucción no soportada: {mnemonic}")

    info = INSTRUCTIONS[mnemonic]
    formato = info["format"]

    lines = [
        f"Instrucción: {instruction}",
        f"Formato: {formato}",
        f"Binario: {word:032b}",
        "",
        "Campos:"
    ]

    if formato == "R":
        funct7 = (word >> 25) & 0x7F
        rs2 = (word >> 20) & 0x1F
        rs1 = (word >> 15) & 0x1F
        funct3 = (word >> 12) & 0x7
        rd = (word >> 7) & 0x1F
        opcode = word & 0x7F

        lines += [
            f"Bits 31-25 | funct7 | {funct7:07b} ({funct7}) | Selecciona la operación junto con funct3.",
            f"Bits 24-20 | rs2    | {rs2:05b} ({rs2}) | Segundo registro fuente: x{rs2}.",
            f"Bits 19-15 | rs1    | {rs1:05b} ({rs1}) | Primer registro fuente: x{rs1}.",
            f"Bits 14-12 | funct3 | {funct3:03b} ({funct3}) | Selecciona la operación junto con funct7.",
            f"Bits 11-7  | rd     | {rd:05b} ({rd}) | Registro destino: x{rd}.",
            f"Bits 6-0   | opcode | {opcode:07b} ({opcode}) | Identifica la familia de la instrucción."
        ]

    elif formato == "I":
        imm12 = (word >> 20) & 0xFFF
        rs1 = (word >> 15) & 0x1F
        funct3 = (word >> 12) & 0x7
        rd = (word >> 7) & 0x1F
        opcode = word & 0x7F

        #vuelve a interpretar correctamente el complemento a 2 como num negativo
        if imm12 & 0x800:
            imm = imm12 - 0x1000
        else:
            imm = imm12

        if info["kind"] == "load":
            rol_imm = "Desplazamiento usado junto con rs1 para calcular la dirección de memoria."
            rol_rs1 = f"Registro base para la dirección de memoria: x{rs1}."
        else:
            rol_imm = "Valor inmediato utilizado por la operación aritmética."
            rol_rs1 = f"Registro fuente: x{rs1}."

        lines += [
            f"Bits 31-20 | imm    | {imm12:012b} ({imm}) | {rol_imm}",
            f"Bits 19-15 | rs1    | {rs1:05b} ({rs1}) | {rol_rs1}",
            f"Bits 14-12 | funct3 | {funct3:03b} ({funct3}) | Identifica la operación específica.",
            f"Bits 11-7  | rd     | {rd:05b} ({rd}) | Registro destino: x{rd}.",
            f"Bits 6-0   | opcode | {opcode:07b} ({opcode}) | Identifica la familia de la instrucción."
        ]

    elif formato == "S":
        imm_11_5 = (word >> 25) & 0x7F
        rs2 = (word >> 20) & 0x1F
        rs1 = (word >> 15) & 0x1F
        funct3 = (word >> 12) & 0x7
        imm_4_0 = (word >> 7) & 0x1F
        opcode = word & 0x7F

        imm12 = (imm_11_5 << 5) | imm_4_0 #los volvemos a pegar

        if imm12 & 0x800:
            imm = imm12 - 0x1000
        else:
            imm = imm12

        lines += [
            f"Bits 31-25 | imm[11:5] | {imm_11_5:07b} ({imm_11_5}) | Parte superior del inmediato.",
            f"Bits 24-20 | rs2       | {rs2:05b} ({rs2}) | Registro cuyo dato se almacena: x{rs2}.",
            f"Bits 19-15 | rs1       | {rs1:05b} ({rs1}) | Registro base de la dirección: x{rs1}.",
            f"Bits 14-12 | funct3    | {funct3:03b} ({funct3}) | Identifica el tipo de almacenamiento.",
            f"Bits 11-7  | imm[4:0]  | {imm_4_0:05b} ({imm_4_0}) | Parte inferior del inmediato.",
            f"Bits 6-0   | opcode    | {opcode:07b} ({opcode}) | Identifica la familia de almacenamiento.",
            f"Inmediato reconstruido: {imm}."
        ]

    elif formato == "B":
        imm_12 = (word >> 31) & 0x1
        imm_10_5 = (word >> 25) & 0x3F
        rs2 = (word >> 20) & 0x1F
        rs1 = (word >> 15) & 0x1F
        funct3 = (word >> 12) & 0x7
        imm_4_1 = (word >> 8) & 0xF
        imm_11 = (word >> 7) & 0x1
        opcode = word & 0x7F

        imm13 = (
            (imm_12 << 12)
            | (imm_11 << 11)
            | (imm_10_5 << 5)
            | (imm_4_1 << 1)
        )

        if imm13 & 0x1000:
            imm = imm13 - 0x2000
        else:
            imm = imm13

        lines += [
            f"Bit 31     | imm[12]   | {imm_12:b} ({imm_12}) | Bit de signo del desplazamiento.",
            f"Bits 30-25 | imm[10:5] | {imm_10_5:06b} ({imm_10_5}) | Parte del desplazamiento.",
            f"Bits 24-20 | rs2       | {rs2:05b} ({rs2}) | Segundo registro a comparar: x{rs2}.",
            f"Bits 19-15 | rs1       | {rs1:05b} ({rs1}) | Primer registro a comparar: x{rs1}.",
            f"Bits 14-12 | funct3    | {funct3:03b} ({funct3}) | Define la condición del salto.",
            f"Bits 11-8  | imm[4:1]  | {imm_4_1:04b} ({imm_4_1}) | Parte del desplazamiento.",
            f"Bit 7      | imm[11]   | {imm_11:b} ({imm_11}) | Parte reorganizada del desplazamiento.",
            f"Bits 6-0   | opcode    | {opcode:07b} ({opcode}) | Identifica una instrucción de branch.",
            f"Inmediato reconstruido: {imm}. El bit imm[0] es implícitamente 0."
        ]

    return "\n".join(lines)

def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()
