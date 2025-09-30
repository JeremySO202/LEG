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

### Formatos (32 bits)  ---> Hay que ver cuáles dejamos

- R: X(13) | RS2(4) | RS1(4) | OPC(6) | RD(4)
- B: OFFSET(18) | RS2(4) | OPC(6) | RS1(4)
- M: OFFSET(18) | BASE(4) | OPC(6) | RS/RD(4)
- I: IMM(18) | RS1(4) | OPC(6) | RD(4)
- V: 



### Instrucciones aritméticas / lógicas  

| Mnemónico | Semántica | Lat. | Tipo | Enc |
|---|---|---|---|---|
| NOP | no-op | 1 | R | 0000000000000 0000 0000 000000 0000 |
| SMA rd,rs1,rs2 | rd ← rs1 + rs2 | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| SMAI rd,rs1,rs2 | rd ← rs1 + rs2 | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| RTA rd,rs1,rs2 | rd ← rs1 - rs2 | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| RTAI rd,rs1,rs2 | rd ← rs1 - rs2 | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| MUL rd,rs1,rs2 | rd ← rs1 * rs2 | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| MULI rd,rs1,rs2 | rd ← rs1 * rs2 | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| Y/O/OEX rd,rs1,rs2 | bitwise | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| ROTD rd,rs,sh | rotr64(rs, sh[0..63]) | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| ROTI rd,rs,sh | rotl64(rs, sh[0..63]) | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| NO rd, rs| rd ← ~rs | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| RET | pc ← x15 | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |
| MOV rd,rs1,rs2 | rd ← rs1 + rs2 | 1 | R | 0000 0000 0000 0000 0000 0000 0000 0000 |

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







