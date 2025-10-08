# Hoja de referencia LEG - Versión 0.1

## Registros (16 registros) 

| Nombre   | Uso                                              |
|----------|--------------------------------------------------|
| L0       | Argumento / Valor de retorno / Variable temporal |
| L1-L2    | Argumento / Variable temporal                    |
| L3-L7    | Variables preservadas                            |
| L8-L11 (P0-P3) | Variable temporal                          |
| L12 (SP) | Puntero a la pila de memoria                     |
| L13 (LR) | Puntero de link / Dirección de retorno           |
| L14 (PC) | Contador de programa                             |
| L15 (Cero) | Número cero     |



## Tipos de Instrucciones

### Formatos (32 bits) 

- R: X(14) | RS2(4) | RS1(4) | OPC(6) | RD(4)
- B: OFFSET(18) | RS2(4) | OPC(6) | RS1(4)
- M: OFFSET(18) | BASE(4) | OPC(6) | RS/RD(4)
- I: IMM(18) | RS1(4) | OPC(6) | RD(4)
- V: 

### OPCODES

| Mnemónico | OPCODE |
|---|---|
| NOP | 000000 |
| SMA | 000001 |
| SMAI | 000010 |
| RTA | 000011 |
| RTAI | 000100 |
| MUL | 000101 |
| MULI | 000110 |
| Y | 000111 |
| O | 001000 |
| OEX | 001001 |
| ROTD | 001010 |
| ROTI | 001011 |
| NO | 001100 |
| MOV | 001101 |
| ROL | 001110 |
| MODP | 001111 |
| MIX | 010000 |
| MULA | 010001 |
| CRG | 010010 |
| GRD | 010011 |
| RIG | 010100 |
| RIM | 010101 |
| RIP | 010110 |
| RIN | 010111 |

### Instrucciones aritméticas / lógicas  

| Mnemónico | Semántica |  Tipo | Encodificación |
|---|---|---|---|
| NOP | no-op | 1 | R | x[12:0] 0000 0000 000000 0000 |
| SMA rd,rs1,rs2 | rd ← rs1 + rs2 | R | x[12:0] rs2[3:0] rs1[3:0] 000001 rd[3:0] |
| SMAI rd,rs1, imm | rd ← rs1 + imm  | I | imm[17:0] rs1[3:0] 000010 rd[3:0] |
| RTA rd,rs1,rs2 | rd ← rs1 - rs2 | R | x[12:0] rs2[3:0] rs1[3:0] 000011 rd[3:0] |
| RTAI rd,rs1,imm | rd ← rs1 - imm |  I | imm[17:0] rs1[3:0] 000100 rd[3:0] |
| MUL rd,rs1,rs2 | rd ← rs1 * rs2 |  R | x[12:0] rs2[3:0] rs1[3:0] 000101 rd[3:0] |
| MULI rd,rs1,imm | rd ← rs1 * imm | I | imm[17:0] rs1[3:0] 000110 rd[3:0] |
| Y rd,rs1,rs2 | rd ← rs1 & rs2  | R | x[12:0] rs2[3:0] rs1[3:0] 000111 rd[3:0] |
| O rd,rs1,rs2 | rd ← rs1 or rs2 |  R | x[12:0] rs2[3:0] rs1[3:0] 001000 rd[3:0] |
| OEX rd,rs1,rs2 | rd ← rs1 ^ rs2 |  R | x[12:0] rs2[3:0] rs1[3:0] 001001 rd[3:0] |
| ROTD rd,rs,imm | rd ← rotr64(rs, imm) | I | imm[17:0] rs1[3:0] 001010 rd[3:0] |
| ROTI rd,rs,imm | rd ← rotl64(rs, imm) |  I | imm[17:0] rs1[3:0] 001011 rd[3:0] |
| NO rd, rs| rd ← ~rs |  R | x[12:0] 0000 rs1[3:0] 001100 rd[3:0] |
| MOV rd,rs1 | rd ← rs1 | R | x[12:0] 0000 rs1[3:0] 001101 rd[3:0] |

### Instrucciones de Hash (≥3, requeridas)

| Mnemónico | Semántica | Tipo | Encodificación |
|---|---|---|---|
| ROL rd,rs1,imm | rd ← (rs1 << imm) or (rs1 >> (64 - imm)) | I | imm[17:0] rs1[3:0] 001110 rd[3:0] |
| MODP rd,rs1 | rd ← rs1 mod 0xFFFFFFFB | I | imm[17:0] rs1[3:0] 001111 rd[3:0] |
| MIX rd,ra,rb,rc | rd ← (ra & rb) or (~ra & rc) | R | x[12:0] rs2[3:0] rs1[3:0] 010000 rd[3:0]  A este tengo que pensarlo como ponerlo|
| MULA rd,ra,rb,rc | rd ← (ra & rb) or (~ra & rc) | I | imm[17:0] rs1[3:0] 010001 rd[3:0] a este también|

### Instrucciones de acceso a memoria / manejo de datos

| Mnemónico | Semántica | Tipo | Encodificación | 
|---|---|---|---|
| CRG rd,offs(base) | rd ← M64[base+offs] | M |  imm[17:0] rs1[3:0] 010010 rd[3:0] |
| GRD rs,offs(base) | M64[base+offs] ← rs | M | imm[17:0] rs2[3:0] 010011 rs1[3:0] |

### Instrucciones de acceso a bóveda *

| Mnemónico | Semántica | Nota |
|---|---|---|


### Instrucciones de salto / branch

| Mnemónico | Semántica | Tipo | Encodificación |
|---|---|---|---|
| RIG rs1,rs2,off | if(rs1==rs2) pc+=off | B | imm[17:0] rs2[3:0] 010100 rs1[3:0] |
| RIM rs1,rs2,off | if(rs1>=rs2) pc+=off | B | imm[17:0] rs2[3:0] 010101 rs1[3:0] |
| RIP rs1,rs2,off | if(rs1<=rs2) pc+=off | B |imm[17:0] rs2[3:0] 010110 rs1[3:0] |
| RIN rd,off | rd←pc+4; pc+=off | B | imm[17:0] 0000 010111 rd[3:0] |

