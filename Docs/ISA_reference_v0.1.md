# Hoja de referencia LEG - Versión 0.1

## Registros (32 registros) 

| Nombre   | Uso                                              |
|----------|--------------------------------------------------|
| L0       | Argumento / Valor de retorno / Variable temporal |
| L1-L3  | Argumento / Variable temporal                      |
| L4-L8  | Variables preservadas                              |
| L9-L12 (P0-P4) | Variable temporal                          |
| L13 (SP) | Puntero a la pila de memoria                     |
| L14 (LR) | Puntero de link / Dirección de retorno           |
| L15 (PC) | Contador de programa                             |
| L16 (Prime) | Número primo 0xFFFFFFFB                       |
| L17 (Golden) | Número proporción áurea 0x9e3779b97f4a7c15   |
| L18 (Cero) | Número cero     |


## Tipos de Instrucciones

### Formatos (32 bits)  ---> Hay que ver cuáles dejamos
- R:  OPC(6) | RD(4) | RS1(4) | RS2(4) | FUN(6) | Z(8)
- I:  OPC(6) | RD(4) | RS1(4) | IMM(18) -> solo 1 Addi, MULI, RTAI
- M:  OPC(6) | RD(4) | BASE(4) | OFFS(18)
- B:  OPC(6) | RS1(4) | RS2(4) | OFFS(18)   ; PC-relative
- V:  OPC(6) | SUB(4) | IDX(2) | RD/RS(4) | FUN(4) | Z(12) ; Bóveda/Hash


### Instrucciones aritméticas / lógicas  

| Mnemónico | Semántica | Lat. |
|---|---|---|
| NOP | no-op | 1 |
| SMA rd,rs1,rs2 | rd ← rs1 + rs2 | 1 |
| RTA rd,rs1,rs2 | rd ← rs1 - rs2 | 1 |
| MUL rd,rs1,rs2 | rd ← rs1 * rs2 | 1 |
| Y/O/OEX rd,rs1,rs2 | bitwise | 1 |
| ROTD rd,rs,sh | rotr64(rs, sh[0..63]) | 1 |
| ROTI rd,rs,sh | rotl64(rs, sh[0..63]) | 1 |
| NO rd, rs| rd ← ~rs | 1 |
| RET | pc ← x15 | 1 |
| MOV rd,rs1,rs2 | rd ← rs1 + rs2 | 1 |

### Instrucciones de Hash (≥3, requeridas)

| Mnemónico | Semántica | Lat. |
|---|---|---|
| ROL rd,rs | rd ← (x << r) | (x >> (64 - r)) | 2 |
| MODP rd,rs | rd ← rs mod 0xFFFFFFFB | 2 |
| MIX rd,ra,rb,rc | rd ← (ra & rb) | (~ra & rc) | 1 |
| MULA rd,ra,rb,rc | rd ← (ra & rb) | (~ra & rc) | 1 |

### Instrucciones de acceso a memoria / manejo de datos

| Mnemónico | Semántica | Lat. |
|---|---|---|
| CRG rd,offs(base) | rd ← M64[base+offs] | 2 |
| GRD rs,offs(base) | M64[base+offs] ← rs | 2 |

### Instrucciones de acceso a bóveda *

| Mnemónico | Semántica | Nota |
|---|---|---|
| VSETK kidx, imm64 | bóveda.K[kidx] ← imm64 | carga segura |
| VSETIV i, imm64 | bóveda.IV[i] ← imm64 (i∈{0:A..3:D}) | carga segura |
| HINIT i | H[i] ← bóveda.IV[i] (no expone IV) | no GPR |
| HKLOAD rd,rs,kidx | rd ← rs ^ bóveda.K[kidx] | no filtra K en claro |

### Instrucciones de salto / branch

| Mnemónico | Semántica | Nota |
|---|---|---|
| RIG rs1,rs2,off | if(rs1==rs2) pc+=off | 1 |
| RIM rs1,rs2,off | if(rs1>=rs2) pc+=off | 1 |
| RIP rs1,rs2,off | if(rs1<=rs2) pc+=off | 1 |
| RIN rd,off | rd←pc+4; pc+=off | 1 |


## Encodificación de instrucciones







