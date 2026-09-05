import subprocess
import tempfile
import re
from encoder_skeleton import encode_instruction

CASOS = [
    # ADD
    "add x0, x1, x2",
    "add x31, x0, x30",
    "add x12, x13, x14",

    # SUB
    "sub x0, x31, x1",
    "sub x15, x16, x17",
    "sub x31, x31, x0",

    # AND
    "and x0, x5, x6",
    "and x31, x30, x29",
    "and x9, x10, x11",

    # OR
    "or x0, x2, x3",
    "or x31, x1, x0",
    "or x20, x21, x22",

    # ADDI
    "addi x1, x0, 0",
    "addi x31, x1, 2047",
    "addi x2, x31, -2048",

    # ANDI
    "andi x3, x0, 0",
    "andi x31, x4, 2047",
    "andi x5, x31, -2048",

    # LW
    "lw x1, 0(x0)",
    "lw x31, 2047(x1)",
    "lw x2, -2048(x31)",

    # LB
    "lb x1, 0(x0)",
    "lb x31, 2047(x1)",
    "lb x2, -2048(x31)",

    # SW
    "sw x1, 0(x0)",
    "sw x31, 2047(x1)",
    "sw x2, -2048(x31)",

    # SB
    "sb x1, 0(x0)",
    "sb x31, 2047(x1)",
    "sb x2, -2048(x31)",

    # BEQ
    "beq x0, x0, 0",
    "beq x31, x1, 4094",
    "beq x2, x3, -4096",

    # BNE
    "bne x0, x1, 0",
    "bne x31, x0, 4094",
    "bne x4, x5, -4096",
]


def adaptar_branch_para_asm(instruccion):
    partes = instruccion.replace(",", " ").split()
    mnemonic = partes[0]

    if mnemonic not in ("beq", "bne"):
        return instruccion

    rs1 = partes[1]
    rs2 = partes[2]
    offset = int(partes[3])

    if offset >= 0:
        destino = f".+{offset}"
    else:
        destino = f".{offset}"

    return f"{mnemonic} {rs1}, {rs2}, {destino}"


def obtener_objdump(instruccion):
    instruccion_asm = adaptar_branch_para_asm(instruccion)

    with tempfile.TemporaryDirectory() as carpeta:
        archivo_s = f"{carpeta}/prueba.s"
        archivo_o = f"{carpeta}/prueba.o"

        with open(archivo_s, "w") as archivo:
            archivo.write(instruccion_asm + "\n")

        subprocess.run(
            [
                "riscv64-unknown-elf-as",
                "-march=rv32i",
                "-mabi=ilp32",
                archivo_s,
                "-o",
                archivo_o
            ],
            check=True,
            capture_output=True,
            text=True
        )

        resultado = subprocess.run(
            [
                "riscv64-unknown-elf-objdump",
                "-d",
                archivo_o
            ],
            check=True,
            capture_output=True,
            text=True
        )

        patron = r"^\s*[0-9a-f]+:\s+([0-9a-f]{8})\s+"
        coincidencia = re.search(
            patron,
            resultado.stdout,
            re.MULTILINE
        )

        if not coincidencia:
            raise RuntimeError(
                f"No se pudo obtener la codificación de: {instruccion}"
            )

        return "0x" + coincidencia.group(1).lower()


resultados = []
correctos = 0

for instruccion in CASOS:
    modelo = f"0x{encode_instruction(instruccion):08x}"
    oficial = obtener_objdump(instruccion)

    coincide = modelo == oficial

    if coincide:
        correctos += 1
        estado = "OK"
    else:
        estado = "ERROR"

    resultados.append((instruccion, modelo, oficial, estado))

    print(
        f"{estado:5} | {instruccion:25} | "
        f"Modelo: {modelo} | objdump: {oficial}"
    )

print()
print(f"Resultado final: {correctos}/{len(CASOS)} correctos")


with open("validacion_36.md", "w", encoding="utf-8") as archivo:
    archivo.write("# Validación contra toolchain oficial RISC-V\n\n")

    archivo.write(
        "| Instrucción | Modelo propio | objdump | Resultado |\n"
    )

    archivo.write(
        "|---|---|---|---|\n"
    )

    for instruccion, modelo, oficial, estado in resultados:
        archivo.write(
            f"| `{instruccion}` | `{modelo}` | "
            f"`{oficial}` | {estado} |\n"
        )

    archivo.write(
        f"\n**Resultado final: "
        f"{correctos}/{len(CASOS)} casos correctos.**\n"
    )