from encoder_skeleton import encode_instruction

total = 0
correctos = 0

with open("vectores_ejemplo.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        linea = linea.strip()

        if not linea or linea.startswith("#"):
            continue

        instruccion, esperado = linea.split(";")
        instruccion = instruccion.strip()
        esperado = esperado.strip().lower()

        resultado = encode_instruction(instruccion)
        obtenido = f"0x{resultado:08x}"

        total += 1

        if obtenido == esperado:
            correctos += 1
            print(f"OK   | {instruccion}")
        else:
            print(f"ERROR| {instruccion}")
            print(f"      esperado: {esperado}")
            print(f"      obtenido: {obtenido}")

print()
print(f"Resultado: {correctos}/{total} correctos")