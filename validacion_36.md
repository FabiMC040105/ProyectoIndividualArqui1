# Validación contra toolchain oficial RISC-V

| Instrucción | Modelo propio | objdump | Resultado |
|---|---|---|---|
| `add x0, x1, x2` | `0x00208033` | `0x00208033` | OK |
| `add x31, x0, x30` | `0x01e00fb3` | `0x01e00fb3` | OK |
| `add x12, x13, x14` | `0x00e68633` | `0x00e68633` | OK |
| `sub x0, x31, x1` | `0x401f8033` | `0x401f8033` | OK |
| `sub x15, x16, x17` | `0x411807b3` | `0x411807b3` | OK |
| `sub x31, x31, x0` | `0x400f8fb3` | `0x400f8fb3` | OK |
| `and x0, x5, x6` | `0x0062f033` | `0x0062f033` | OK |
| `and x31, x30, x29` | `0x01df7fb3` | `0x01df7fb3` | OK |
| `and x9, x10, x11` | `0x00b574b3` | `0x00b574b3` | OK |
| `or x0, x2, x3` | `0x00316033` | `0x00316033` | OK |
| `or x31, x1, x0` | `0x0000efb3` | `0x0000efb3` | OK |
| `or x20, x21, x22` | `0x016aea33` | `0x016aea33` | OK |
| `addi x1, x0, 0` | `0x00000093` | `0x00000093` | OK |
| `addi x31, x1, 2047` | `0x7ff08f93` | `0x7ff08f93` | OK |
| `addi x2, x31, -2048` | `0x800f8113` | `0x800f8113` | OK |
| `andi x3, x0, 0` | `0x00007193` | `0x00007193` | OK |
| `andi x31, x4, 2047` | `0x7ff27f93` | `0x7ff27f93` | OK |
| `andi x5, x31, -2048` | `0x800ff293` | `0x800ff293` | OK |
| `lw x1, 0(x0)` | `0x00002083` | `0x00002083` | OK |
| `lw x31, 2047(x1)` | `0x7ff0af83` | `0x7ff0af83` | OK |
| `lw x2, -2048(x31)` | `0x800fa103` | `0x800fa103` | OK |
| `lb x1, 0(x0)` | `0x00000083` | `0x00000083` | OK |
| `lb x31, 2047(x1)` | `0x7ff08f83` | `0x7ff08f83` | OK |
| `lb x2, -2048(x31)` | `0x800f8103` | `0x800f8103` | OK |
| `sw x1, 0(x0)` | `0x00102023` | `0x00102023` | OK |
| `sw x31, 2047(x1)` | `0x7ff0afa3` | `0x7ff0afa3` | OK |
| `sw x2, -2048(x31)` | `0x802fa023` | `0x802fa023` | OK |
| `sb x1, 0(x0)` | `0x00100023` | `0x00100023` | OK |
| `sb x31, 2047(x1)` | `0x7ff08fa3` | `0x7ff08fa3` | OK |
| `sb x2, -2048(x31)` | `0x802f8023` | `0x802f8023` | OK |
| `beq x0, x0, 0` | `0x00000063` | `0x00000063` | OK |
| `beq x31, x1, 4094` | `0x7e1f8fe3` | `0x7e1f8fe3` | OK |
| `beq x2, x3, -4096` | `0x80310063` | `0x80310063` | OK |
| `bne x0, x1, 0` | `0x00101063` | `0x00101063` | OK |
| `bne x31, x0, 4094` | `0x7e0f9fe3` | `0x7e0f9fe3` | OK |
| `bne x4, x5, -4096` | `0x80521063` | `0x80521063` | OK |

**Resultado final: 36/36 casos correctos.**
