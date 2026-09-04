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

    raise NotImplementedError(f"Formato {formato} pendiente de implementar")
def explain_instruction(instruction: str, word: int) -> str:

    return f"Binario: {word:032b}"

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
